from mongo_utils import keyword_search, ingredient_search, nutrition_search, advanced_search
from bson.objectid import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import RecipeModel, QuantityOperator
from typing import Optional
from db import db



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/", response_description="List recipes", response_model=list[RecipeModel])
async def list_recipes():
    recipes = list(db.all_recipes.find().limit(12))
    return recipes



@app.get("/search_by_keyword/", response_description="Search by recipe name", response_model=list[RecipeModel])
async def search_recipe_by_name(query: str):
    recipe = keyword_search(query, db.all_recipes, "recipe_name", 5)
    if recipe is not None:
        return list(recipe)
    raise HTTPException(status_code=404, detail=f"No results for {query} found")



@app.get("/search_by_ingredients/", response_description="Search by ingredients", response_model=list[RecipeModel])
async def search_recipe_by_ingredients(ingredients: str):
    recipe = ingredient_search(ingredients, db.all_recipes, 5)
    if recipe is not None:
        return list(recipe)
    raise HTTPException(status_code=404, detail=f"No results for {ingredients} found")



@app.get("/search_by_nutrition/", response_description="Search by nutrition", response_model=list[RecipeModel])
async def search_by_macronutrients(protein_operator: QuantityOperator = QuantityOperator.gte, protein_quantity: Optional[float] = 0.0,
                                carbs_operator: QuantityOperator = QuantityOperator.gte, carbs_quantity: Optional[float] = 0.0, 
                                fat_operator: QuantityOperator = QuantityOperator.gte, fat_quantity: Optional[float] = 0.0, 
                                limit: Optional[int] = 5):
              
    nutrition_list = [
            {
                "range": {
                    "path": "protein_per_serving_grams",
                    protein_operator.value: protein_quantity,
                    }
            }, 
            {
                "range": {
                    "path": "carbs_per_serving_grams",
                    carbs_operator.value: carbs_quantity,
                    }
            }, 
            {
                "range": {
                    "path": "fat_per_serving_grams",
                    fat_operator.value: fat_quantity,
                    }
            } 
        ]
    

    recipe = nutrition_search(nutrition_list, db.all_recipes, 5)
    if recipe is not None:
        return list(recipe)
    raise HTTPException(status_code=404, detail=f"No results found")


@app.get("/advanced_search/", response_description="Advanced recipe search")
async def advanced_recipe_search(query: str, ingredients: str, protein_operator: QuantityOperator = QuantityOperator.gte, protein_quantity: Optional[float] = 0.0,
                                carbs_operator: QuantityOperator = QuantityOperator.gte, carbs_quantity: Optional[float] = 0.0, 
                                fat_operator: QuantityOperator = QuantityOperator.gte, fat_quantity: Optional[float] = 0.0, 
                                limit: Optional[int] = 5):
              
    nutrition_list = [
            {
                "range": {
                    "path": "protein_per_serving_grams",
                    protein_operator.value: protein_quantity,
                    }
            }, 
            {
                "range": {
                    "path": "carbs_per_serving_grams",
                    carbs_operator.value: carbs_quantity,
                    }
            }, 
            {
                "range": {
                    "path": "fat_per_serving_grams",
                    fat_operator.value: fat_quantity,
                    }
            } 
        ]
    

    recipe = advanced_search(db.all_recipes, limit, keywords=query, ingredients=ingredients, nutrition=nutrition_list)
    if recipe is not None:
        return list(recipe)
    raise HTTPException(status_code=404, detail=f"No results found")





@app.get("/{id}", response_description="Get a single recipe by ID", response_model=RecipeModel)
async def get_recipe_by_id(id: str):
    recipe = db.all_recipes.find_one({"_id": ObjectId(id)})
    if recipe is not None:
        return recipe
    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")

