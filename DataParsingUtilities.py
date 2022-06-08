
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
def get_ingredients(soup=None) -> List[str]:

    ingredient_elements = soup.find_all("span", class_="ingredients-item-name elementFont__body")

    ingredients = []

    for ingred in ingredient_elements:
        ingred_text = ingred.text
        ingred_text = ingred_text.replace("\u2009" , "")
        ingredient_name = ingred_text

        ingredient_quantity, ingredient_unit = get_quantity_measurement(ingred_text)

        #if we have a quantity, cut off the measurement and units
        if ingredient_quantity > 0:
            split_ingred = ingred_text.split(" ")
            ingredient_name = ""
            for word in split_ingred[1::]:
                if word not in FoodDataClass().measurements and "(" not in word and ")" not in word:
                    ingredient_name += word + " "
            ingredient_name = ingredient_name.rstrip()
        else:
            ingredient_quantity = "To Taste"
            ingredient_unit = ""

        ingredient = {
            "name": ingredient_name,
            "quantity" : ingredient_quantity,
            "measurement": ingredient_unit
            }
        ingredients.append(ingredient)

    return ingredients

# Given a url, returns a list of steps as they appear on the page
def get_steps(soup=None) -> List[str]:
    step_elemets = soup.find_all("li", class_="subcontainer instructions-section-item")

    steps = []
    for step in step_elemets:
        paragraph = step.find("div", class_="paragraph")
        paragraph_element = paragraph.find("p")
        steps.append(paragraph_element.text)

    return steps

#Given a url, returns the title of the recipe
def get_title(soup=None) -> str:
    title = soup.find("title")

    title = title.text

    title = title.split(' | Allrecipes')

    return title[0]

# Helper function for get_ingredients, finds the quantity for an ingredient
def get_quantity_measurement(ingrediant_str):
    split_str = re.split(' ', ingrediant_str)

    quantity = split_str[0]
    try:
        quantity = sum([round(unicodedata.numeric(val), 2) for val in quantity]) # converts unicode to a float
    except:
        quantity =  "FAILED"
    if split_str[1] in FoodDataClass().measurements:
        measurement = split_str[1]
    else:
        measurement = ""
        for word in split_str[1:]:
            measurement += word + " "
            if ")" in word:
                measurement.rstrip()
                break

    return quantity, measurement

# Getting the tools of cooking 
# give it a list of steps and it will return a set of tools
def get_tools(steps):
    data_class = FoodDataClass()
    tools = set()
    for step in steps:
        split_step = re.split(r'[ .,\'()]', step)
        for word in split_step:
            if word.lower() in data_class.tools:
                tools.add(word)
    
    return tools

# Getting the methods of cooking given a list of steps object
# it will return a set of methods used in the process
def get_methods(steps):
    methods = {}

    for step in steps:
        for word in re.split(r'[ .,\']',step):
            if word.lower() in FoodDataClass().methods:
                methods[word.lower()] = methods.get(word, 0) + 1
    return methods


if __name__ == "__main__":
    ingredients = get_ingredients(url="https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/")
    steps = get_steps(url = "https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/")
    tools = get_tools(steps)