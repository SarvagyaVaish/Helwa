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