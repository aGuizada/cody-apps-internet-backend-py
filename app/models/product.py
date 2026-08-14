from typing import Optional
# pyrefly: ignore [missing-import]
from sqlmodel import Field, SQLModel

class ProductBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)
    price: float
    stock: int = Field(default=0)
    category_id: int = Field(foreign_key="category.id")

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ProductCreate(ProductBase):
    pass
    
class ProductPublic(ProductBase):
    id: int
    
class ProductUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
