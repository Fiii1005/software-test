from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from schemas import data
from crud import importdata as crud

def import_data(db: Session, filepath: str)-> str:
    """
    从文件中导入数据到数据库中
    参数：
    db：数据库操作
    filepath：文件路径
    返回值：
    str：导入结果
    """
    # 实际的数据库操作
    res = crud.upload_import_data(db, filepath)

    return res
