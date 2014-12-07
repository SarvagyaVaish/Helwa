import ast
import re
import pprint

class Recipe:
    m_DirectionsList = [
        {
        'id': 1,
        'sentence': "Preheat/NNP the/DT broiler/NN ./."
        },
        {
        'id': 1,
        'sentence': "Lightly/RB oil/NN the/DT broiler/NN pan/NN ./."
        },
        {
        'id': 1,
        'sentence': "Toss/NNP the/DT carrots/NNS with/IN 1/CD tablespoon/NN olive/JJ oil/NN in/IN a/DT bowl/NN ,/, then/RB spread/VB out/RP on/IN one/CD side/NN of/IN the/DT pan/NN ./."
        },
        {
        'id': 1,
        'sentence': "Broil/NNP until/IN the/DT carrots/NNS begin/VBP to/TO soften/VB ,/, 2/CD to/TO 3/CD minutes.Meanwhile/JJ ,/, whisk/NN 2/CD tablespoons/NNS olive/JJ oil/NN ,/, the/DT honey/NN ,/, mustard/NN and/CC 1/CD tablespoon/NN lime/NN juice/NN in/IN a/DT small/JJ bowl/NN ./."
        },
        {
        'id': 1,
        'sentence': "Brush/NNP the/DT tops/NNS and/CC sides/NNS of/IN the/DT salmon/NN with/IN the/DT glaze/NN ./."
        },
        {
        'id': 1,
        'sentence': "Put/NNP the/DT salmon/NN ,/, skin-side/JJ down/IN ,/, on/IN the/DT other/JJ side/NN of/IN the/DT broiler/NN pan/NN next/IN to/TO the/DT carrots/NNS and/CC season/NN with/IN salt/NN and/CC pepper/NN ./."
        },
        {
        'id': 1,
        'sentence': "Broil/NNP until/IN the/DT salmon/NN is/VBZ golden/VBN brown/RP and/CC just/RB cooked/VBD through/IN and/CC the/DT carrots/NNS are/VBP crisp-tender/JJ ,/, 5/CD to/TO 7/CD minutes ./."
        },
        {
        'id': 1,
        'sentence': "Whisk/JJ the/DT remaining/VBG 1/CD tablespoon/NN each/DT olive/JJ oil/NN and/CC lime/NN juice/NN ,/, the/DT coriander/NN ,/, cumin/NN ,/, cinnamon/NN ,/, mint/NN and/CC almonds/NNS in/IN a/DT bowl/NN ./."
        },
        {
        'id': 1,
        'sentence': "Add/NNP the/DT carrots/NNS and/CC toss/NN to/TO combine/VB ;/: season/NN with/IN salt/NN and/CC pepper/NN ./."
        },
        {
        'id': 1,
        'sentence': "Serve/NNP the/DT salmon/NN with/IN the/DT carrots/NNS and/CC lime/VB wedges/NNS ./."
        }
    ]

    m_SentencePattern = re.compile(r"(\w*)/VB")

    # Find the VB* in the direction sentences
    # For each found verb, add a node to the corresponding dictionary
    # Assumes that there already exists a list of direction dictionaries (m_DirectionsList)
    # Updates each direction dictionary with a list of action-nodes
    def ParseVerbsInDirections(self):

        for i in range(len(self.m_DirectionsList)):
            directionDict = self.m_DirectionsList[i]
            directionString = directionDict["sentence"]

            prettySentence = directionString
            prettySentence = re.sub(r'\/[A-Z]{2,3}|\/.|\/,','', prettySentence)

            print prettySentence

            directionDict['action-nodes'] = []

            matchResultsIt = self.m_SentencePattern.finditer(directionString)
            for matchResult in matchResultsIt:
                verb = matchResult.group(1)
                newActionNode = { "verb": verb }
                directionDict['action-nodes'].append(newActionNode)

            self.m_DirectionsList[i] = directionDict

        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.m_DirectionsList)

        return




############

r = Recipe()
r.ParseVerbsInDirections()