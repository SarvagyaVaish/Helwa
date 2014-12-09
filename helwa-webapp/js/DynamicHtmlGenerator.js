var DynamicHtmlGenerator = (function () {



    // 
    // Template Code For Reference
    // 
    // var myPrivateVar, myPrivateMethod;
    //
    // // A private counter variable
    // myPrivateVar = 0;
    //
    // // A private function which logs any arguments
    // myPrivateMethod = function( foo ) {
    //     console.log( foo );
    // };

    return {

        RepopulateIngredientsList: function( ingredients ) {

            // TODO: Use document.writes / templates to populate 
            //       a list of ingredients on the webpage

            // Delete existing list items
            $("#ingredients_placement").empty();

            $("#ingredientTemplate").tmpl(ingredients).appendTo("#ingredients_placement");

            // console.log(ingredients)
            for (i in ingredients) {
                $('#'+ingredients[i]['id']).popover({
                    placement : 'bottom',
                    content : '<form class="form-inline" id="' + ingredients[i]['id'] + '">' +
                                '<table class="table table-bordered"><tr>' + 
                                '<td><input type="text" class="form-control" id="amount' + ingredients[i]['id'] + '" value="' + ingredients[i]['amount'] + '"> </td>' + 
                                '<td><input type="text" class="form-control" id="unit'   + ingredients[i]['id'] + '" value="' + ingredients[i]['unit']   + '"> </td>' + 
                                '<td><input type="text" class="form-control" id="name'   + ingredients[i]['id'] + '" value="' + ingredients[i]['name']   + '"> </td>' + 
                                '<td><button type="button" class="btn btn-default updateIngredientButton" ' + 
                                'onClick=\'UpdateIngredient("' + ingredients[i]['id'] + 
                                '")\'>Save</button>' +
                                '</td></tr></table>'
                });
            }
        }, 


        RepopulateDirectionsList: function( directions ) {

            // TODO: Use document.writes / templates to populate 
            //       a list of directions on the webpage

            // Delete existing list items
            $("#directions_placement").empty();

            $("#directionTemplate").tmpl(directions).appendTo("#directions_placement");

            console.log(directions)
            for (i in directions) {
                $('#'+directions[i]['id']).popover({
                    placement : 'bottom',
                    content : '<form class="form-inline" id="' + directions[i]['id'] + '">' +
                                '<table class="table table-bordered"><tr>' + 
                                '<td><input type="text" size="50" class="form-control" id="prettySentence' + directions[i]['id'] + '" value="' + directions[i]['prettySentence'] + '"> </td>' + 
                                '<td><button type="button" class="btn btn-default updateIngredientButton" ' + 
                                'onClick=\'UpdateDirection("' + directions[i]['id'] + 
                                '")\'>Save</button>' +
                                '</td></tr></table>'
                });
            }
        }, 

        RepopulateGraph: function ( ingredients, directions ) {

            // TODO: Use the current list of ingredients and directions to construct a graph 
            //          and update the mermaid div
            // 
            
            // var verbNodes = [];

            var everyTwo = 0;
            var lastverb = "";
            var skipFirstWord = 0;
            // console.log(lastverb);

            // Count verbs
            var count = 0;
            for (i in directions) {
                for ( j in directions[i]['action-nodes']) {

                    count++;
                }
            }
            console.log(count);

            // Build verbs first            
            var verbNodes = "";
            var previousVerb = ""; 
            for (i in directions) {
                for (j in directions[i]['action-nodes']) {
                    if ( previousVerb == "" ) {
                        previousVerb = directions[i]['action-nodes'][j]['verb'];
                    } else {
                        var currentVerb = directions[i]['action-nodes'][j]['verb'];
                        verbNodes = verbNodes + previousVerb + '((' + previousVerb + '))' + 
                            '-->' + currentVerb + '((' + currentVerb + '))' + ';\n';
                        previousVerb = currentVerb;
                    }
                }
            }

            function GetIngredient(id) { 
                return id;
            }

            var previousId = -1;
            var ingredientNodes = "";
            var verbCounter = 0;
            for (i in directions) {
                for (j in directions[i]['action-nodes']) {
                    previousId = -1;
                    verbCounter = verbCounter + 1;

                    for (k in directions[i]['action-nodes'][j]['ingredientIds']) {
                        currentId = directions[i]['action-nodes'][j]['ingredientIds'][k];
                        if (previousId == -1) {
                            previousId = currentId;
                        }
                        else {
                            var previousIngredient = GetIngredient(previousId);
                            var currentIngredient = GetIngredient(currentId);
                            ingredientNodes = ingredientNodes + previousIngredient + 'v' + verbCounter + '(' + previousIngredient + ')' + 
                            '---' + currentIngredient + 'v' + verbCounter + '(' + currentIngredient + ');\n';
                            previousId = currentId;
                        }
                    }
                    
                    if (previousId != -1) {
                        // link the last ingredient to the current verb
                        var verb = directions[i]['action-nodes'][j]['verb']
                        var previousIngredient = GetIngredient(previousId);
                        ingredientNodes = ingredientNodes + previousIngredient + 'v' + verbCounter + '(' + previousIngredient + ')' + 
                        '-->' + verb + ';\n';
                    }
                }
            }


            
            console.log(">>>>>>> verbNodes: ");
            // console.log(verbNodes);

            var graphString = "graph LR;\n" + verbNodes + ingredientNodes;
            console.log(graphString);

            // Example structure. Circles are verbs, e.g. 
            //                                ingred1 --- ingred2 ---> ((verb))  
            //                                                               \ 
            //                          ingred3 --- ingred4 --- ingred5 ---> ((verb))
            //                                                               /
            //                                              ingred6 ---> ((verb))

            // graphString = 'graph LR;\n' +
            //                 'C-->F;\n' +
            //                 'F-->I;\n' +
            //                 'A---B;\n' +
            //                 'B-->C((C));\n' +
            //                 'D---E;\n' +
            //                 'E-->F((F));\n' +
            //                 'G---H;\n' +
            //                 'H-->I((I));';
            $('.mermaid').empty();
            $('.mermaid').html(graphString);
        }

        // 
        //  Template Code For Reference
        //        
        // // A public variable
        // myPublicVar: "foo",
        //
        // // A public function utilizing privates
        // myPublicFunction: function( bar ) {
        //
        //   // Increment our private counter
        //   myPrivateVar++;
        //
        //   // Call our private method using bar
        //   myPrivateMethod( bar );
        // }
    };

})();