# ------------------------------------------
# Build in modules
# ------------------------------------------
import os

# ------------------------------------------
# 3rd party modules (installation needed)
# ------------------------------------------
None
# ------------------------------------------
# Custom modules
# ------------------------------------------
None
#f

class Recipe:
    def __init__(self, name: str, ingredients: list, time: int, instructions: str):
        self.__name = name
        self.__ingredients = ingredients
        self.__time = time
        self.__instructions = instructions

    def __repr__(self):
        return f"Recipe(name='{self.name}', ingredients={self.ingredients}, time={self.time}, instructions='{self.instructions}')"

    @property
    def name(self):
        return self.__name

    @property
    def ingredients(self):
        return self.__ingredients

    @property
    def time(self):
        return self.__time

    @property
    def instructions(self):
        return self.__instructions

    @name.setter
    def name(self, new_name: str):
        # Name must be a string and has at least 3 characters
        if isinstance(new_name, str) and len(new_name) >= 3:
            self.__name = str(new_name)

    def __le__(self, another):
        return self.time <= another.time

    def __ge__(self, another):
        return self.time >= another.time

    def __lt__(self, another):
        return self.time < another.time

    def __gt__(self, another):
        return self.time > another.time

    def __eq__(self, another):
        return self.time == another.time


class RecipeBook:

    def __init__(self):
        self.__recipe_book = []

    def __str__(self) -> str:
        return "RecipeBook:" + "\n" + "\n".join([str(r) for r in self.__recipe_book])

    def add_recipe(self, new_recipe: Recipe) -> None:
        """
        Add new recipe to RecipeBook
        Parameters
        ----------
        new_recipe: Recipe type object

        Returns None
        -------
        """
        self.__recipe_book.append(new_recipe)

    def remove_recipe(self, recipe_to_remove: Recipe) -> None:
        """
        Remove recipe from RecipeBook
        Parameters
        ----------
        recipe_to_remove: Recipe type object

        Returns None
        -------
        """
        self.__recipe_book.remove(recipe_to_remove)

    def recipe_by_name(self, recipe_name: str):
        """
        Find recipe by name
        Parameters
        ----------
        recipe_name: the name of recipe

        Returns If found ->Recipe type object | If not found -> None
        -------
        """
        recipes = [r for r in self.__recipe_book if r.name == recipe_name]
        if len(recipes) == 0:
            return None
        else:
            return recipes[0]

    def recipes_containing_ingredients(self, ingredients: list) -> list:
        """
        Find all recipes that contains provided ingredients
        Parameters
        ----------
        ingredients: the list of ingredients

        Returns list of Recipe type objects
        -------
        """
        recipes = [r for r in self.__recipe_book if all(item in r.ingredients for item in ingredients)]
        if len(recipes) == 0:
            return []
        else:
            return recipes

    def recipes_within_time(self, searched_time: int) -> list:
        """
        Find all recipes that can be made within specified time
        Parameters
        ----------
        searched_time: Max time needed for recipe preparation

        Returns list of Recipe type objects
        -------
        """
        recipes = [r for r in self.__recipe_book if r.time <= searched_time]
        if len(recipes) == 0:
            return []
        else:
            return recipes

    def recipes_with_all_ingredients(self, ingredients: list) -> list:
        """
        Find all recipes that can be made using provided ingredients
        Parameters
        ----------
        ingredients: the list of ingredients

        Returns list of Recipe type objects
        -------
        """
        recipes = [r for r in self.__recipe_book if all(item in ingredients for item in r.ingredients)]
        if len(recipes) == 0:
            return []
        else:
            return recipes

    def all_recipes(self) -> list:
        """
        Returns A copy of list of Recipe type objects
        -------
        """
        return self.__recipe_book.copy()

    def cleer_recipes(self):
        """
        Clear RecipeBook list
        -------
        """
        self.__recipe_book = []


