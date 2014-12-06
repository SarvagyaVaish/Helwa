import re
import json


class MeasurementParser:
    # Constants
    fractionPattern = re.compile(r"\d*\s*\d*/\d*")
    decimalPattern = re.compile(r"\d*\.\d+")
    integerPattern = re.compile(r"(\d+)")

    amountWords = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
    amountWordsPatternStr = ""
    for tempStr in amountWords:
        amountWordsPatternStr = amountWordsPatternStr + "|" + tempStr
    amountWordsPatternStr = amountWordsPatternStr[1:]
    amountWordsPattern = re.compile(amountWordsPatternStr)

    unitsMapper = {
        "cup": ["cups", "cup", "c.", "c"],
        "fluid_ounce": ["fl\. oz\.", "fl oz", "fluid ounce", "fluid ounces"],
        "gallon": ["gal", "gal\.", "gallon", "gallons"],
        "ounce": ["oz", "oz\.", "ounce", "ounces"],
        "pint": ["pt", "pt\.", "pint", "pints"],
        "pound": ["lb", "lb\.", "pound", "pounds"],
        "quart": ["qt", "qt\.", "qts", "qts\.", "quart", "quarts"],
        "tablespoon": ["tbsp\.", "tbsp", "T", "T\.", "tablespoon", "tablespoons", "tbs\.", "tbs"],
        "teaspoon": ["tsp\.", "tsp", "t", "t\.", "teaspoon", "teaspoons"],
        "gram": ["g", "g\.", "gr", "gr\.", "gram", "grams"],
        "kilogram": ["kg", "kg\.", "kilogram", "kilograms"],
        "liter": ["l", "l\.", "liter", "liters"],
        "milligram": ["mg", "mg\.", "milligram", "milligrams"],
        "milliliter": ["ml", "ml\.", "milliliter", "milliliters"],
        "pinch": ["pinch", "pinches"],
        "dash": ["dash", "dashes"],
        "touch": ["touch", "touches"],
        "handful": ["handful", "handfuls"]
    }


    # Helper method
    def StartAndEndOfLongestTuple(self, tuples):
        longestLength = -1
        start = -1
        end = -1
        for tuple in tuples:
            currLen = tuple[1] - tuple[0]
            if currLen > longestLength:
                longestLength = currLen
                start = tuple[0]
                end = tuple[1]

        return (start, end)


    # Takes in a list of strings containing ingredient text
    # Returns a list of structured ingredient data in dictionary form
    def Parse(self, ingredients):

        resultDict = []
        idInt = -1
        idString = ""

        for ingredientStr in ingredients:

            ingredientNameStartIndex = 0

            #############################
            ####    Ingredient ID    ####
            #############################

            idInt = idInt + 1
            idString = str(idInt)


            #############################
            ####    Parse Amounts    ####
            #############################

            # Matching fractions
            fractionIndices = []
            matchResultsIt = self.fractionPattern.finditer(ingredientStr)
            for matchResult in matchResultsIt:
                fractionIndices.append(matchResult.span(0))
                # print "fraction: " + matchResult.group(0)

            # Matching decimals
            decimalIndices = []
            matchResultsIt = self.decimalPattern.finditer(ingredientStr)
            for matchResult in matchResultsIt:
                decimalIndices.append(matchResult.span(0))
                # print "decimal: " + matchResult.group(0)

            # Matching integers
            integerIndices = []
            matchResultsIt = self.integerPattern.finditer(ingredientStr)
            for matchResult in matchResultsIt:
                integerIndices.append(matchResult.span(0))
                # print "integer: " + matchResult.group(0)

            # Matching words
            amountWordsIndices = []
            matchResultsIt = self.amountWordsPattern.finditer(ingredientStr)
            for matchResult in matchResultsIt:
                amountWordsIndices.append(matchResult.span(0))
                # print "words: " + matchResult.group(0)

            # TODO: Be able to understand results from multiple parsers
            # # Concatenate all index tuples
            # amountIndices = []
            # if len(fractionIndices) > 0:
            #     for i in fractionIndices:
            #         amountIndices.append(i)
            # if len(decimalIndices) > 0:
            #     for i in decimalIndices:
            #         amountIndices.append(i)
            # if len(integerIndices) > 0:
            #     for i in integerIndices:
            #         amountIndices.append(i)
            # if len(amountWordsIndices) > 0:
            #     for i in amountWordsIndices:
            #         amountIndices.append(i)
            #
            # # Order the index tuples
            # amountIndices = sorted(amountIndices, key=lambda item: item[0])
            # print amountIndices


            # Priority order: Fractions, Decimals, Integers, Words
            # TODO: instead of using this priority, maybe we can do it based on the type that comes first

            amountString = ""

            if len(fractionIndices) > 0:
                (start, end) = self.StartAndEndOfLongestTuple(fractionIndices)
                amountString = ingredientStr[start:end]
                ingredientNameStartIndex = end

            elif len(decimalIndices) > 0:
                (start, end) = self.StartAndEndOfLongestTuple(decimalIndices)
                amountString = ingredientStr[start:end]
                ingredientNameStartIndex = end

            elif len(integerIndices) > 0:
                (start, end) = self.StartAndEndOfLongestTuple(integerIndices)
                amountString = ingredientStr[start:end]
                ingredientNameStartIndex = end

            elif len(amountWordsIndices) > 0:
                # use the first one instead of the longest one
                (start, end) = self.StartAndEndOfLongestTuple([amountWordsIndices[0]])
                amountString = ingredientStr[start:end]
                ingredientNameStartIndex = end

            else:
                amountString = "1"


            ###########################
            ####    Parse Units    ####
            ###########################

            keepSearching = True
            unitString = ""
            unitStringEnd = -1

            for unitKey in self.unitsMapper:
                if not keepSearching:
                    break
                unitTextList = self.unitsMapper[unitKey]
                for unitText in unitTextList:
                    unitText = "[^a-zA-Z]+" + unitText + "[^a-zA-Z]+"
                    matchResult = re.search(unitText, ingredientStr)
                    if matchResult:
                        unitString = unitKey
                        keepSearching = False
                        unitStringEnd = matchResult.end(0)
                        break

            if not keepSearching:
                ingredientNameStartIndex = unitStringEnd


            ###########################
            ####    Parse Names    ####
            ###########################

            ingredientNameString = ""
            ingredientNameString = ingredientStr[ingredientNameStartIndex:]


            ###########################
            ####    Create Dict    ####
            ###########################

            currDict = {
                "id": idString,
                "amount": amountString,
                "unit": unitString,
                "name": ingredientNameString
            }

            resultDict.append(currDict)

        return resultDict




############    TESTING    ################

# testIngredients = ["1 pound carrots, thinly sliced",
#                    "20 tablespoons fresh lime juice, plus lime wedges for serving",
#                    "Kosher salt and freshly ground pepper",
#                    "Pinch of ground cinnamon",
#                    "1/3 cup roughly chopped fresh mint",
#                    "2 1/4 cup sliced almonds",
#                    "1 cup flour",
#                    "one cup flour",
#                    "1 1/2 cups flour",
#                    "1.0 cup flour",
#                    "1.5 cups flour",
#                    "1 2/3 cups flour",
#                    "1 (28 ounce) can crushed tomatoes",
#                    "2 (28 ounce) can crushed tomatoes",
#                    "3 28 ounce can crushed tomatoes",
#                    "one 28 ounce can crushed tomatoes",
#                    "two five-ounce can crushed tomatoes",
#                    "two 28 ounce cans crushed tomatoes",
#                    "three 28 ounce cans crushed tomatoes",
#                    "1/2 cups flour",
#                    ".25 fl. oz. flour",
#                    "fl. oz. flour",
#                    "12oz tequila"]
#
# parser = MeasurementParser()
# print parser.Parse(testIngredients)