# [START imports]
import sys
sys.path.insert(0, 'libs')

import os
import urllib

from Recipe import Recipe
from MeasurementParser import MeasurementParser
from Jsonify import Jsonify

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import logging

# from google.appengine.api import urlfetch

# import numpy
# from nltk import tokenize
# from nltk import tag


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)
# [END imports]


# [START HomePage]
class HomePage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HomePage.html')
        self.response.write(template.render())
# [END HomePage]


# [START RecipeEnginePage]
class RecipeEnginePage(webapp2.RequestHandler):

    def get(self):
        query_params = {'Error': "no-url-found"}
        self.redirect('/?' + urllib.urlencode(query_params))

    def post(self):
        recipeUrl = self.request.get('recipe_url')

        logging.info("Url Recived:  " + recipeUrl)


        ################################
        ##        Fetch Recipe        ##
        ################################

        recipeObj = Recipe(recipeUrl)

        measurementParserObj = MeasurementParser()
        structuredIngredients = measurementParserObj.Parse(recipeObj.ScrapeIngredients())
        recipeObj.setStructuredIngredients(structuredIngredients)

        structuredDirections = recipeObj.InitDirections()

        structuredIngredientsJsonString = Jsonify.ListToJsonString(structuredIngredients)
        structuredDirectionsJsonString = Jsonify.ListToJsonString(structuredDirections)

        template_values = {
            'RecipeUrl':    recipeUrl,
            'title':        recipeObj.getTitle(),
            'ingredients':  structuredIngredientsJsonString,
            'directions':   structuredDirectionsJsonString,
            'nutrition':    recipeObj.getNutrition()
        }

        template = JINJA_ENVIRONMENT.get_template('RecipeEnginePage.html')
        self.response.write(template.render(template_values))
# [END RecipeEnginePage]


class NltkTestPage(webapp2.RequestHandler):
    def get(self):

        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("hello world")


application = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/RecipeEngine', RecipeEnginePage),
    ('/NltkTest', NltkTestPage),
], debug=True)
