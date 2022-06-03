# This file will run our program, just call it in the terminal and it will output the results in the output json
from RecipeParserClass import RecipeParser
from DataParsingUtilities import *
import json

# Pass in a URL and it will return a dictionar 
# {"ingredients": ingredients_dictionary, "steps" : list of steps, 
# "tools" : list of tools, *not implemented yet
# "methods": list of methods *not implemented yet
# "primary method": primary_method} #not implemented yet
def parse_recipe(url=None, transformation="None"):
    ingredients = get_ingredients(url)
    steps = get_steps(url)
    
    parsed_recipe = {"url" : url,
                     "ingredients" : ingredients,
                     "steps": steps,
                     "tools" : None,
                     "primary method": None,
                     "methods" : None,
                     "transformation" : transformation
                     }

    return parsed_recipe

# Takes a parsed recipe and creates a new parsed recipe with the transformation
def transform_parsed_recipe(parsed_recipe):

    transformation = parsed_recipe["transformation"]

    transformed_recipe = {}
    
    # Call your tranformation functions 
    if transformation == "vegetarian":
        transformed_recipe = transform_vegetarian(parsed_recipe)
    if transformation == "healthy":
        transformed_recipe = transform_healthy(parsed_recipe)
    if transformation == "unhealthy":
        transformed_recipe = transform_unhealthy(parsed_recipe)
    if transformation == "non-vegetarian":
        transformed_recipe = transform_non_vegetarian(parsed_recipe)

    return transformed_recipe

####
####Implement the tranformation functions here
####
def transform_vegetarian(parsed_recipe):
    raise NotImplementedError

def transform_non_vegetarian(parsed_recipe):
    raise NotImplementedError

def transform_healthy(parsed_recipe):
    raise NotImplementedError

def transform_unhealthy(parsed_recipe):
    raise NotImplementedError
####


if __name__ == "__main__":
    # Load in our config file
    with open("config.json") as f:
        config_arguments = json.load(f)

    urls = config_arguments["urls"]  # The URLS we want to transform
    commands = config_arguments["commands"] # The transformations to do on the correspounding URL

    url_command_list = [] # list of URLs, command [[url, command] , [url, command], ...]
    for i in range(len(urls)):
        entry = [urls[i], commands[i]]
        url_command_list.append(entry)

    parsed_original_recipes = [] # List of the parsed recipes as they were originally

    for url_command in url_command_list:
        parsed_recipe = parse_recipe(url_command[0], transformation=url_command[1])
        parsed_original_recipes.append(parsed_recipe)

    example_parsed_recipe = parsed_original_recipes[0] # to test out making a transformation on one recipe at a time

    transformed_recipe = transform_parsed_recipe(example_parsed_recipe)
    
