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


ingredients = soup.findAll('li', attrs={"itemprop": "ingredients"})
print ingredients
print strip_tags(ingredients[0], ['a'])
print type(ingredients[0])
print ingredients[1]
print type(ingredients[1])


arr = []
for ingredient in ingredients:
    # print type(ingredient)
    arr.append(strip_tags(ingredient, ['a']).getText())

print
print
print arr



# x = soup.find(attrs={"itemprop": "recipeInstructions"}).contents[3]
# strip_tags(x, ['a'])
# print x.getText()

# print type(soup.findAll(attrs={"itemprop": "recipeInstructions"})[0])

# print len(soup.findAll(attrs={"itemprop": "recipeInstructions"}))