class UserInterface():

    def __init__(self) -> None:
        self.__recipebook = RecipeBook()
        self.storage_name = "recipes.txt"
        self.create_storage()
        self.upload_storage()

    def create_storage(self) -> None:
        """
        Create a storage file if not exists
        Returns
        -------
        """
        if not os.path.exists(self.storage_name):
            with open(self.storage_name, "w") as file:
                pass

    def delete_storage(self) -> None:
        """
        Remove storage file
        Returns None
        -------
        """
        os.remove(self.storage_name)

    def clear_memory(self) -> None:
        """
        Clear current RecipeBook memory and storage file.
        Returns None
        -------
        """
        self.delete_storage()
        self.__recipebook.cleer_recipes()
        print("Memory cleared")

    def add_recipe_to_storage(self, new_recipe: Recipe) -> None:
        """
        Add recipe to storage file
        Parameters
        ----------
        new_recipe: Recipe type object

        Returns None
        -------
        """
        # Create storage file if not exist
        self.create_storage()
        # Save information from Recipe object into string
        text_to_add = f"{new_recipe.name};{','.join(new_recipe.ingredients)};{new_recipe.time};{new_recipe.instructions}"
        # Save information in file
        with open(self.storage_name, "a") as file:
            file.write(text_to_add + '\n')

    def update_storage(self) -> None:
        """
        Update storage file using information in RecipeBook
        Returns None
        -------
        """
        self.delete_storage()
        # Add all recipe from RecipeBook to storage file
        for r in self.__recipebook.all_recipes():
            self.add_recipe_to_storage(r)

    def upload_storage(self) -> None:
        """
        Upload information from storage file to RecipeBook.
        Returns None
        -------
        """
        # Open storage file and read content
        with open(self.storage_name, 'r') as file:
            lines = file.readlines()

        # loop through every line
        for line in lines:
            # Skip empty lines and brake lines
            if line != "" and line != "\n":
                # Split information by ";"
                items = line.split(";")
                # Create Recipe object
                new_recipe = Recipe(items[0], items[1].split(","), int(items[2]), items[3])
                # Add to RecipeBook
                self.__recipebook.add_recipe(new_recipe)

    def help(self) -> None:
        """
        Print all commands available in Application
        Returns None
        -------
        """
        help_text = """Commands:
0 - Exit
1 - Add recipe
2 - Remove recipe
3 - Search recipe by name
4 - Search recipe by ingredients
5 - Search recipe by preparation time
6 - Search recipe by available ingredients
7 - Return all recipes
8 - Clear memory"""
        print(help_text)

    def execute(self) -> None:
        """
        Run application
        Returns None
        -------
        """
        print("Recipe book program")
        # Print available commands
        self.help()
        while True:
            command = input("Enter command:")
            if command == "0":
                break
            elif command == "1":
                self.add_recipe()
            elif command == "2":
                self.remove_recipe()
            elif command == "3":
                self.search_by_name()
            elif command == "4":
                self.search_recipe_by_ingredients()
            elif command == "5":
                self.search_recipe_by_preparation_time()
            elif command == "6":
                self.search_recipe_by_available_ingredients()
            elif command == "7":
                self.return_all_recipes()
            elif command == "8":
                self.clear_memory()
            else:
                self.help()

    def add_recipe(self) -> None:
        """
        Add new Recipe according to user information
        Returns None
        -------
        """
        # Get recipe name from user
        recipe_name = input("Enter recipe name:")
        # Find recipe in current RecipeBook
        recipe = self.__recipebook.recipe_by_name(recipe_name)
        # If recipe not found add it to RecipeBook
        if recipe is None:
            # Get recipe information from user
            recipe_ingredients = input("Enter recipe ingredients separated by comma:")
            recipe_cooking_time = input("Enter recipe cook time (min):")
            recipe_instructions = input("Enter recipe instructions:")
            # Set default value
            recipe_cooking_time_int = None
            try:
                # Try to convert to int
                recipe_cooking_time_int = int(recipe_cooking_time)
            except Exception as error_message:
                print("Time need to be integer number.")

            if recipe_cooking_time_int is not None:
                # Create Recipe object
                new_recipe = Recipe(recipe_name, recipe_ingredients.split(","), recipe_cooking_time_int,
                                    recipe_instructions)
                # Add recipe to storage and RecipeBook
                self.add_recipe_to_storage(new_recipe)
                self.__recipebook.add_recipe(new_recipe)
                print(f"Added recipe {recipe_name}")

        else:
            print("Recipe already exists")

    def remove_recipe(self) -> None:
        """
        Remove recipe from RecipeBook and storage
        Returns None
        -------
        """
        # Get recipe name from user
        recipe_name = input("Enter name of recipe to remove:")
        # Find recipe in current RecipeBook
        recipe = self.__recipebook.recipe_by_name(recipe_name)
        # If recipe found remove it from RecipeBook and storage
        if recipe is None:
            print(f"No recipe found with name {recipe_name}")
        else:
            self.__recipebook.remove_recipe(recipe)
            self.update_storage()
            print(f"Removed recipe {recipe_name}")

    def search_by_name(self) -> None:
        """
        Find recipe by name provided by user. If recipe found print Recipe information.
        Returns
        -------
        """
        # Get recipe name from user
        recipe_name = input("Enter recipe name to search:")
        # Find recipe in current RecipeBook
        recipe = self.__recipebook.recipe_by_name(recipe_name)
        # If recipe found print Recipe information
        if recipe is None:
            print(f"No recipe found with name {recipe_name}")
        else:
            print(f"Found recipe: {recipe}")

    def search_recipe_by_ingredients(self) -> None:
        """
        Find recipes by ingredients provided by user
        Returns None
        -------
        """
        # Get ingredients from user
        recipe_ingredients = input("Enter the ingredients of the recipe you're looking for, separated by commas:")
        # Find all recipes that contains provided ingredients
        recipes = self.__recipebook.recipes_containing_ingredients(recipe_ingredients.split(","))
        # If recipes found print them with recipe information
        if len(recipes) == 0:
            print(f"No recipe found with ingredients {recipe_ingredients.split(',')}")
        else:
            print(f"Found recipes with ingredients {recipe_ingredients.split(',')}: ")
            for item in recipes:
                print(item)

    def search_recipe_by_preparation_time(self) -> None:
        """
        Search all recipes that can be made within time provided by user.
        Returns None
        -------
        """
        # Get time from user
        recipe_time = int(input("Enter the preparation time of the recipe you're looking for (min):"))
        # Find all recipes that that can be made within provided time
        recipes = self.__recipebook.recipes_within_time(recipe_time)
        # If recipes found print them with recipe information
        if len(recipes) == 0:
            print(f"No recipe found with preparation time {recipe_time} min")
        else:
            print(f"Found recipes with preparation time {recipe_time} min: ")
            for item in recipes:
                print(item)

    def search_recipe_by_available_ingredients(self):
        """
        Find all recipes that can be made from provided ingredients
        Returns None
        -------
        """
        # Get ingredients from user
        recipe_ingredients = input("Enter the ingredients of the recipe you're looking for, separated by commas:")
        # Find all recipes that can be made from provided ingredients
        recipes = self.__recipebook.recipes_with_all_ingredients(recipe_ingredients.split(","))
        # If recipes found print them with recipe information
        if len(recipes) == 0:
            print(f"No recipe found with ingredients {recipe_ingredients.split(',')}")
        else:
            print(f"Found recipes with ingredients {recipe_ingredients.split(',')}: ")
            for item in recipes:
                print(item)

    def return_all_recipes(self) -> None:
        """
        Print all recipes
        Returns None
        -------
        """
        # Get recipes from RecipeBook
        recipes = self.__recipebook.all_recipes()
        # If recipes exist print them
        if len(recipes) == 0:
            print(f"No recipes found")
        else:
            print(f"Found recipes: ")
            for item in recipes:
                print(item)


if __name__ == "__main__":
    # Create Instance of App
    app = UserInterface()
    # Run App
    app.execute()
