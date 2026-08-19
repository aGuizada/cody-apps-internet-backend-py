from typing import Optional
# pyrefly: ignore [missing-import]
from sqlmodel import Field, SQLModel

class CartItemBase(SQLModel):
    quantity: int = Field(default=1, ge=0)

class CartItem(CartItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")

class CartItemCreate(CartItemBase):
    product_id: int

class CartItemPublic(CartItemBase):
    id: int
    user_id: int
    product_id: int

class CartItemWithProduct(CartItemPublic):
    title: Optional[str] = None
    price: Optional[float] = None
    product_stock: Optional[int] = None