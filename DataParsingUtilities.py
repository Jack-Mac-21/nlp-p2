
from posixpath import split
import requests
from bs4 import BeautifulSoup
from typing import List
import re
from fractions import Fraction
import unicodedata
from DataClassFile import FoodDataClass


# Given a url this function returns a list of ingredients as a dictionary
# [{"name", "quantity", "measurement"}, ... ]
def get_ingredients(url=None) -> List[str]:
    ingredients = []
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    ingredient_elements = soup.find_all("span", class_="ingredients-item-name elementFont__body")

    for ingred in ingredient_elements:
        ingred_text = ingred.text
        ingred_text = ingred_text.replace("\u2009" , "")
        ingredient_name = ingred_text
        ingredient_quantity, ingredient_unit = get_quantity_measurement(ingred_text)
        ingredients.append(ingred_text)
        ingredient = {
            "name": ingredient_name,
            "quantity" : ingredient_quantity,
            "measurement": ingredient_unit
            }
        ingredients.append(ingredient)

    return ingredients

# Given a url, returns a list of steps as they appear on the page
def get_steps(url=None) -> List[str]:
    steps = []
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    step_elemets = soup.find_all("li", class_="subcontainer instructions-section-item")

    for step in step_elemets:
        paragraph = step.find("div", class_="paragraph")
        paragraph_element = paragraph.find("p")
        steps.append(paragraph_element.text)

    return steps

# Helper function for get_ingredients, finds the quantity for an ingredient
def get_quantity_measurement(ingrediant_str):
    split_str = re.split(' ', ingrediant_str)

    quantity = split_str[0]
    try:
        quantity = sum([round(unicodedata.numeric(val), 2) for val in quantity]) # converts unicode to a float
    except:
        quantity =  "FAILED"
    measurement = split_str[1]

    return quantity, measurement


if __name__ == "__main__":
    ingredients = get_ingredients(url="https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/")
    steps = get_steps(url = "https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/")
    print(ingredients)
    print(steps)