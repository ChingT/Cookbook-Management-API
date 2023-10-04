import os

import django

# Configure the Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.cookbook_management.settings")
django.setup()


from cookbook.models import Cookbook
from ingredient.models import Ingredient
from recipe.models import Recipe
from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    return user


def create_ingredient(name):
    ingredient = Ingredient.objects.create(name=name)
    return ingredient


def create_cookbook(title, author, description=""):
    cookbook = Cookbook.objects.create(
        title=title, author=author, description=description
    )
    return cookbook


def create_recipe(title, cookbook, author, difficulty, description, ingredients):
    recipe = Recipe.objects.create(
        title=title,
        cookbook=cookbook,
        author=author,
        difficulty=difficulty,
        description=description,
    )
    recipe.ingredients.set(ingredients)
    return recipe


def create_user_profile(user):
    user_profile = UserProfile.objects.create(user=user)
    return user_profile


if __name__ == "__main__":
    User.objects.exclude(id=1).delete()
    Ingredient.objects.all().delete()

    # Create users
    user1 = create_user("Peter", "0000")
    user2 = create_user("Alice", "0000")
    user3 = create_user("John", "0000")

    user_profile1 = create_user_profile(user1)
    user_profile2 = create_user_profile(user2)
    user_profile3 = create_user_profile(user3)

    # Create ingredients
    flour = create_ingredient("Flour")
    eggs = create_ingredient("Eggs")
    milk = create_ingredient("Milk")
    sugar = create_ingredient("Sugar")
    salt = create_ingredient("Salt")
    butter = create_ingredient("Butter")
    bacon = create_ingredient("Bacon")
    parmesan = create_ingredient("Parmesan Cheese")
    black_pepper = create_ingredient("Black Pepper")
    spaghetti = create_ingredient("Spaghetti")
    pepper = create_ingredient("Pepper")

    # Create cookbooks
    cookbook1 = create_cookbook(
        "Baking Delights", user1, "A cookbook for delicious baked goods."
    )
    cookbook2 = create_cookbook(
        "Healthy Eating", user2, "Discover healthy and nutritious recipes."
    )

    # Create recipes
    recipe1 = create_recipe(
        "Chocolate Cake",
        cookbook1,
        user1,
        Recipe.Difficulty.Hard,
        "A delicious chocolate cake recipe.",
        [flour, eggs, milk, sugar, butter],
    )

    recipe2 = create_recipe(
        "Pancakes",
        cookbook1,
        user1,
        Recipe.Difficulty.Easy,
        "Fluffy pancakes for breakfast.",
        [flour, eggs, milk, butter, sugar],
    )

    recipe3 = create_recipe(
        "Spaghetti Carbonara",
        cookbook2,
        user2,
        Recipe.Difficulty.Intermediate,
        "Classic Italian pasta dish.",
        [eggs, bacon, parmesan, black_pepper, spaghetti],
    )

    recipe4 = create_recipe(
        "Omelette",
        cookbook2,
        user3,
        Recipe.Difficulty.Intermediate,
        "Quick and simple omelette recipe.",
        [eggs, butter, salt, pepper],
    )
    print("Test data added successfully!")
