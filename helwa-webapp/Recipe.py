import sys
sys.path.insert(0, 'libs')

from bs4 import BeautifulSoup, element, NavigableString
import urllib, urllib2, re, logging, ast

import pprint
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
    m_BlacklistedVerbs = ['are', 'is', 'begin', 'lime', 'golden', 'remaining', 'cooked']

    # Pattern used to find verbs
    m_VerbPattern = re.compile(r"(\w*)/VB")

    def __init__(self, url):
        self.m_Url = url
        self.m_Page = urllib2.urlopen(self.m_Url).read()
        Recipe.soup = BeautifulSoup(self.m_Page)
    
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
        ingredients = Recipe.soup.findAll('li', attrs={"itemprop": "ingredients"})
        arr = []
        for ingredient in ingredients:
            arr.append(self.strip_tags(ingredient, ['a']).getText())
        self.m_Ingredients = arr

        # arr = [
        #     "1 cup Ingredient0", 
        #     "1 cup Ingredient1", 
        #     "1 cup Ingredient2"
        # ]

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
                directionString = directionString + " " + direction

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

        # apiUrl = "https://textanalysis.p.mashape.com/nltk-pos-tagging"
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
        # logging.info(result.content)
        # resultDict = ast.literal_eval(result.content)

        result = '{"result": "Preheat/NNP the/DT broiler/NN ./. Lightly/RB oil/NN the/DT broiler/NN pan/NN ./. Toss/NNP the/DT carrots/NNS with/IN 1/CD tablespoon/NN olive/JJ oil/NN in/IN a/DT bowl/NN ,/, then/RB spread/VB out/RP on/IN one/CD side/NN of/IN the/DT pan/NN ./. Broil/NNP until/IN the/DT carrots/NNS begin/VBP to/TO soften/VB ,/, 2/CD to/TO 3/CD minutes/NNS ./. Meanwhile/NNP ,/, whisk/NN 2/CD tablespoons/NNS olive/JJ oil/NN ,/, the/DT honey/NN ,/, mustard/NN and/CC 1/CD tablespoon/NN lime/NN juice/NN in/IN a/DT small/JJ bowl/NN ./. Brush/NNP the/DT tops/NNS and/CC sides/NNS of/IN the/DT salmon/NN with/IN the/DT glaze/NN ./. Put/NNP the/DT salmon/NN ,/, skin-side/JJ down/IN ,/, on/IN the/DT other/JJ side/NN of/IN the/DT broiler/NN pan/NN next/IN to/TO the/DT carrots/NNS and/CC season/NN with/IN salt/NN and/CC pepper/NN ./. Broil/NNP until/IN the/DT salmon/NN is/VBZ golden/VBN brown/RP and/CC just/RB cooked/VBD through/IN and/CC the/DT carrots/NNS are/VBP crisp-tender/JJ ,/, 5/CD to/TO 7/CD minutes/NNS ./. Whisk/NNP the/DT remaining/VBG 1/CD tablespoon/NN each/DT olive/JJ oil/NN and/CC lime/NN juice/NN ,/, the/DT coriander/NN ,/, cumin/NN ,/, cinnamon/NN ,/, mint/NN and/CC almonds/NNS in/IN a/DT bowl/NN ./. Add/NNP the/DT carrots/NNS and/CC toss/NN to/TO combine/VB ;/: season/NN with/IN salt/NN and/CC pepper/NN ./. Serve/NNP the/DT salmon/NN with/IN the/DT carrots/NNS and/CC lime/VB wedges/NNS ./."}'

        # result = '{"result": "Verb0/VB Ingredient0/DD ./. Verb1/VB Ingredient0/DD Ingredient1/DD ./. Verb2/VB Ingredient2/DD ./."}'
        resultDict = ast.literal_eval(result)
        
        self.m_TaggedDirectionString = resultDict["result"]
        
        return 

    # Splits tagged directions into by newlines
    # Returns a list of dictionaries with id and sentence of each POS tagged sentence
    def SplitDirections(self):
        # Split sentences
        m = re.sub(r'\/\.\s|\/;\s', '\n', self.m_TaggedDirectionString)
        sentenceList = re.split('\n', m)
        i = 0
        for sentence in sentenceList:
            directionDictionary = {}
            directionDictionary['id'] = 'direction' + str(i)
            directionDictionary['prettySentence'] = re.sub(r'\/[A-Z]{2,3}|\/\.|\/,','', sentence)
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
            foundVerbFlag = False
            for matchResult in matchResultsIt:
                verb = matchResult.group(1)
                if (verb not in self.m_BlacklistedVerbs):
                    foundVerbFlag = True
                    newActionNode = { 
                        "verb": verb,
                        "ingredientIds": []
                    }
                    directionDict['action-nodes'].append(newActionNode)

            # If no verb was found, use the first word of the sentence
            if not foundVerbFlag:
                verb = "Unknown"
                matchResult = re.match(r"([a-zA-Z]+)\/[A-Z]{2,3}", directionString)
                if matchResult:
                    verb = matchResult.group(1)
                
                newActionNode = { 
                    "verb": verb,
                    "ingredientIds": []
                }
                directionDict['action-nodes'].append(newActionNode)

            self.m_SplitDirections[i] = directionDict

        return


    # Associate ingredients with directions
    def AssociateIngredientsWithDirections(self):

        # Create a map from ingredient ids to ingredient names (words)
        ingredientMap = {}
        for ingredient in self.m_StructuredIngredients:
            ingredientMap[ingredient["id"]] = []

            ingredientString = ingredient["name"]
            ingredientWords = re.split(r" |,|\.|'", ingredientString)
            for word in ingredientWords:
                if len(word) > 3:   # TODO: This is a hack to get rid of 'and', 'the', etc
                    ingredientMap[ingredient["id"]].append(word.lower())

        logging.info(ingredientMap)

        # Iterate over each direction prettySentence and try to find ingredient words
        for i in range(len(self.m_SplitDirections)):
            directionString = self.m_SplitDirections[i]["prettySentence"]
            directionString = directionString.lower()

            for ingredientId, ingredientWords in ingredientMap.iteritems():
                for ingredientWord in ingredientWords:

                    # try to find the word in the direction string
                    ingredientWordLoc = directionString.find(ingredientWord)
                    if ingredientWordLoc >= 0:
                        # find locations of the verbs in the current direction string
                        actionNodeLocations = []
                        for actionNode in self.m_SplitDirections[i]["action-nodes"]:
                            actionNodeLocations.append(directionString.find(actionNode['verb']))

                        # find verb that is closest to ingredient word
                        minDist = 999999
                        minId = -1
                        for locIndex in range(len(actionNodeLocations)):
                            if abs(actionNodeLocations[locIndex] - ingredientWordLoc) < minDist:
                                minDist = abs(actionNodeLocations[locIndex] - ingredientWordLoc)
                                minId = locIndex

                        # associate this ingredient with the minId action-node
                        self.m_SplitDirections[i]["action-nodes"][minId]['ingredientIds'].append(ingredientId)
                        break # to avoid duplicates

            pp = pprint.PrettyPrinter(indent=4)
            logging.info("####    Associated Ingredients Results    ####")
            logging.info(pp.pformat(self.m_SplitDirections[i]))

        return


    def getDirections(self):
        return self.m_SplitDirections


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

