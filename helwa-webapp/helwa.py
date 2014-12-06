# [START imports]
import os
import urllib

from Recipe import Recipe

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import logging


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
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

        r = Recipe(recipeUrl)

        template_values = {
            'RecipeUrl': recipeUrl,
            'title': r.getTitle(),
            'ingredients': r.ScrapeIngredients(),
            'directions': r.ScrapeDirections(),
            'nutrition': r.getNutrition()
        }

        template = JINJA_ENVIRONMENT.get_template('RecipeEnginePage.html')
        self.response.write(template.render(template_values))
# [END RecipeEnginePage]


application = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/RecipeEngine', RecipeEnginePage),
], debug=True)
