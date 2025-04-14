from fastapi import APIRouter, HTTPException
from business import Business, CreateBusinessModel, UpdateBusinessModel
from dependencies import SessionDep

router = APIRouter(prefix="/businesses", tags=["businesses"])


@router.get("/")
def get_businesses(session: SessionDep):
    businesses = session.query(Business).all()
    return businesses


@router.get("/{id}")
def get_business(id: int, session: SessionDep):
    business = session.query(Business).filter(Business.id == id).first
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.post("/")
def create_business(create_business: CreateBusinessModel, session: SessionDep):
    business = Business(**create_business.model_dump())
    session.add(business)
    session.commit()
    session.refresh(business)
    return business


@router.put("/{id}")
def update_business(id: int, business: UpdateBusinessModel, session: SessionDep):
    business_to_update = session.query(Business).filter(Business.id == id).first()
    print("entro a update")
    if not business_to_update:
        raise HTTPException(status_code=404, detail="Business not found")

    update_data = business.model_dump(exclude_unset=True)
    print("update_data", update_data)

    # Update the model attributes
    for key, value in update_data.items():
        setattr(business_to_update, key, value)

    session.commit()
    session.refresh(business_to_update)
    return business_to_update


@router.delete("/{id}")
def delete_business(id: int, session: SessionDep):
    business_to_delete = session.query(Business).filter(Business.id == id).first()
    if not business_to_delete:
        raise HTTPException(status_code=404, detail="Business not found")
    session.delete(business_to_delete)
    session.commit()
    return {"message": "Business deleted successfully"}
