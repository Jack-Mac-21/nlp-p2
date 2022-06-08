# This file will run our program, just call it in the terminal and it will output the results in the output json
from RecipeParserClass import RecipeParser
from DataParsingUtilities import *
from data.region_transform import substitutes
import json
import StringOutputGenerator
from bs4 import BeautifulSoup
import copy

# Pass in a URL and it will return a dictionar 
# {"ingredients": ingredients_dictionary, "steps" : list of steps, 
# "tools" : list of tools, *not implemented yet
# "methods": list of methods *not implemented yet
# "primary method": primary_method} #not implemented yet
def parse_recipe(soup=None, url=None, transformation="None"):
    ingredients = get_ingredients(soup=soup)
    title = get_title(soup=soup)
    steps = get_steps(soup=soup)
    tools = get_tools(steps)
    methods = get_methods(steps)
    primary_method = get_primary_method(methods)

    
    parsed_recipe = {"url" : url,
                     "title" : title,
                     "ingredients" : ingredients,
                     "steps": steps,
                     "tools" : tools,
                     "primary_method": primary_method,
                     "methods" : methods,
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
    if transformation == "european":
        transformed_recipe = transform_european(parsed_recipe)
    # if transformation == "east_asian":
    #     transformed_recipe = transform_east_asian(parsed_recipe)

    return transformed_recipe

####
####Implement the tranformation functions here
####
def transform_vegetarian(parsed_recipe):
    food_dict = {
            "protein" : ["chicken", "fish", "salmon", "shrimp", "steak", "beef", "tofu", "pork", "bacon", "meat", "ground beef"],
            "vegtable_proteing" : ["tofu", "impossible meat", "veggie burger", "plant based burger"],
            "vegtables" : ["carrots", "onions", "broccoli", "cauliflower", "spinach", "lettuce", "tomato", "broccolini"]
            
        }
    #print(food_dict[protein])
    proteinMap = [["beef", "tofu"],["chicken", "chickpeas"], ["bacon", "imitation bacon"], ["burger patty", "impossible burger patty"], ["beef burger", "impossible burger patty"], ["burger", "impossible burger"]]
    changed = {}
    ingredients = parsed_recipe['ingredients']
    steps = parsed_recipe['steps']

    for i in range(len(proteinMap)):
        for j in range(len(ingredients)):
            if proteinMap[i][0] in ingredients[j]['name']:
                t = ingredients[j]['name']
                changed[proteinMap[i][0]] = t
                t = proteinMap[i][1]
                ingredients[j]['name'] = t
        for k in range(len(steps)):
            if proteinMap[i][0] in steps[k]:
                t =steps[k]
                if proteinMap[i][0] in changed and changed[proteinMap[i][0]] in steps[k]:
                    t = t.replace(changed[proteinMap[i][0]], proteinMap[i][1])
                    steps[k] = t
                else: 
                    t = t.replace(proteinMap[i][0], proteinMap[i][1])
                    steps[k] = t
               # print(ingredients)
    parsed_recipe['ingredients'] = ingredients
    parsed_recipe['steps'] = steps
    print(ingredients)
    print(steps)
    return parsed_recipe
def transform_non_vegetarian(parsed_recipe):
        #print(food_dict[protein])
    proteinMap = [["beef steak", "tofu"],["chicken", "chickpeas"], ["bacon", "imitation bacon"], ["burger patty", "impossible burger patty"], ["beef burger", "impossible burger patty"], ["burger", "impossible burger"], ["ham", "mushroom"]]
    changed = {}
    ingredients = parsed_recipe['ingredients']
    steps = parsed_recipe['steps']

    for i in range(len(proteinMap)):
        for j in range(len(ingredients)):
            if proteinMap[i][1] in ingredients[j]['name']:
                t = ingredients[j]['name']
                changed[proteinMap[i][1]] = t
                t = proteinMap[i][0]
                ingredients[j]['name'] = t
                print(t)
        for k in range(len(steps)):
            if proteinMap[i][1] in steps[k]:
                t =steps[k]
                if proteinMap[i][1] in changed and changed[proteinMap[i][1]] in steps[k]:
                    t = t.replace(changed[proteinMap[i][1]], proteinMap[i][0])
                    steps[k] = t
                else: 
                    t = t.replace(proteinMap[i][1], proteinMap[i][0])
                    steps[k] = t
               # print(ingredients)
    parsed_recipe['ingredients'] = ingredients
    parsed_recipe['steps'] = steps
    print(ingredients)
    print(steps)
    return parsed_recipe

def transform_healthy(parsed_recipe):
    ingredient_substitutes = {
        "bacon":["shiitake mushrooms", "sun-dried tomatoes", "smoked paprika"],
        "butter":["olive oil"],
        "beef chuck roast":["flank steak"],
        "flour":["whole-wheat flour"],
        "beef broth": ["low sodium beef broth"],
        "chicken broth": ["low sodium chicken broth"],
        "vegetable broth": ["low sodium vegetable broth"],
        "sugar": ["sugar"],
        }
    ingredient_conversions = {
        "bacon":[2, 2, 4],
        "butter":[1],
        "beef chuck roast":[1],
        "flour":[1],
        "sugar":[.75]
    }
    ingredient_meas = {
        "shiitake mushrooms":"pounds",
        "sun-dried tomatoes":"cups",
        "smoked paprika":"teaspoons",
        "flank steak":"pounds",
        "whole-wheat flour":"tablespoons",
        "olive oil":"tablespoons"
    }
    ingredient_methods = {
        "butter":"melt"
    }

    # replace ingredients
    new_ingredients = []
    substitutes_made = []
    for ingredient in parsed_recipe["ingredients"]:
        isSubstituted = False
        for ingredient_substring in ingredient_substitutes:
            if ingredient_substring in ingredient["name"].lower():
                isSubstituted = True
                substitutes_made.append(ingredient_substring)
                for substitute in ingredient_substitutes[ingredient_substring]:
                    ingredient_sub= {}
                    # ingredient name
                    ingredient_sub["name"] = ingredient["name"].lower().replace(ingredient_substring, substitute)
                    ind = ingredient_substitutes[ingredient_substring].index(substitute)
                    # quantity 
                    if ingredient_substring in ingredient_conversions:
                        ingredient_sub["quantity"] = ingredient_conversions[ingredient_substring][ind]*ingredient["quantity"]
                    else:
                        ingredient_sub["quantity"] = ingredient["quantity"]
                    # measurement
                    if substitute in ingredient_meas:
                        ingredient_sub["measurement"] = ingredient_meas[substitute]
                    else:
                        ingredient_sub["measurement"] = ingredient["measurement"]
                    # append fleshed out substitute to ingredient list
                    new_ingredients.append(ingredient_sub)
        if not isSubstituted:
            # keep healthy ingredients
            new_ingredients.append(ingredient)

    # replaced parsed recipe ingredient list
    parsed_recipe["ingredients"] = new_ingredients

    # replace in steps with correct ingredients
    new_steps = parsed_recipe["steps"].copy()
    for i in range(len(new_steps)):
        for ingredient in substitutes_made:
            if ingredient in new_steps[i]:
                new_steps[i] = new_steps[i].replace(ingredient,  ingredient_substitutes[ingredient][0])
                # print(new_steps[i])

    parsed_recipe["steps"]=new_steps
    return parsed_recipe

def transform_unhealthy(parsed_recipe):
    raise NotImplementedError

def transform_european(parsed_recipe):
    ingredients = parsed_recipe["ingredients"]
    transform_list = []
    for i in range(len(ingredients)):
        ingre = ingredients[i]['name']
        for j in range(len(substitutes)):
            sub = substitutes[j]
            if (sub[1] in ingre):
                transform_list.append((i,j))
    new_recipe = copy.deepcopy(parsed_recipe)
    for sub in transform_list:
        new_recipe["ingredients"][sub[0]]["name"] = substitutes[sub[1]][0]
    return new_recipe

def transform_east_asian(parsed_recipe):
    ingredients = parsed_recipe["ingredients"]
    transform_list = []
    for i in range(len(ingredients)):
        ingre = ingredients[i]['name']
        for j in range(len(substitutes)):
            sub = substitutes[j]
            if (sub[0] in ingre):
                transform_list.append((i,j))
    new_recipe = copy.deepcopy(parsed_recipe)
    for sub in transform_list:
        new_recipe["ingredients"][sub[0]]["name"] = substitutes[sub[1]][1]
    return new_recipe
####
def double_or_half_amount(parsed_recipe, mul = 0):
    ingredients = parsed_recipe["ingredients"]
    x = 0.5 + 1.5*mul
    for i in range(len(ingredients)):
        ingredients[i]['quantity']=  ingredients[i]['quantity'] * x
    parsed_recipe["ingredients"] = ingredients
    return parsed_recipe
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
        page = requests.get(url_command[0])
        soup = BeautifulSoup(page.content, "html.parser")

        parsed_recipe = parse_recipe(soup=soup, url=url_command[0], transformation=url_command[1])
        parsed_original_recipes.append(parsed_recipe)

    example_parsed_recipe = parsed_original_recipes[1]  # to test out making a transformation on one recipe at a time


    output_string = StringOutputGenerator.create_string_from_recipe(example_parsed_recipe)
    print(output_string)

    #transformed_recipe = transform_parsed_recipe(example_parsed_recipe)
    #output_string = StringOutputGenerator.create_string_from_recipe(transformed_recipe)
    #print(output_string)
    # print(example_parsed_recipe["steps"])
    
