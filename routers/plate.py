from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select, Session
from database import SessionDep
from models import CarPlate,  CarPlateUpdate
from fastapi import Query, Depends
from database import get_session
from models import CarPlate, CarPlateBase
import re

router = APIRouter(prefix="/plates", tags=["Plates"])

# ------------------------------
# Ethiopian Plate Regex
# ------------------------------
PLATE_REGEX = re.compile(
    r"""^(
        # Private / Commercial: 1-A-12345 or 12-B-123456
        ([0-9]{1,2}-[A-Z]-[0-9]{1,6})
        |
        # Government: ET-12345
        (ET-[0-9]{3,6})
        |
        # Diplomatic: CD-12-123 or CD-03-1234
        (CD-[0-9]{1,2}-[0-9]{2,4})
    )$""",
    re.IGNORECASE | re.VERBOSE
)

def validate_plate(plate: str):
    """Validate Ethiopian plate format and raise HTTP error if invalid."""
    if not PLATE_REGEX.match(plate):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Ethiopian plate format: '{plate}'. "
                   "Examples: '1-A-12345', 'ET-12345', 'CD-12-123'"
        )
@router.post("/about", response_model=CarPlateBase)
def create_plate(payload: CarPlateBase, session: SessionDep):
    validate_plate(payload.plate)

    
    existing = session.exec(
        select(CarPlateBase).where(CarPlateBase.plate == payload.plate)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Plate already exists")

    # plate = CarPlate.from_orm(payload)
    session.add(payload)
    session.commit()
    session.refresh(payload)
    return payload


# router = APIRouter(prefix="/plates", tags=["Plates"])
@router.get("/me", response_model=list[CarPlateBase])
def get_all(session:SessionDep):
    plates=session.exec(select(CarPlateBase)).all()
    return plates

@router.get("/", response_model=list[CarPlateBase])
def list_plates(
    q: str | None = Query(None, description="search substring in plate"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session)
):
    # query = select(CarPlateBase)
    if q:  
       query = select(CarPlateBase).where(CarPlateBase.plate.like(f"%{q}%"))  
    results = session.exec(query.offset(offset).limit(limit)).all()
    return results

@router.get("/{plate_id}", response_model=CarPlate)
def get_plate(plate_id: int, session: SessionDep):
    plate = session.get(CarPlateBase, plate_id)
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")
    return plate


@router.patch("/{plate_id}", response_model=CarPlateBase)
def update_plate(plate_id: int, paylod: CarPlateUpdate, session: SessionDep):
    plat = session.get(CarPlateBase, plate_id)
    if not plat:
        raise HTTPException(status_code=404, detail="Plate not found")

   
    if paylod.plate is not None:
        validate_plate(paylod.plate)
       
        existing = session.exec(
            select(CarPlateBase).where(CarPlateBase.plate == paylod.plate, CarPlateBase.id != plate_id)
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Another record has that plate")

   
    update_data = paylod.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(plat, key, value)

    session.add(plat)
    session.commit()
    session.refresh(plat)
    return plat


@router.delete("/{plate_id}")
def delete_plate(plate_id: int, session: SessionDep):
    plate = session.get(CarPlateBase, plate_id)
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")
    session.delete(plate)
    session.commit()
    return {"message": f"Plate '{plate.plate}' deleted successfully"}




