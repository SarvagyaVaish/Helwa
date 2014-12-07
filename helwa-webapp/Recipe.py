import sys
sys.path.insert(0, 'libs')

from bs4 import BeautifulSoup, element, NavigableString
import urllib, urllib2, re, logging, ast

from google.appengine.api import urlfetch

class Recipe:

    soup = BeautifulSoup()
    m_Nutrition = ""
    m_Ingredients = []
    m_Url = ""
    m_SplitDirections  = []
    m_TaggedDirectionString = ""
    m_Page = ""
    m_StructuredIngredients = []

    # Pattern used to find verbs
    m_VerbPattern = re.compile(r"(\w*)/VB")

    def __init__(self, url):
        self.m_Url = url
        m_Page = urllib2.urlopen(self.m_Url).read()
        Recipe.soup = BeautifulSoup(m_Page)
    
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
    # Returns a list of ingredients in plain text
    def ScrapeIngredients(self):
        ingredients = Recipe.soup.findAll('li', attrs={"itemprop": "ingredients"}, text=True)
        arr = []
        for ingredient in ingredients:
            arr.append(ingredient.string)
        self.m_Ingredients = arr
        return arr

    # Scape a Recipe's Directions - for foodnetwork.com
    def ScrapeDirections(self):
        # Must use the 4th element in the resultant array for foodnetwork's setup
        directions = Recipe.soup.find(attrs={"itemprop": "recipeInstructions"}).findAll('p')
        directionString = ""
        for direction in directions:
            # Get rid of the anchor tags
            direction = self.strip_tags(direction, ['a']).getText()
            # Save Recipe's nutritional Information, if available
            if "Calories" in direction:
                self.nutrition = direction
            # Remove misc info at the bottom of directions section
            elif "Food Network" not in direction and "Photograph" not in direction and len(direction.split()) > 2:
                directionString = directionString + direction

        self.m_Directions = directionString

        return

    # Return Recipe Nutritional Info
    def getNutrition(self):
        return  self.nutrition

    # Convenience method
    def InitDirections(self):
        self.ScrapeDirections()
        self.RunPosTaggerOnDirections()
        self.SplitDirections()
        self.ParseVerbsInDirections()
        self.AssociateIngredientsWithDirections()

        return self.m_SplitDirections


    # Return tagged directions
    def RunPosTaggerOnDirections(self):
        apiUrl = "https://textanalysis.p.mashape.com/nltk-pos-tagging"

        # form_fields = {
        #     "text": self.m_Directions
        # }

        # form_data = urllib.urlencode(form_fields)
        # result = urlfetch.fetch(url=apiUrl,
        #     payload=form_data,
        #     method=urlfetch.POST,
        #     headers={
        #         "X-Mashape-Key": "",
        #         "Content-Type": "application/x-www-form-urlencoded"
        #     })

        result = '{"result": "Preheat/NNP the/DT broiler/NN ./. Lightly/RB oil/NN the/DT broiler/NN pan/NN ./. Toss/NNP the/DT carrots/NNS with/IN 1/CD tablespoon/NN olive/JJ oil/NN in/IN a/DT bowl/NN ,/, then/RB spread/VB out/RP on/IN one/CD side/NN of/IN the/DT pan/NN ./. Broil/NNP until/IN the/DT carrots/NNS begin/VBP to/TO soften/VB ,/, 2/CD to/TO 3/CD minutes.Meanwhile/JJ ,/, whisk/NN 2/CD tablespoons/NNS olive/JJ oil/NN ,/, the/DT honey/NN ,/, mustard/NN and/CC 1/CD tablespoon/NN lime/NN juice/NN in/IN a/DT small/JJ bowl/NN ./. Brush/NNP the/DT tops/NNS and/CC sides/NNS of/IN the/DT salmon/NN with/IN the/DT glaze/NN ./. Put/NNP the/DT salmon/NN ,/, skin-side/JJ down/IN ,/, on/IN the/DT other/JJ side/NN of/IN the/DT broiler/NN pan/NN next/IN to/TO the/DT carrots/NNS and/CC season/NN with/IN salt/NN and/CC pepper/NN ./. Broil/NNP until/IN the/DT salmon/NN is/VBZ golden/VBN brown/RP and/CC just/RB cooked/VBD through/IN and/CC the/DT carrots/NNS are/VBP crisp-tender/JJ ,/, 5/CD to/TO 7/CD minutes.Whisk/JJ the/DT remaining/VBG 1/CD tablespoon/NN each/DT olive/JJ oil/NN and/CC lime/NN juice/NN ,/, the/DT coriander/NN ,/, cumin/NN ,/, cinnamon/NN ,/, mint/NN and/CC almonds/NNS in/IN a/DT bowl/NN ./. Add/NNP the/DT carrots/NNS and/CC toss/NN to/TO combine/VB ;/: season/NN with/IN salt/NN and/CC pepper/NN ./. Serve/NNP the/DT salmon/NN with/IN the/DT carrots/NNS and/CC lime/VB wedges/NNS ./."}'
        resultDict = ast.literal_eval(result)
        
        self.m_TaggedDirectionString = resultDict["result"]
        
        return 

    # Splits tagged directions into by newlines
    # Returns a list of dictionaries with id and sentence of each POS tagged sentence
    def SplitDirections(self):
        # Split sentences
        m = re.sub(r'\/\.\s*', '\n', self.m_TaggedDirectionString)
        sentenceList = re.split('\n', m)
        i = 0
        for sentence in sentenceList:
            directionDictionary = {}
            directionDictionary['id'] = i
            directionDictionary['sentence'] = sentence
            self.m_SplitDirections.append(directionDictionary)
            i = i + 1

        return 

    # Find the VB* in the direction sentences
    # For each found verb, add a node to the corresponding dictionary
    # Assumes that there already exists a list of direction dictionaries (m_SplitDirections)
    # Updates each direction dictionary with a list of action-nodes
    def ParseVerbsInDirections(self):

        for i in range(len(self.m_SplitDirections)):
            directionDict = self.m_SplitDirections[i]
            directionString = directionDict["sentence"]

            directionDict['action-nodes'] = []

            matchResultsIt = self.m_VerbPattern.finditer(directionString)
            for matchResult in matchResultsIt:
                verb = matchResult.group(1)
                newActionNode = { "verb": verb }
                directionDict['action-nodes'].append(newActionNode)

            self.m_SplitDirections[i] = directionDict

        return


    # Associate ingredients with directions
    def AssociateIngredientsWithDirections(self):
        return


    def getDirections(self):
        return m_SplitDirections


    def setStructuredIngredients(self, ingredients):
        self.m_StructuredIngredients = ingredients
        return






################# TESTING #################################
# test1 = Recipe('http://www.foodnetwork.com/recipes/food-network-kitchens/glazed-salmon-with-spiced-carrots-recipe.html')
# print test1.getTitle()
# print "Ingredients"
# for i in test1.ScrapeIngredients():
#     print i
# print
# print "Directions"
# # for i in test1.ScrapeDirections():
# #   print i
# print test1.ScrapeDirections()
# if test1.getNutrition():
#     print "Nutritional Info"
#     print test1.getNutrition()

# logging.info(test1.RunPosTaggerOnDirections())
# print test1.RunPosTaggerOnDirections()

# logging.info(test1.SplitDirections())

# print len(test1.ScrapeDirections())

# print
# print

# test2 = Recipe('http://www.foodnetwork.com/recipes/food-network-kitchens/classic-glazed-ham-recipe.html')
# print test2.getTitle()
# print "Ingredients"
# for i in test2.ScrapeIngredients():
#   print i
# print
# print "Directions"
# for i in test2.ScrapeDirections():
#   print i
# if test2.getNutrition():
#   print "Nutritional Info"
#   print test2.getNutrition()

