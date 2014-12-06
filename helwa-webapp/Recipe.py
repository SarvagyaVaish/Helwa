import sys
sys.path.insert(0, 'libs')

from bs4 import BeautifulSoup, element, NavigableString
import urllib2, re

class Recipe:

	soup = BeautifulSoup()
	nutrition = ""

	def __init__(self, url):
		page = urllib2.urlopen(url).read()
		Recipe.soup = BeautifulSoup(page)
	
	def strip_tags(self, snippet, invalid_tags):
	    for tag in snippet:
	        if tag.name in invalid_tags:
	            s = ""
	            for c in tag.contents:
	                if not isinstance(c, NavigableString):
	                    c = strip_tags(unicode(c), invalid_tags)
	                s += unicode(c)
	            tag.replaceWith(s)
	    return snippet


	def getTitle(self):
		return  Recipe.soup.find('h1', attrs={"itemprop": "name"}).string
		
	# Scrape a Recipe's Ingredients
	def ScrapeIngredients(self):
		ingredients = Recipe.soup.findAll('li', attrs={"itemprop": "ingredients"}, text=True)
		arr = []
		for ingredient in ingredients:
			arr.append(ingredient.string)
		return arr

	# Scape a Recipe's Directions - for foodnetwork.com
	def ScrapeDirections(self):
		# Must use the 4th element in the resultant array for foodnetwork's setup
		directions = Recipe.soup.find(attrs={"itemprop": "recipeInstructions"}).findAll('p')
		arr = []
		for direction in directions:
			# Get rid of the anchor tags
			direction = self.strip_tags(direction, ['a']).getText()
			# Save Recipe's nutritional Information, if available
			if "Calories" in direction:
				self.nutrition = direction
			# Remove misc info at the bottom of directions section
			elif "Food Network" not in direction and "Photograph" not in direction and len(direction.split()) > 2:
				# Split sentences
				m = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', direction)
				for x in m:
					arr.append(x)

		return arr

	# Return Recipe Nutritional Info
	def getNutrition(self):
		return  self.nutrition


################# TESTING #################################
# test1 = Recipe('http://www.foodnetwork.com/recipes/food-network-kitchens/glazed-salmon-with-spiced-carrots-recipe.html')
# print test1.getTitle()
# print "Ingredients"
# for i in test1.ScrapeIngredients():
# 	print i
# print
# print "Directions"
# for i in test1.ScrapeDirections():
# 	print i
# if test1.getNutrition():
# 	print "Nutritional Info"
# 	print test1.getNutrition()

# print len(test1.ScrapeDirections())

# print
# print

# test2 = Recipe('http://www.foodnetwork.com/recipes/food-network-kitchens/classic-glazed-ham-recipe.html')
# print test2.getTitle()
# print "Ingredients"
# for i in test2.ScrapeIngredients():
# 	print i
# print
# print "Directions"
# for i in test2.ScrapeDirections():
# 	print i
# if test2.getNutrition():
# 	print "Nutritional Info"
# 	print test2.getNutrition()

