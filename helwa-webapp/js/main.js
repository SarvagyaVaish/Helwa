$(document).ready(function(){

	// Save the ingredients and directions in the RecipeModel
	RecipeModel.SetIngredients(ingredients);
    RecipeModel.SetDirections(directions);

    // Populate the ingredients list
    DynamicHtmlGenerator.RepopulateIngredientsList(RecipeModel.GetIngredients());

    // Populate the directions list
    DynamicHtmlGenerator.RepopulateDirectionsList(RecipeModel.GetDirections());

})
	
function UpdateIngredient(id) {
    amount = $('#amount'+id).val();
    unit =   $('#unit'+id).val();
    name =   $('#name'+id).val();
	RecipeModel.UpdateIngredients(id, amount, unit, name);
	$('#'+id).popover('hide');

    // RePopulate the ingredients list
    DynamicHtmlGenerator.RepopulateIngredientsList(RecipeModel.GetIngredients());

    return false;
}

function UpdateDirection(id) {
    prettySentence = $('#prettySentence'+id).val();
    // console.log(prettySentence);
    RecipeModel.UpdateDirections(id, prettySentence);
    $('#'+id).popover('hide');

    // RePopulate the ingredients list
    DynamicHtmlGenerator.RepopulateDirectionsList(RecipeModel.GetDirections());

    return false;
}


