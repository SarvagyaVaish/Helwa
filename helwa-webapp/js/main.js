$(document).ready(function(){

	// Save the ingredients and directions in the RecipeModel
	RecipeModel.SetIngredients(ingredients);
    RecipeModel.SetDirections(directions);

    // Populate the ingredients list
    DynamicHtmlGenerator.RepopulateIngredientsList(RecipeModel.GetIngredients());

    // Populate the directions list
    DynamicHtmlGenerator.RepopulateDirectionsList(RecipeModel.GetDirections());

}) 