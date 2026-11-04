from __future__ import annotations
import json, os, uuid, tempfile, shutil
from pathlib import Path
from typing import Annotated
import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

ROOT=Path(__file__).resolve().parents[3]
STORE=Path(os.getenv('VISUALSOP_STORAGE',str(Path(__file__).resolve().parents[1]/'storage')))
STORE.mkdir(parents=True,exist_ok=True)
MAX_MB=int(os.getenv('VISUALSOP_MAX_UPLOAD_MB','150'))
ALLOW={'.mp4','.mov','.avi','.mkv','.webm'}
app=FastAPI(title='VisualSOP Checker API',version='0.1.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_credentials=False,allow_methods=['GET','POST'],allow_headers=['*'])

class Analysis(BaseModel):
    id:str
    filename:str
    duration_s:float
    fps:float
    width:int
    height:int
    frames:int
    motion:list[dict]
    model_status:str='not_integrated'
    activity_predictions:list=[]
    sop_status:str='not_evaluated'
    warning:str='Motion score is optical frame difference, NOT an AI activity prediction or SOP violation result.'

@app.get('/api/health')
def health():
    ckpt=ROOT/'models'/'best_finetuned_layer4_fc.pt'
    recipe=ROOT/'models'/'inference_recipe.json'
    return {'status':'ok','service':'VisualSOP Checker','model_checkpoint_present':ckpt.exists(),
            'inference_recipe_present':recipe.exists(),'model_inference_enabled':False,
            'note':'R3D-18 inference requires matching V6 preprocessing and class mapping. No fabricated predictions.'}

@app.post('/api/analyze',response_model=Analysis)
async def analyze(file:Annotated[UploadFile,File(description='Video to inspect')]):
    name=Path(file.filename or 'upload').name
    ext=Path(name).suffix.lower()
    if ext not in ALLOW:raise HTTPException(415,'Supported: MP4, MOV, AVI, MKV, WEBM')
    job=uuid.uuid4().hex
    directory=STORE/job
    directory.mkdir(parents=True,exist_ok=False)
    video_path=directory/('source'+ext)
    size=0
    try:
        with video_path.open('wb') as out:
            while chunk:=await file.read(1024*1024):
                size+=len(chunk)
                if size>MAX_MB*1024*1024:raise HTTPException(413,f'Video exceeds {MAX_MB}MB limit')
                out.write(chunk)
        if size==0:raise HTTPException(400,'Empty video')
        cap=cv2.VideoCapture(str(video_path))
        if not cap.isOpened():raise HTTPException(422,'Could not decode video')
        try:
            fps=float(cap.get(cv2.CAP_PROP_FPS))
            n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if fps<=0 or fps>240 or n<=0 or w<=0 or h<=0:raise HTTPException(422,'Invalid video metadata')
            if n/fps>60*30:raise HTTPException(413,'Maximum 30 minutes per video')
            # Sparse deterministic sampling: 2 frames/sec, capped at 600 frames.
            step=max(1,int(round(fps/2)),int(np.ceil(n/600)))
            samples=[];previous=None;index=0
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            while index<n:
                cap.set(cv2.CAP_PROP_POS_FRAMES,index)
                ok,frame=cap.read()
                if not ok:break
                small=cv2.resize(frame,(160,90),interpolation=cv2.INTER_AREA)
                gray=cv2.cvtColor(small,cv2.COLOR_BGR2GRAY)
                diff=float(np.mean(cv2.absdiff(gray,previous))/255) if previous is not None else 0.
                samples.append({'time_s':round(index/fps,2),'motion':round(diff,4)})
                if len(samples)==1:
                    cv2.imwrite(str(directory/'preview.jpg'),small)
                previous=gray
                index+=step
            if not samples:raise HTTPException(422,'No readable frames')
        finally:cap.release()
        result=Analysis(id=job,filename=name,duration_s=round(n/fps,2),fps=round(fps,2),width=w,height=h,frames=n,motion=samples)
        (directory/'result.json').write_text(result.model_dump_json(indent=2),encoding='utf8')
        return result
    except Exception:
        shutil.rmtree(directory,ignore_errors=True)
        raise
    finally:await file.close()

@app.get('/api/analyses/{job_id}',response_model=Analysis)
def get_analysis(job_id:str):
    if not job_id.isalnum():raise HTTPException(400,'Invalid ID')
    p=STORE/job_id/'result.json'
    if not p.is_file():raise HTTPException(404,'Not found')
    return json.loads(p.read_text(encoding='utf8'))

@app.get('/api/analyses/{job_id}/preview')
def preview(job_id:str):
    if not job_id.isalnum():raise HTTPException(400,'Invalid ID')
    p=STORE/job_id/'preview.jpg'
    if not p.is_file():raise HTTPException(404,'Not found')
    return FileResponse(p,media_type='image/jpeg')
