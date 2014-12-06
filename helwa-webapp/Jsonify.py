import json

# Jsonify creates recipe JSON object based on ingredients and directions
class Jsonify:

	def __init__(self, recipe_id, ingredients, directions):
		self.recipe_id = recipe_id
		self.ingredients = { "ingredients": ingredients }
		self.directions = { "directions": directions }

	def dump(self):
		with open(self.recipe_id+'.json', 'w') as outfile:
			json.dump(self.directions, outfile)

		with open(self.recipe_id+'.json') as outfile:
			data = json.load(outfile)
			data.update(self.ingredients)
		with open(self.recipe_id+'.json', 'w') as outfile:
			json.dump(data, outfile)
			

############################ TESTING ###################
# ingredients = [
#  {
#  	"Amount": "1 1/2",
#  	"Unit": "cups",
#  	"Ingredient": "flour",
#  },
#  {
#  	"Amount": "1",
#  	"Unit": "Pinch",
#  	"Ingredient": "of ground cinnamon",
#  },
# ]

# directions = [
#  {
#  			"id": "direction_2", 
#             "ingredient_list": [ 
#                 "ingredient_1" 
#             ], 
#             "cookware_list": [ 
#                 "cookware_2", 
#                 "cookware_3" 
#             ], 
#             "description": "Line a #<cookware_2> with #<cookware_3> and spray with #<ingredient_1>.", 
#             "original_text": "Line a baking sheet with aluminum foil and spray with cooking spray." 
#  },
#  { 
#             "id": "direction_3",
#             "ingredient_list": [ 
#                 "ingredient_2", 
#                 "ingredient_3" 
#             ], 
#             "description": "Stir #<ingredient_2> and #<ingredient_3> together in a #<cookware_4>.", 
#             "original_text": "Stir bread crumbs and Parmesan cheese together in a shallow bowl." 
#         },
# ]

# test = Jsonify('123', ingredients, directions)
# test.dump()