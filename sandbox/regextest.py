import re


resultString = '{"result": "Preheat/NNP the/DT broiler/NN ./. Lightly/RB oil/NN the/DT broiler/NN pan/NN ./. Toss/NNP the/DT carrots/NNS with/IN 1/CD tablespoon/NN olive/JJ oil/NN in/IN a/DT bowl/NN ,/, then/RB spread/VB out/RP on/IN one/CD side/NN of/IN the/DT pan/NN ./. Broil/NNP until/IN the/DT carrots/NNS begin/VBP to/TO soften/VB ,/, 2/CD to/TO 3/CD minutes.Meanwhile/JJ ,/, whisk/NN 2/CD tablespoons/NNS olive/JJ oil/NN ,/, the/DT honey/NN ,/, mustard/NN and/CC 1/CD tablespoon/NN lime/NN juice/NN in/IN a/DT small/JJ bowl/NN ./. Brush/NNP the/DT tops/NNS and/CC sides/NNS of/IN the/DT salmon/NN with/IN the/DT glaze/NN ./. Put/NNP the/DT salmon/NN ,/, skin-side/JJ down/IN ,/, on/IN the/DT other/JJ side/NN of/IN the/DT broiler/NN pan/NN next/IN to/TO the/DT carrots/NNS and/CC season/NN with/IN salt/NN and/CC pepper/NN ./. Broil/NNP until/IN the/DT salmon/NN is/VBZ golden/VBN brown/RP and/CC just/RB cooked/VBD through/IN and/CC the/DT carrots/NNS are/VBP crisp-tender/JJ ,/, 5/CD to/TO 7/CD minutes.Whisk/JJ the/DT remaining/VBG 1/CD tablespoon/NN each/DT olive/JJ oil/NN and/CC lime/NN juice/NN ,/, the/DT coriander/NN ,/, cumin/NN ,/, cinnamon/NN ,/, mint/NN and/CC almonds/NNS in/IN a/DT bowl/NN ./. Add/NNP the/DT carrots/NNS and/CC toss/NN to/TO combine/VB ;/: season/NN with/IN salt/NN and/CC pepper/NN ./. Serve/NNP the/DT salmon/NN with/IN the/DT carrots/NNS and/CC lime/VB wedges/NNS ./."}'

m = re.sub(r'\/\.\s*', '\n', 'Preheat/NNP the/DT broiler/NN ./. Lightly/RB oil/NN the/DT broiler/NN pan/NN ./.')

x = re.split('\n', m)
print x