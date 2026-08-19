# pyrefly: ignore [missing-import]
from sqlmodel import Session, select
from app.models.cart_item import CartItem, CartItemCreate, CartItemWithProduct
from app.models.product import Product

def add_to_cart(*, session: Session, cart_in: CartItemCreate, user_id: int) -> CartItem:
    statement = select(CartItem).where(
        CartItem.user_id == user_id,
        CartItem.product_id == cart_in.product_id
    )
    db_item = session.exec(statement).first()
    if db_item:
        db_item.quantity += cart_in.quantity
        if db_item.quantity <= 0:
            item_id = db_item.id
            session.delete(db_item)
            session.commit()
            return CartItem(id=item_id, user_id=user_id, product_id=db_item.product_id, quantity=0)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item

    db_item = CartItem.model_validate(cart_in, update={"user_id": user_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def get_cart(*, session: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[CartItemWithProduct]:
    statement = (
        select(CartItem, Product)
        .join(Product, Product.id == CartItem.product_id)
        .where(CartItem.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    result = []
    for cart_item, product in session.exec(statement).all():
        result.append(CartItemWithProduct(
            id=cart_item.id,
            user_id=cart_item.user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            title=product.title,
            price=product.price,
            product_stock=product.stock
        ))
    return result

def remove_from_cart(*, session: Session, item_id: int, user_id: int) -> bool:
    statement = select(CartItem).where(
        CartItem.id == item_id,
        CartItem.user_id == user_id
    )
    db_item = session.exec(statement).first()
    if not db_item:
        return False
    session.delete(db_item)
    session.commit()
    return True