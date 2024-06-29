from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import models
from schemas import data
from crud.equipment import get_equipment_location_map, create_equipment_data, get_equipment_data
from utils.database import get_db
from services import dataService

equipment = APIRouter()

# 请求设备数据函数
@equipment.get('/get_equipment', response_model=List[data.EquipmentOut])
async def equipment_request(request: Request, equipment_id: str, equipment_type: str | None = None, db: Session = Depends(get_db)):
    return get_equipment_data(db, equipment_id, equipment_type)

# 创建设备数据函数
@equipment.post('/create_equipment', response_model=data.EquipmentUploadOut)
async def equipment_upload(request: Request, equipment_data: data.EquipmentUploadIn, db: Session = Depends(get_db)):
    return create_equipment_data(db, equipment_data)

# 请求设备地理位置信息函数
# frontend--views/pages/hugedata--equipment_locations
@equipment.get('/get_equipment_locations', response_model=List[data.EquipmentLocationOut])
async def equipment_locations_request(request: Request, equipment_type: str, db: Session = Depends(get_db)):
    return get_equipment_location_map(db, equipment_type)
