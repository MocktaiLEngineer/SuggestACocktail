import requests
import json

search_by_ingredient_api = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={}"
search_by_cocktail_api = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s={}"


# Helper functions
def queryIngredientsForCocktail(cocktails, input_ingredients):
    possible_drinks = []
    for cocktail in cocktails:
        res = requests.get(search_by_cocktail_api.format(cocktail))
        cocktail_json_res = json.loads(res.text)
        cocktail_ingredients = {value for key, value in cocktail_json_res['drinks'][0].items() if "strIngredient" in key and value is not None}
        if cocktail_ingredients <= input_ingredients:
            print("{}".format(cocktail))
            possible_drinks.append(cocktail)

    return possible_drinks


def gatherPossibleDrinksForEachIngredient(inputIngredients):
    # Step 1 - Gather all possible drinks that can be made for each of the ingredient
    drinks = []
    for ingredient in inputIngredients:
        res = requests.get(search_by_ingredient_api.format(ingredient))
        cocktail_json_res = json.loads(res.text)
        for cocktail in cocktail_json_res['drinks']:
            drinks.append(cocktail['strDrink'])

    return drinks


def findCommonCocktails(drinks):
    # Step 2 - Common cocktails
    seen = set()
    common_cocktails = {x for x in drinks if x in seen or seen.add(x)}
    return common_cocktails


def possibleCocktails(input_ingredients_set, drinks, common_cocktails):
    # Step 3 - Query the ingredients for each cocktail
    if len(common_cocktails) >= 1:
        possible_drinks = queryIngredientsForCocktail(common_cocktails, input_ingredients_set)
    else:
        possible_drinks = queryIngredientsForCocktail(drinks, input_ingredients_set)

    if len(possible_drinks) == 0:
        print("No cocktails can be made with the given ingredients")
        return None
    else:
        return possible_drinks


def suggestCocktails(inputIngredients):
    inputIngredients = inputIngredients.split(",")
    input_ingredients_set = set(inputIngredients)
    drinks = gatherPossibleDrinksForEachIngredient(inputIngredients)
    common_cocktails = findCommonCocktails(drinks)
    possible_drinks = possibleCocktails(input_ingredients_set, drinks, common_cocktails)
    return possible_drinks


if __name__ == "__main__":
    inputIngredients = input("Give a comma separated list of ingredients:")
    suggestCocktails(inputIngredients)
