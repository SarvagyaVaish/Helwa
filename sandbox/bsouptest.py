from bs4 import BeautifulSoup, element, NavigableString
import urllib2, re

page = urllib2.urlopen('http://www.foodnetwork.com/recipes/food-network-kitchens/glazed-salmon-with-spiced-carrots-recipe.html').read()
# page = urllib2.urlopen('http://www.foodnetwork.com/recipes/food-network-kitchens/classic-glazed-ham-recipe.html').read()
soup = BeautifulSoup(page)

# print soup.findAll(attrs={"itemprop": "recipeInstructions"})
def strip_tags(snippet, invalid_tags):

    # for tag in snippet.findAll(True):
    for tag in snippet:
        if tag.name in invalid_tags:
            s = ""

            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(unicode(c), invalid_tags)
                s += unicode(c)

            tag.replaceWith(s)

    return snippet

# x = soup.find(attrs={"itemprop": "recipeInstructions"}).contents[3]
# strip_tags(x, ['a'])
# print x.getText()

# print type(soup.findAll(attrs={"itemprop": "recipeInstructions"})[0])

# print len(soup.findAll(attrs={"itemprop": "recipeInstructions"}))

# Must use the 4th element in the resultant array for foodnetwork's setup
directions = soup.find(attrs={"itemprop": "recipeInstructions"}).findAll('p')
# print directions
# strip_tags(directions, ['a'])

nutrition = ""
arr = []

for direction in directions:
	i = strip_tags(direction, ['a']).getText()
	if "Calories" in i:
		nutrition = i
	elif "Food Network" not in i and "Photograph" not in i:
		m = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', i)
		print type(m)
		for x in m:
			arr.append(x)
# print soup.find(attrs={"itemprop": "recipeInstructions"}).contents
# print directions.getText()

for i in arr:
	print i

print len(arr)
# print nutrition

# print soup.find(attrs={"itemprop": "recipeInstructions"}).findAll('p')