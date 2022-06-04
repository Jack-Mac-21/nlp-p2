from cmath import sin
from RecipeParserClass import RecipeParser
from DataParsingUtilities import *
import json

def create_string_from_recipe(parsed_recipe):
    ingredients = parsed_recipe["ingredients"]
    print(ingredients)
    steps = parsed_recipe["steps"]

    single_line = "-------------------------------------------------------------------------------------\n"
    output_string = single_line +single_line+single_line
    output_string += "\nURL: " + parsed_recipe["url"] + '\n' + \
                    single_line + \
                    "\n\nINGREDIENTS\n" + \
                    "--------------------------------------------\n"

    for i in range(len(ingredients)):
        ingredient = ingredients[i]
        output_string += str(i+1) + ". " + ingredient["name"] + \
                        "\nAmount: " + str(ingredient["quantity"]) + " " + ingredient["measurement"] +'\n'

    output_string += single_line + single_line
    output_string +="\nSTEPS: \n"
    output_string += "--------------------------------------------\n"

    for i in range(len(steps)):
        step = steps[i]
        output_string += "\n" + str(i+1) + ". " + step

    output_string += '\n\n' + single_line + single_line + single_line
    return output_string