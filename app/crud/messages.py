from sqlalchemy.orm import Session
from typing import List
from models.models import Message
from fastapi import HTTPException

def get_all_messages(db: Session) -> List[Message]:
    return db.query(Message).all()

def mark_as_read(db: Session, message_id: int) -> Message:
    message = db.query(Message).filter(Message.msg_id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    message.status = 'read'
    db.commit()
    db.refresh(message)
    return message

def mark_as_deleted(db: Session, message_id: int) -> Message:
    message = db.query(Message).filter(Message.msg_id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    message.status = 'deleted'
    db.commit()
    db.refresh(message)
    return message

def restore_message(db: Session, message_id: int) -> Message:
    message = db.query(Message).filter(Message.msg_id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    message.status = 'read'
    db.commit()
    db.refresh(message)
    return message

def mark_all_as_read(db: Session):
    messages = db.query(Message).filter(Message.status == 'unread').all()
    for message in messages:
        message.status = 'read'
    db.commit()

def delete_all_read(db: Session):
    messages = db.query(Message).filter(Message.status == 'read').all()
    for message in messages:
        message.status = 'deleted'
    db.commit()

def clear_recycle_bin(db: Session):
    db.query(Message).filter(Message.status == 'deleted').delete()
    db.commit()