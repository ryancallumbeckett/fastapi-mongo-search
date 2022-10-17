
from cmath import rect
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from enum import Enum


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class RecipeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    recipe_name: str = Field(...)
    recipe_link: str = Field(...)
    recipe_image: str = Field(...)
    recipe_time: Optional[int]
    recipe_servings: Optional[int] 


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "recipe_name": "Sweet and sour tofu",
                "recipe_link": "https://example-website.co.uk/recipes/recipe-1",
                "recipe_image": "https://example-image.com/image1.png",
                "recipe_time": "30",
                "recipe_servings": "2",
                "ingredients": "tofu, sweet and sour sauce",
                "method": "cook tofu, add sweet and sour sauce",
                "cuisine": "Asian"
            }
        }


class QuantityOperator(str, Enum):
    gte = "gte"
    lte = "lte"


