from schemas import data
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from utils.database import get_db
from typing import List
from services import dataService

# 获取请求的远程地址
limiter = Limiter(key_func=get_remote_address)

# 实例化新的FastAPI路由器
dataRequest = APIRouter()


# 请求水体物理数据函数
@dataRequest.post('/get_water_physic', response_model=List[data.waterPhysicOut])
@limiter.limit("10/10minutes")
async def waterPhysic_request(request: Request,
                              waterPhysicR: data.waterPhysicIn,
                              db: Session = Depends(get_db)):
    return dataService.search_water_physic_data(db,waterPhysicR)

# 上传水体物理数据函数
@dataRequest.post('/upload_water_physic', response_model=data.waterPhysicUploadOut)
@limiter.limit("10/10minutes")
async def waterPhysic_upload(request: Request,
                             waterPhysicU: data.waterPhysicUploadIn,
                             db: Session = Depends(get_db)):
    return dataService.upload_water_physic_data(db,waterPhysicU)

# 请求水体化学数据函数
@dataRequest.post('/get_water_chemistry', response_model=List[data.waterChemistryOut])
@limiter.limit("10/10minutes")
async def waterChemistry_request(request: Request,
                                 waterChemistryR: data.waterChemistryIn,
                                 db: Session = Depends(get_db)):
    return dataService.search_water_chemistry_data(db,waterChemistryR)

# frontend--views/pages/farmer-manage--ranks
@dataRequest.get('/ranks', response_model=List)
@limiter.limit("10/10minutes")
async def ranks_request(request: Request,db: Session=Depends(get_db)):
    return dataService.search_ranks(db)

# frontend--views/pages/farmer-manage--fishnumber
@dataRequest.get('/fishnumber',response_model=data.fishnumberOut)
#@limiter.limit("10/10minutes")
async def fishnumber_request(request: Request,fishType: str = Query(..., description="The type of the fish"), db: Session=Depends(get_db)):
    return dataService.search_fishnumber(db, fishType)

# frontend--views/pages/farmer-manage--chart-data
@dataRequest.get('/chart-data',response_model=data.fish_chartdataOut)
#@limiter.limit("10/10minutes")
async def chart_data_request(
    request: Request,
    type: str = Query(..., description="The type of the chart data"),
    fishType: str = Query(..., description="The type of the fish"),
    placeType: str = Query(..., description="The type of the place"),
    db: Session = Depends(get_db)
):
    fish_chartdata = data.fish_chartdataIn(type=type, fishtype=fishType, placetype=placeType)
    return dataService.search_fish_chartdata(db,fish_chartdata)

# frontend--views/pages/dashboard--dashOpt1
@dataRequest.get('/dashOpt1',response_model=data.dashOpt1Out)
async def dash_opt1_request(request: Request,db: Session = Depends(get_db)):
    return dataService.search_fish_daynumber(db)

# frontend--views/pages/dashboard--dashOpt2
@dataRequest.get('/dashOpt2',response_model=data.dashOpt2Out)
async def dash_opt2_request(request: Request,db: Session = Depends(get_db)):
    return dataService.search_dashOpt2(db)