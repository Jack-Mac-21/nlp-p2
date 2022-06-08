unhealthy_to_healthy_dicts = {
    "subs": {
        "bacon":["shiitake mushrooms", "sun-dried tomatoes", "smoked paprika"],
        "butter":["olive oil"],
        "beef chuck roast":["flank steak"],
        "flour":["whole-wheat flour"],
        "beef broth": ["low sodium beef broth"],
        "chicken broth": ["low sodium chicken broth"],
        "vegetable broth": ["low sodium vegetable broth"],
        "sugar": ["sugar"],
        "salt": ["salt"],
        "chicken thighs": ["chicken breast"],
        "flour tortilla": ["corn tortilla"],
    },
    "conversions": {
        "bacon":[2, 2, 4],
        "butter":[1],
        "beef chuck roast":[1],
        "flour":[1],
        "sugar":[.75],
        "salt":[.75],
    },
    "measurements": {
        "shiitake mushrooms":"pounds",
        "sun-dried tomatoes":"cups",
        "smoked paprika":"teaspoons",
        "flank steak":"pounds",
        "whole-wheat flour":"tablespoons",
        "olive oil":"tablespoons"
    },
    "aliases": {
        "beef chuck roast":["beef", "meat"]
    },
    "methods": {
        "butter":["melt", "heat"]
    }
}

healthy_to_unhealthy_dicts = {
    "subs": {
        "mushrooms":["bacon"],
        "sesame oil":["butter"],
        "ground mustard":["yellow mustard"],
        "soy sauce":["soy sauce"],
        "low sodium beef broth": ["beef broth"],
        "low sodium chicken broth": ["chicken broth"],
        "low sodium vegetable broth": ["vegetable broth"],
        "sugar": ["sugar"],
        "salt": ["salt"],
        "chicken thighs": ["chicken breast"],
        "corn tortilla": ["flour tortilla"],
        "salmon": ["bone-in, skin-on chicken thighs"]
        },
    "conversions": {
        "bacon":[1/2],
        "butter":[1],
        "beef chuck roast":[1],
        "flour":[1],
        "sugar":[1.25],
        "salt":[1.25],
        "soy sauce":[1.25]
    },
    "measurements": {
        "sun-dried tomatoes":"cups",
        "smoked paprika":"teaspoons",
        "olive oil":"tablespoons",
    },
    "aliases": {
        "salmon":["fish"]
    },
    "methods": {

    }
}
def transform_healthy_helper(parsed_recipe):
    substitutes = unhealthy_to_healthy_dicts["subs"]
    conversions = unhealthy_to_healthy_dicts["conversions"]
    measurements = unhealthy_to_healthy_dicts["measurements"]
    aliases = unhealthy_to_healthy_dicts["aliases"]
    methods = unhealthy_to_healthy_dicts["methods"]

    return replacement_function(parsed_recipe, substitutes, conversions, measurements, aliases, methods)

def transform_unhealthy_helper(parsed_recipe):
    substitutes = healthy_to_unhealthy_dicts["subs"]
    conversions = healthy_to_unhealthy_dicts["conversions"]
    measurements = healthy_to_unhealthy_dicts["measurements"]
    aliases = healthy_to_unhealthy_dicts["aliases"]
    methods = healthy_to_unhealthy_dicts["methods"]

    return replacement_function(parsed_recipe, substitutes, conversions, measurements, aliases, methods)

def replacement_function(parsed_recipe, ingredient_substitutes, ingredient_conversions, ingredient_meas, ingredient_aliases, ingredient_methods):
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
                    original_quantity = ingredient["quantity"]
                    if (ingredient_substring in ingredient_conversions 
                        and (type(original_quantity) == int or type(original_quantity) == float)):
                            ingredient_sub["quantity"] = ingredient_conversions[ingredient_substring][ind]*original_quantity
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
            ingredient_names = [ingredient]
            if ingredient in ingredient_aliases:
                ingredient_names += ingredient_aliases[ingredient]
            for alias in ingredient_names:
                if alias in new_steps[i]:
                    if ingredient in ingredient_methods:
                        new_steps[i] = new_steps[i].replace(ingredient_methods[ingredient][0], ingredient_methods[ingredient][1])
                    new_steps[i] = new_steps[i].replace(alias,  ingredient_substitutes[ingredient][0])
                    # print(new_steps[i])

    parsed_recipe["steps"]=new_steps
    return parsed_recipe