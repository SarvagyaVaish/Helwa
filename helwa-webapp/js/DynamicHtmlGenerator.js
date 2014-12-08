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
            
            var graphString = "graph LR;\n";    // init graph string
            // var verbNodes = [];
            var verbNodes = ""; //directions[0]['action-nodes'][0]['verb'];

            var everyTwo = 0;
            var lastverb = "";
            var skipFirstWord = 0;
            // console.log(lastverb);

            // Build verbs first
            for (i in directions) {
                // skipFistWord = (verbNodes == "") ? 1 : 0;
                for (j in directions[i]['action-nodes']) {
                    // console.log(j);
                    // console.log(directions[i]['action-nodes'].length - 1);
                    // if( j != directions[i]['action-nodes'].length){

                        // ######################################   BROKEN ################################### \\
                        if ( i == 0 && j == 0){
                            verbNodes = (everyTwo % 2 == 1 || i == directions.length-1  ? ';\n' : '-->' );
                            lastverb =  directions[i]['action-nodes'][j]['verb'];
                                    everyTwo = everyTwo + 1;
                        }
                        verbNodes = verbNodes + lastverb + (everyTwo % 2 == 1 || i == directions.length-1  ? ';\n' : '-->' ) + 
                                    directions[i]['action-nodes'][j]['verb'];
                                    // Messy ternary: put a connection or a newline for everyother verb
                                    //      In case you are at the last verb, just end it. 
                                    // TODO: Should we check for the second to last verb and just put the last three together?
                                    //      Or just attach it to the second to last verb?
                                    lastverb =  directions[i]['action-nodes'][j]['verb'];
                                    everyTwo = everyTwo + 1;
                    // }
                        // ######################################   BROKEN ################################### \\
                }
            }
            
            console.log(">>>>>>> verbNodes: ");
            console.log(verbNodes);

            // graphString = graphString + verbNodes;
            console.log(graphString);

            // Example structure. Circles are verbs, e.g. 
            //                                ingred1 --- ingred2 ---> ((verb))  
            //                                                               \ 
            //                          ingred3 --- ingred4 --- ingred5 ---> ((verb))
            //                                                               /
            //                                              ingred6 ---> ((verb))

            graphString = 'graph LR;\n' +
                            'C-->F;\n' +
                            'F-->I;\n' +
                            'A---B;\n' +
                            'B-->C((C));\n' +
                            'D---E;\n' +
                            'E-->F((F));\n' +
                            'G---H;\n' +
                            'H-->I((I));';
            $('.mermaid').append(graphString);
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