from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry
from models import Author,Recipe,RecipeNutrition,Ingredient,Step,Category
import click

registry = registry()

    # create the database engine 
engine = create_engine('sqlite:///Personal-Recipe.db')

Session = sessionmaker(bind=engine)


# creating a CLI using click
@click.group()
def cli():
    """
    CLI for  Personal Recipe Organizer.
    """
    pass

# command to add a new recipe
@click.command()
@click.option('--title',prompt='Enter recipe title')
@click.option('--description',prompt='Enter recipe description')
@click.option('--cooking_time',prompt='Enter cooking time (in minutes)', type=int, default=0)
@click.option('--servings',prompt='Enter number of servings', type=int, default=0)
@click.option('--meal_type',prompt='Enter mealtype')
@click.option('--cuisine',prompt='Enter Cuisine')
@click.option('--difficulty',prompt='Enter Preparation Difficulty')
@click.option('--num_ingredients', prompt='Enter number of ingredients', type=int, default=0)
@click.option('--num_steps', prompt='Enter number of steps', type=int, default=0)
def add_recipe(title,description,cooking_time,servings,author_id,num_ingredients, num_steps ,meal_type,cuisine,difficulty):
    session=Session()
    recipe=Recipe(title=title, description=description, cooking_time=cooking_time, servings=servings, author_id=author_id ,meal_type=meal_type, cuisine=cuisine ,difficulty=difficulty) 

    # for adding a new author to the data base
    session.add(recipe) 
    # for saving author to the data base
    session.commit()

  # Add ingredients
    for i in range(num_ingredients):
        ingredient_name = click.prompt(f"Enter name of ingredient #{i+1}")
        quantity = click.prompt(f"Enter quantity for {ingredient_name}")
        unit = click.prompt(f"Enter unit for {ingredient_name}")
        
        ingredient = session.query(Ingredient).filter(Ingredient.name == ingredient_name).first()
        if not ingredient:
            ingredient = Ingredient(name=ingredient_name, quantity=quantity, unit=unit)
            session.add(ingredient)
            session.commit()  # Commit to generate an ID for the ingredient
        
            recipe.ingredients.append(ingredient)

    #    add steps
    for i in range(num_steps):
        step_instruction = click.prompt(f"Enter instruction for step #{i+1}")
        step = Step(recipe_id=recipe.recipe_id, step_number=i+1, instruction=step_instruction)
        session.add(step)
    
    session.commit()  # Save the ingredients and steps
    click.echo(f"Recipe '{recipe.title}' added successfully with ingredients and steps!")


    click.echo(f"Recipe added successfully! ID: {recipe.recipe_id}")

    session.close()

@click.command()
def list_recipes():
    """List all recipes in the database."""
    session = Session()
    recipes = session.query(Recipe).all()
    if recipes:
        click.echo("Recipes:")
        for recipe in recipes:
            click.echo(f"ID: {recipe.recipe_id}, Title: {recipe.title}, Description: {recipe.description}")
    else:
        click.echo("No recipes found.")

@click.command()
@click.argument('recipe_id', type=int)
def view_recipe(recipe_id):
    """View details of a specific recipe by its ID."""
    session = Session()
    recipe = session.get(Recipe,recipe_id)
    if recipe:
        click.echo(f"\nRecipe ID: {recipe.recipe_id}")
        click.echo(f"Title: {recipe.title}")
        click.echo(f"Description: {recipe.description}")
        click.echo(f"Cooking Time: {recipe.cooking_time} minutes")
        click.echo(f"Servings: {recipe.servings}")
        click.echo(f"Author:", recipe.author.name if recipe.author else "Unknown")
        
        if recipe.nutrition:
            click.echo(f"Nutrition - Calories: {recipe.nutrition.calories}, Fat: {recipe.nutrition.fat}, "
                       f"Protein: {recipe.nutrition.protein}, Carbs: {recipe.nutrition.carbs}")
        else:
            click.echo("No nutrition information.")
        
        if recipe.steps:
            click.echo("Steps:")
            for step in sorted(recipe.steps, key=lambda s: s.step_number):
                click.echo(f"  {step.step_number}. {step.instruction}")
        else:
            click.echo("No steps available.")
        
        if recipe.recipe_ingredients:
            click.echo("Ingredients:")
            for ri in recipe.recipe_ingredients:
                click.echo(f"  {ri.quantity} {ri.unit} of {ri.ingredient.name}")
        else:
            click.echo("No ingredients added.")
        
        if recipe.recipe_categories:
            click.echo("Categories:")
            for rc in recipe.recipe_categories:
                click.echo(f"  {rc.category.name}")
        else:
            click.echo("No categories assigned.")
    else:
        click.echo("Recipe not found.")

# Command to search recipes by a single string across title, cuisine, and meal_type
@click.command()
@click.option('--search_string', prompt='Enter search string (title, cuisine, or meal type)')
def search_recipes(search_string):
    """Search for recipes by title, cuisine, or meal type using a single string."""
    session = Session()
    query = session.query(Recipe)

    # Perform case-insensitive search on title, cuisine, or meal type
    query = query.filter(
        (Recipe.title.ilike(f"%{search_string}%")) |
        (Recipe.cuisine.ilike(f"%{search_string}%")) |
        (Recipe.meal_type.ilike(f"%{search_string}%"))
    )

    recipes = query.all()

    # Display search results
    if recipes:
        click.echo("Search Results:")
        for recipe in recipes:
            click.echo(f"ID: {recipe.recipe_id}, Title: {recipe.title}, Cuisine: {recipe.cuisine}, Meal Type: {recipe.meal_type}")
    else:
        click.echo("No recipes found matching your search criteria.")

    session.close()

@click.command()
@click.argument('recipe_id', type=int)
def delete_recipe(recipe_id):
    """Delete a recipe from the database."""
    session = Session()
    recipe = session.query(Recipe).get(recipe_id)
    if recipe:
        session.delete(recipe)
        session.commit()
        click.echo("Recipe deleted successfully!")
    else:
        click.echo("Recipe not found.")



# # Add all commands to the CLI group
cli.add_command(add_author)
cli.add_command(add_recipe)
cli.add_command(list_recipes)
cli.add_command(view_recipe)
cli.add_command(search_recipes)
cli.add_command(delete_recipe)

if __name__ == "__main__":
    cli()