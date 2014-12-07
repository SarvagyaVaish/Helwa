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
    return false;
}
