from collections import defaultdict
from sys import stdout
from typing import List, Dict, Tuple, Union


def print_recipe(recipe) -> None:
    """Pretty print recipe, which is a dictionary whose keys are
    ingredients and whose values are their corresponding amounts.
    """
    for ingredient, amount in recipe.items():
        print(f"{ingredient}: {amount}")

def read_recipe(recipe_file_name) -> Dict[str, int]:
    """Read recipe file 'recipe_file_name', and return ingredients as a
    dictionary whose keys are ingredients and whose values are the
    corresponding amounts.
    """
    recipe = {}
    with open(recipe_file_name) as recipe_file:
        for line in recipe_file:
            line = line.strip()
            if line == "":
                continue
            ingredient, amount = line.split(",")
            recipe[ingredient.strip()] = int(amount.strip())
    return recipe

def write_recipe(recipe, recipe_file_name) -> None:
    """Write recipe to a file named recipe_file_name."""
    with open(recipe_file_name, "w") as recipe_file:
        for ingredient, amount in recipe.items():
            recipe_file.write(f"{ingredient},{amount}\n")

def read_fridge(fridge_file_name) -> Dict[str, int]:
    """Read fridge file 'fridge_file_name', and return the ingredients
    held in the given fridge as an ingredient=amount dictionary.
    """
    fridge = defaultdict(int)
    with open(fridge_file_name) as fridge_file:
        for line in fridge_file:
            line = line.strip()
            if line == "":
                continue
            ingredient, amount = line.split(",")
            ingredient, amount = ingredient.strip(), int(amount.strip())
            fridge[ingredient] += amount
    return dict(fridge)

def is_cookable(recipe_file_name, fridge_file_name) -> bool:
    """Return True if the contents of the fridge named fridge_file_name
    are sufficient to cook the recipe named recipe_file_name.
    """
    recipe = read_recipe(recipe_file_name)
    fridge = read_fridge(fridge_file_name)
    for ingredient, amount in recipe.items():
        if fridge.get(ingredient, 0) < amount:
            return False
    return True

def add_recipes(recipes) -> Dict[str, int]:
    """Return a dictionary representing the sum of all of
    the recipe dictionaries in recipes.
    """
    total = defaultdict(int)
    for recipe in recipes:
        for ingredient, amount in recipe.items():
            total[ingredient] += amount
    return dict(total)

def create_shopping_list(recipe_file_names, fridge_file_name) -> Dict[str, int]:
    """Return the shopping list (a dictionary of ingredients and
    amounts) needed to cook the recipes named in recipe_file_names,
    after the ingredients already present in the fridge named
    fridge_file_name have been used.
    """
    recipes = [read_recipe(recipe_file_name) for recipe_file_name in recipe_file_names]
    fridge = read_fridge(fridge_file_name)
    total_recipe = add_recipes(recipes)
    shopping_list = defaultdict(int)
    for ingredient, amount in total_recipe.items():
        shopping_list[ingredient] += amount - fridge.get(ingredient, 0)
    return {product: amount for product, amount in shopping_list.items() if amount > 0}

def read_market(market_filename) -> Dict[str, int]:
    """Return a dictionary mapping ingredients to their prices in
    millicents.
    """
    market = {}
    with open(market_filename) as market_file:
        for line in market_file:
            line = line.strip()
            if line == "":
                continue
            ingredient, price = line.split(",")
            market[ingredient.strip()] = int(price.strip())
    return market

def total_price(shopping_list, market_file_name) -> int:
    """Return the total price in millicents of the given shopping_list
    at the market named market_file_name.
    """
    market = read_market(market_file_name)
    total = 0
    for ingredient, amount in shopping_list.items():
        total += amount * market[ingredient]
    return total

def find_cheapest(shopping_list, market_file_names) -> Union[Tuple[str, int], None]:
    """Return the name of the market in market_file_names
    offering the lowest total price for the given shopping_list,
    together with the total price.
    """
    cheapest = None
    for market_file_name in market_file_names:
        price = total_price(shopping_list, market_file_name)
        if cheapest is None or price < cheapest[1]:
            cheapest = (str(market_file_name), price)
    return cheapest

def update_fridge(fridge_file_name, recipe_file_names, market_file_names, new_fridge_file_name) -> None:
    """Compute the shopping list for the given recipes after the
    ingredients in fridge fridge_file_name have been used; find the cheapest
    market; and write the new fridge contents to new_fridge_file_name.
    Print the shopping list, the cheapest market name, and the total
    amount to be spent at that market.
    """
    shopping_list = create_shopping_list(recipe_file_names, fridge_file_name)
    cheapest = find_cheapest(shopping_list, market_file_names)
    assert cheapest is not None, "No market found"
    cheapest_market, total_price = cheapest
    fridge = defaultdict(int, read_fridge(fridge_file_name))
    for ingredient, amount in shopping_list.items():
        fridge[ingredient] += amount
    write_recipe(fridge, new_fridge_file_name)
    print("Shopping list:")
    print_recipe(shopping_list)
    print(f"Market: {cheapest_market}")
    print(f"Total cost: {total_price}")
