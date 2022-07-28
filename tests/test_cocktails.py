import unittest.mock as mock
import pytest

from cocktail.cocktails import gatherPossibleDrinksForEachIngredient, findCommonCocktails, suggestCocktails


@pytest.fixture
def fake_input():
    with mock.patch('cocktail.cocktails.input') as m:
        yield m


def test_possible_cocktails_from_ingredients(fake_input):
    """
    GIVEN a user who isn't logged in
    WHEN the user tries to access a page that they do not have access to
    THEN check if the user is being redirected to the sign in page instead
    """
    fake_input.return_value = ['7-up', 'Salt']
    assert gatherPossibleDrinksForEachIngredient(fake_input.return_value) == \
        ['69 Special', 'Apple Slammer', 'Radler', 'Tequila Slammer', 'Egg-Nog - Classic Cooked', 'Lassi Khara', 'Microwave Hot Cocoa', 'Salty Dog']


def test_common_cocktails(fake_input):
    fake_input.return_value = ['Gin Toddy', 'Gin Fizz', 'Gin Toddy']
    assert findCommonCocktails(fake_input.return_value) == {'Gin Toddy'}


def test_suggested_cocktail_with_multiple_ingredients(fake_input):
    fake_input.return_value = 'Gin,Water,Powdered sugar,Lemon peel'
    assert suggestCocktails(fake_input.return_value) == ['Gin Toddy']


def test_suggested_cocktail_with_multiple_ingredients_different_order(fake_input):
    fake_input.return_value = 'Lemon peel,Powdered sugar,Gin,Water'
    assert suggestCocktails(fake_input.return_value) == ['Gin Toddy']


def test_suggested_cocktail_with_ingredients_negative(fake_input):
    fake_input.return_value = 'Gin,Water,Powdered sugar'
    assert suggestCocktails(fake_input.return_value) is None


def test_suggested_cocktail_with_single_ingredient(fake_input):
    fake_input.return_value = 'Lemon peel'
    assert suggestCocktails(fake_input.return_value) is None


def test_suggested_cocktails_with_multiple_ingredients(fake_input):
    fake_input.return_value = 'Lemon peel,Powdered sugar,Gin,Water,Carbonated water,Lemon'
    actual = suggestCocktails(fake_input.return_value)
    expected = ['Gin Toddy', 'Gin Fizz']
    assert set(actual) == set(expected)
