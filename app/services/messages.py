from sqlalchemy.orm import Session
from typing import List
from models.models import Message
from crud import messages as crud

def get_all_messages(db: Session) -> List[Message]:
    return crud.get_all_messages(db)

def mark_message_as_read(db: Session, message_id: int) -> Message:
    return crud.mark_as_read(db, message_id)

def mark_message_as_deleted(db: Session, message_id: int) -> Message:
    return crud.mark_as_deleted(db, message_id)

def restore_message(db: Session, message_id: int) -> Message:
    return crud.restore_message(db, message_id)

def mark_all_messages_as_read(db: Session):
    crud.mark_all_as_read(db)

def delete_all_read_messages(db: Session):
    crud.delete_all_read(db)

def clear_recycle_bin(db: Session):
    crud.clear_recycle_bin(db)