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

    // http://stackoverflow.com/questions/8999210/how-do-i-call-a-jquery-function-on-submitting-a-form

    return {

        RepopulateIngredientsList: function( ingredients ) {

            // TODO: Use document.writes / templates to populate 
            //       a list of ingredients on the webpage

            // Delete existing list items
            $("#ingredients_placement").empty();

            $("#ingredientTemplate").tmpl(ingredients).appendTo("#ingredients_placement");

            console.log(ingredients)
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