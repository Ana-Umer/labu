# models.py
from typing import Optional, List
from sqlmodel import SQLModel, Field

class CarPlateBase(SQLModel ,table=True):
    plate: str
    owner_name: Optional[str] = None
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    year: Optional[int] = None
    id: Optional[int] = Field(default=None, primary_key=True)

class CarPlate(CarPlateBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# class CarPlateCreate(CarPlateBase):
#     pass

class CarPlateUpdate(SQLModel):
    plate: Optional[str] = None
    owner_name: Optional[str] = None
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    year: Optional[int] = None

