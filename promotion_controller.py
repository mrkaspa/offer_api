from fastapi import APIRouter, HTTPException
from promotion import CreatePromotionModel, UpdatePromotionModel, Promotion
from dependencies import SessionDep

router = APIRouter(prefix="/promotions", tags=["promotions"])


@router.get("/{slug}")
def get_promotion_by_slug(slug: str, session: SessionDep):
    promotion = session.query(Promotion).filter(Promotion.slug == slug).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotion


@router.get("/")
def get_promotions(session: SessionDep):
    promotions = session.query(Promotion).all()
    return promotions


@router.put("/{slug}")
def update_promotion(slug: str, promotion: UpdatePromotionModel, session: SessionDep):
    promotion_to_update = (
        session.query(Promotion).filter(Promotion.slug == slug).first()
    )
    if not promotion_to_update:
        raise HTTPException(status_code=404, detail="Promotion not found")

    # Get only the fields that were provided in the request
    update_data = promotion.model_dump(exclude_unset=True)

    # Update the model attributes
    for key, value in update_data.items():
        setattr(promotion_to_update, key, value)

    session.commit()
    session.refresh(promotion_to_update)
    return promotion_to_update


@router.post("/")
def create_promotion(promotion: CreatePromotionModel, session: SessionDep):
    # Create the promotion without setting the slug yet
    promotion_data = promotion.model_dump()
    promotion_data.pop("slug", None)  # Remove slug if present
    promotion_orm = Promotion(**promotion_data)

    # Add to session and commit
    session.add(promotion_orm)
    session.commit()

    # Refresh to get the updated slug
    session.refresh(promotion_orm)

    return promotion_orm


@router.delete("/{slug}")
def delete_promotion(slug: str, session: SessionDep):
    promotion = session.query(Promotion).filter(Promotion.slug == slug).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    session.delete(promotion)
    session.commit()
    return {"message": "Promotion deleted successfully"}
