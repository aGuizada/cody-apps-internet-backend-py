from typing import Any
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep, CurrentUser
from app.models.cart_item import CartItemPublic, CartItemCreate, CartItemWithProduct
from app.services import cart_service

router = APIRouter()

@router.post("/", response_model=CartItemPublic)
def add_to_cart(*, session: SessionDep, current_user: CurrentUser, cart_in: CartItemCreate) -> Any:
    return cart_service.add_to_cart(
        session=session, 
        cart_in=cart_in, 
        user_id=current_user.id
    )

@router.get("/", response_model=list[CartItemWithProduct])
def read_cart(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    return cart_service.get_cart(
        session=session,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

@router.delete("/{item_id}")
def delete_cart_item(*, session: SessionDep, current_user: CurrentUser, item_id: int) -> Any:
    removed = cart_service.remove_from_cart(
        session=session,
        item_id=item_id,
        user_id=current_user.id
    )
    if not removed:
        raise HTTPException(status_code=404, detail="Item de carrito no encontrado")
    return {"detail": "Item eliminado del carrito"}