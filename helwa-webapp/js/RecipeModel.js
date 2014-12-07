var RecipeModel = (function () {

    // Private variable to hold the ingredients json object
    var m_Ingredients;

    // Private variable to hold the directions json object
    var m_Directions;


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

        // Ingredients Setter
        SetIngredients: function( ingredients ) {
            m_Ingredients = ingredients;
        }, 

        // Directions Setter
        SetDirections: function( directions ) {
            m_Directions = directions;
        },

        GetIngredients: function() {
            return m_Ingredients;
        }, 

        GetDirections: function() {
            return m_Directions;
        },

        UpdateIngredients: function(id, amount, unit, name) {
            // console.log(m_Ingredients);
            for (i in m_Ingredients) {
                if ( id == m_Ingredients[i]['id']) {
                    m_Ingredients[i]['amount'] = amount;
                    m_Ingredients[i]['unit'] = unit;
                    m_Ingredients[i]['name'] = name;
                }
            }
        },

        UpdateDirections: function(id, prettySentence) {
            // console.log(m_Directions);
            for (i in m_Directions) {
                if ( id == m_Directions[i]['id']) {
                    m_Directions[i]['prettySentence'] = prettySentence;
                }
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