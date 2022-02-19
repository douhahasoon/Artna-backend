import datetime
from typing import List

from ninja import Schema
from pydantic import UUID4
from ninja import ModelSchema
from ninja.orm import create_schema


class UUIDSchema(Schema):
    id: UUID4

class MessageOut(Schema):
    detail: str


class CategoryOut(Schema):
    id: UUID4
    name: str
    description: str
    image: str

class LabelOut(Schema):
    id: UUID4
    name: str



class ArtistOut(Schema):
    id: UUID4
    name: str
    image: str


class ProductImage(Schema):
    image:str
    is_default_image:bool



class ProductOut(Schema):
    id: UUID4
    is_featured: bool
    name: str
    description: str
    qty: int
    price: int
    discounted_price: int
    category: CategoryOut
    artist: ArtistOut
    label: LabelOut
    images: List[ProductImage]


class CitySchema(Schema):
    name: str


class CitiesOut(CitySchema, UUIDSchema):
    pass


class ItemSchema(Schema):
    # user:
    product: ProductOut
    item_qty: int
    ordered: bool


class ItemCreate(Schema):
    product_id: UUID4
    item_qty: int


class ItemOut(UUIDSchema, ItemSchema):
    pass


##---------------------

class AddressSchema(Schema):

    address1: str
  


class  Add_address(Schema):
    work_address: bool
    address1: str
    address2: str
    city: UUID4
    phone: str



class AddressOut(AddressSchema, UUIDSchema):
    pass



class OrderSchema(Schema):
    address:UUID4