from sqlalchemy.orm import Session
from sqlalchemy import extract, func, asc
from typing import List
from schemas import data
from models import models
from fastapi import HTTPException
from datetime import datetime
import pandas as pd

def upload_import_data(db: Session, filepath: str)-> str:
    # 读取CSV文件
    df = pd.read_csv(filepath, encoding='utf-8')

    # 遍历CSV数据，并将每一行添加到数据库
    for index, row in df.iterrows():
        # 解析日期
        year = int(row['年'])
        month = int(row['月'])
        day = int(row['日'])

        # 解析鱼类名称
        fish_name = row['鱼']

        # 解析长度范围和体重范围
        length_range = row['范围（长度cm）']
        weight_range = row['范围（重量kg）']

        # 解析数量
        num = int(row['数量'])

        # 将数据添加到数据库
        new_fish_data = models.fish(
            date=datetime(year, month, day),
            fishname=fish_name,
            lengthrange=length_range,
            weightrange=weight_range,
            num=num
        )
        try:
            db.add(new_fish_data)
            # 提交更改
            db.commit()
            return "Fish data uploaded successfully!"
        except Exception as e:
            return str(e)
        