# pyrefly: ignore [missing-import]
from sqlmodel import Session, select
from app.models.cart_item import CartItem, CartItemCreate

def add_to_cart(*, session: Session, cart_in: CartItemCreate, user_id: int) -> CartItem:
    db_item = CartItem.model_validate(cart_in, update={"user_id": user_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def get_cart(*, session: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[CartItem]:
    statement = select(CartItem).where(CartItem.user_id == user_id).offset(skip).limit(limit)
    return list(session.exec(statement).all())
