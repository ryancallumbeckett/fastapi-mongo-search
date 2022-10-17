
from ast import keyword
import sys
sys.path.append("..")
from config import settings
from pymongo import MongoClient


client = MongoClient(settings.mongo_url)
db = client.recipes


def advanced_search(table, limit, **kwargs):

    must_list = []
    should_list = []
    query_count = 0

    for query_type, values in kwargs.items():
        if query_type.lower() == "keywords":
            query_count += 1
            includes_search = True
            query = {
                    "text": {
                        "query": values,
                        "path": "recipe_name",
                        "fuzzy": {}
                    }, 
                }

            must_list.append(query)

        elif query_type.lower() == "ingredients":
            query_count += 1
            ingredients = values.split(",")
            for ingredient in ingredients:
                ingredient = ingredient.replace(" ", "_")
                should_list.append({
                        "exists": {
                            "path": f"ingredients_map.{ingredient.strip()}"
                            }
                        })
        
        elif query_type.lower() == "nutrition":
            query_count += 1
            for nutr in values:
                must_list.append(nutr)

        else:
            print(f"{query_type} is not a valid argument. Valid arguments are: Keywords, Ingredients, Nutrition")



    if query_count >= 2 and includes_search:
        result = table.aggregate([
            {
                "$search": {
                    "index" : "recipe_index", 
                    "compound": {
                        "must": must_list,
                        "should": should_list
                    }   
                }
            }, 
            {
            '$limit': limit
            },
            {
                "$project": {
                "_id": 0,
                "recipe_name": 1,
                "protein_per_serving_grams": 1,
                "calories_per_serving": 1,
                "recipe_link": 1
                }
            }
            ])
    else:
        must_list = must_list if len(must_list) > 0 else should_list
        result = table.aggregate([
            {
                "$search": {
                    "index" : "recipe_index", 
                    "compound": {
                        "must": must_list  
                    }   
                }
            }, 
            {
            '$limit': limit
            },
            {
                "$project": {
                "_id": 0,
                "recipe_name": 1,
                "protein_per_serving_grams": 1,
                "calories_per_serving": 1,
                "recipe_link": 1
                }
            }
            ])

    return result




def keyword_search(search_query, table, field, limit):

        result = table.aggregate([
            {
                "$search": {
                    "index" : "recipe_index", 
                    "text": {
                        "query": search_query,
                        "path":  field,
                        "fuzzy": {}
                    }   
                }
            }, {
            '$limit': limit
            }
        ])


        return result



def ingredient_search(ingredients, table, limit):

    ingredient_list = ingredients.split(',')
    query_list = []
    for ingredient in ingredient_list:
        ingredient = ingredient.replace(" ", "_")
        query = {
                "exists": {
                    "path": f"ingredients_map.{ingredient.strip()}"
                    },
                }

        query_list.append(query)

    result = table.aggregate([
        {
            "$search": {
                "index" : "recipe_index", 
                "compound": {
                    "must": query_list  
                }   
            }
        }, 
        {
        '$limit': limit
        }
    ])


    return result



def nutrition_search(nutrition_list, table, limit):


    result = table.aggregate([
        
        {
            "$search": {
                "index" : "recipe_index", 
                "compound": {
                    "must": nutrition_list
                }   
            }
        }, 
        {
        '$limit': limit
        }
    ])


    return result









