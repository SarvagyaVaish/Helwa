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

from google.appengine.api import urlfetch

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

        scrapedRecipe = Recipe(recipeUrl)

        measurementParser = MeasurementParser()
        structuredIngredients = measurementParser.Parse(scrapedRecipe.ScrapeIngredients())
        structuredIngredientsJsonString = Jsonify.ListToJsonString(structuredIngredients)

        directionsJsonString = Jsonify.ListToJsonString(scrapedRecipe.ScrapeDirections())

        template_values = {
            'RecipeUrl':    recipeUrl,
            'title':        scrapedRecipe.getTitle(),
            'ingredients':  structuredIngredientsJsonString,
            'directions':   directionsJsonString,
            'nutrition':    scrapedRecipe.getNutrition()
        }

        template = JINJA_ENVIRONMENT.get_template('RecipeEnginePage.html')
        self.response.write(template.render(template_values))
# [END RecipeEnginePage]


class NltkTestPage(webapp2.RequestHandler):
    def get(self):

        url = "https://textanalysis.p.mashape.com/nltk-pos-tagging"

        form_fields = {
            "text": "This is english pos tagger test"
        }

        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url=url,
        payload=form_data,
        method=urlfetch.POST,
        headers={
            "X-Mashape-Key": "",
            "Content-Type": "application/x-www-form-urlencoded"
            })

        logging.info(result.content)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("hello world")


application = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/RecipeEngine', RecipeEnginePage),
    ('/NltkTest', NltkTestPage),
], debug=True)
