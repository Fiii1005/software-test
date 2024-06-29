from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from schemas import schemas, data
from utils.database import get_db
import config
import openai
import cv2
import os, shutil
from ultralytics import YOLO
from loguru import logger
from fastapi.responses import FileResponse
from services import importdata

openai.api_base = "https://apikeyplus.com/v1"
openai.api_key = config.API_KEY

# 获取请求的远程地址
limiter = Limiter(key_func=get_remote_address)

# 创建路由实例
agent = APIRouter()

# 创建模型实例
model = YOLO("yolov10n.pt")   
if not os.path.exists("temp_images"):
    os.makedirs("temp_images")

# 定义chatgpt接口
@agent.post('/chat', response_model=schemas.ChatInfo)
# 限制10分钟最多被访问10次
@limiter.limit("10/10minutes")
async def chat(
    request: Request, 
    chat: schemas.ChatCreate,
    db: Session = Depends(get_db)
):
    try:
        response = openai.ChatCompletion.create(
            model = config.LLM_MODEL,
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": chat.prompt}
            ]
        )
        reply = response['choices'][0]['message']['content']
        print(reply)
        return schemas.ChatInfo(message=reply, status='success')
    except Exception as e:
        print('Error:', e)
        return schemas.ChatInfo(message=str(e), status='failed')


@agent.post("/identify_fish")
@limiter.limit("10/10minutes")
async def identify_fish(
    request: Request, 
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
         # 1. 缓存接收到的图片为文件
        image_path = f"temp_images/{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        # 2. 使用模型处理图片 
        results = model.predict(image_path, save=True, name=f'/temp/{image.filename}')
        
        # 3. 返回处理后的图片并删除模型保存的图片
        resp = FileResponse(os.path.join('C:\\Users\\10141\\Documents\\Fi\\2024Spring\\3-软件工程\\code\\now', image.filename), media_type='image/jpeg')
        return resp 
    
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
    
    
# 接收导入数据

@agent.post("/import_data")
@limiter.limit("10/10minutes")
async def import_data(
    request: Request, 
    datafile: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
         # 1. 缓存接收到的数据文件

         # 先得到当前文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # app文件夹
        current_dir=os.path.dirname(current_dir)
        # 项目根目录
        current_dir=os.path.dirname(current_dir)
        file_path = os.path.join(current_dir, 'temp_file', datafile.filename)
        # 如果这个文件不存在，先创建这个文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(datafile.file, buffer)
        
        # 2. 调用接口将数据导入数据库
        res = importdata.import_data(db, file_path)

        # 3. 删除缓存的数据文件
        os.remove(file_path)
        return res

    
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
    