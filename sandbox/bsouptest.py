from bs4 import BeautifulSoup
import urllib2

page = urllib2.urlopen('http://www.foodnetwork.com/recipes/food-network-kitchens/spanish-style-noodles-with-chicken-and-sausage-recipe.html').read()
soup = BeautifulSoup(page)

soup.prettify()
for anchor in soup.findAll('a', href=True):
    print anchor['href']
