from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from services import messages as messages_service
from slowapi import Limiter
from slowapi.util import get_remote_address
from schemas import schemas
from schemas.schemas import MessageOut
from utils.database import get_db
from models.models import Message
from typing import List


# 获取请求的远程地址
limiter = Limiter(key_func=get_remote_address)

# 创建路由实例
messages = APIRouter()


@messages.get('/messages', response_model=List[MessageOut])
@limiter.limit("30/minute")
async def get_messages(request: Request, db: Session = Depends(get_db)):
    return messages_service.get_all_messages(db)

@messages.post('/messages/{message_id}/read', response_model=MessageOut)
@limiter.limit("30/minute")
async def mark_as_read(request: Request, message_id: int, db: Session = Depends(get_db)):
    return messages_service.mark_message_as_read(db, message_id)

@messages.post('/messages/{message_id}/delete', response_model=MessageOut)
@limiter.limit("30/minute")
async def restore_message(request: Request, message_id: int, db: Session = Depends(get_db)):
    return messages_service.mark_message_as_deleted(db, message_id)

@messages.post('/messages/{message_id}/restore', response_model=MessageOut)
@limiter.limit("30/minute")
async def restore_message(request: Request, message_id: int, db: Session = Depends(get_db)):
    return messages_service.restore_message(db, message_id)

@messages.post('/messages/markAllAsRead', response_model=dict)
@limiter.limit("30/minute")
async def mark_all_as_read(request: Request, db: Session = Depends(get_db)):
    messages_service.mark_all_messages_as_read(db)
    return {"status": "success"}

@messages.post('/messages/deleteAll', response_model=dict)
@limiter.limit("30/minute")
async def delete_all_read(request: Request, db: Session = Depends(get_db)):
    messages_service.delete_all_read_messages(db)
    return {"status": "success"}

@messages.post('/messages/clearRecycleBin', response_model=dict)
@limiter.limit("30/minute")
async def clear_recycle_bin(request: Request, db: Session = Depends(get_db)):
    messages_service.clear_recycle_bin(db)
    return {"status": "success"}