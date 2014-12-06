import json

ingredients = [
 {
 	"Amount": "1 1/2",
 	"Unit": "cups",
 	"Ingredient": "flour",
 },
 {
 	"Amount": "1",
 	"Unit": "Pinch",
 	"Ingredient": "of ground cinnamon",
 },
]

ingredients = {	"ingredients": ingredients }

# print ingredients

directions = [
 {
 			"id": "direction_2", 
            "ingredient_list": [ 
                "ingredient_1" 
            ], 
            "cookware_list": [ 
                "cookware_2", 
                "cookware_3" 
            ], 
            "description": "Line a #<cookware_2> with #<cookware_3> and spray with #<ingredient_1>.", 
            "original_text": "Line a baking sheet with aluminum foil and spray with cooking spray." 
 },
 { 
            "id": "direction_3",
            "ingredient_list": [ 
                "ingredient_2", 
                "ingredient_3" 
            ], 
            "description": "Stir #<ingredient_2> and #<ingredient_3> together in a #<cookware_4>.", 
            "original_text": "Stir bread crumbs and Parmesan cheese together in a shallow bowl." 
        },
]

directions = { "directions": directions }

# print ingredients
# print
# print directions

with open('data.json', 'w') as outfile:
	json.dump(ingredients, outfile)
	# json.dump(directions, outfile)

with open('data.json') as outfile:
	data = json.load(outfile)
	print data
	print
	data.update(directions)
	print data
# data.update(directions)

with open('data.json', 'w') as outfile:
	data = json.dump(data, outfile)