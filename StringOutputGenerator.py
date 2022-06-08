from cmath import sin
from RecipeParserClass import RecipeParser
from DataParsingUtilities import *
import json

def create_string_from_recipe(parsed_recipe, isTransformed=False):
    ingredients = parsed_recipe["ingredients"]
    steps = parsed_recipe["steps"]
    tools = parsed_recipe["tools"]
    title = parsed_recipe["title"]
    methods = parsed_recipe["methods"].keys()
    primary_method = parsed_recipe["primary_method"]
    data = FoodDataClass()


    #Format strings
    single_line = "-------------------------------------------------------------------------------------\n"
    single_small_line = "--------------------------------------------\n"


    #Starting lines
    output_string = single_line +single_line+single_line

    #TITLE
    output_string += "\nTITLE: " + title

    #URL
    output_string += "\nURL: " + parsed_recipe["url"] + '\n' + \
                    single_line

    #IS TRANSFORMED
    if not isTransformed:
        output_string += "ORIGINAL\n"
    else:
        output_string += "TRANSFORMED\n"

    #INGREDIANTS           
    output_string += "\n\nINGREDIENTS\n" + \
                    "--------------------------------------------\n"

    for i in range(len(ingredients)):
        ingredient = ingredients[i]
        output_string += str(i+1) + ". " + ingredient["name"] + \
                        "\nAmount: " + str(ingredient["quantity"]) + " " + ingredient["measurement"] +'\n'

    output_string += single_small_line + single_small_line

    #TOOLS
    output_string +="\nTOOLS: \n"
    output_string += "--------------------------------------------\n"
    
    i = 1
    for tool in tools:
        output_string += str(i) + ". " + tool + '\n'
        i+=1

    output_string += single_small_line + single_small_line
    
    #METHODS
    output_string +="\nPRIMARY METHOD -> " + data.method_converter[primary_method] + "\n"
    output_string +="ALL METHODS: \n"
    output_string += "--------------------------------------------\n"
    
    i = 1
    for method in methods:
        output_string += str(i) + ". " + data.method_converter[method] + '\n'
        i+=1

    output_string += single_small_line + single_small_line

    #STEPS
    output_string +="\nSTEPS: \n"
    output_string += "--------------------------------------------\n"

    for i in range(len(steps)):
        step = steps[i]
        output_string += "\n" + str(i+1) + ". " + step

    
    output_string += '\n\n' + single_line + single_line + single_line

    if isTransformed:
        with open("transformed_recipe.txt", 'w') as f:
            f.write(output_string)
    else:
        with open("original_recipe.txt", 'w') as f:
            f.write(output_string)
    return output_string