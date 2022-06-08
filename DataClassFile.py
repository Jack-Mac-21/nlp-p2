class FoodDataClass():

    def __init__(self) -> None:
        self.food_dictionary = {
            "protein" : ["chicken", "fish", "salmon", "shrimp", "steak", "beef", "tofu", "pork", "bacon"],
            "vegtable_protein" : ["tofu", "impossible meat", "veggie burger", "plant based burger"],
            "vegtables" : ["carrots", "onions", "broccoli", "cauliflower", "spinach", "lettuce", "tomato", "broccolini"]
            
        }
        self.measurements = ["teaspoons", "teaspoon", "ounce", "ounces", "tablespoon", "tablespoons", "cups", "cup", "pint","pints",
        "quarts", "quart", "pound", "pounds", "grams", "gram"]

        self.methods = ["bake", "broil", "sauté", "saute", "whisk", "scramble", "fold", "grate", "shred", "blend", "mix", "cover", "blend", "melt", "heat"
                        "cook", "fill", "mince", "chop", "cube", "stir", "roast" , "boil", "slice", "steam", "layer", "fry"]

        self.method_converter = {
            "bake" : "baking", "broil" : "broiling", "sauté" : "sauteing", 
             "saute" : "sauteing", 
             "whisk" : "whisking", 
             "scramble" : "scrambling", 
             "fold" : "folding", 
             "grate" : "grating", 
             "shred" : "shredding",
              "blend": "blending", 
              "mix" : "mixing", 
              "cover" : "covering", 
              "blend" : "blending", 
              "melt" : "melting", 
              "heat" : "heating",
              "cook" : "cooking", 
              "fill" : "filling", 
              "mince" : "mincing", 
              "chop" : "chopping", 
              "cube" : "cubing", "stir" : "stirring", 
              "roast" : "roasting" , "boil" : "boiling", 
              "slice" : "slicing", "steam" : "steaming", 
              "layer" : "layering", "fry" : "frying"

        }

        self.tools = ["pan", "skillet", "spatula", "whisk", "pot", "ladle", "knife", "cutting board", "strainer", "slotted spoon", "tongs", "julienne",
                    "grater", "shredder", "blender", "saucepan", "oven"]

        self.cooking_stlyes = []

            
    

