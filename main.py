from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry
from models import Recipe,Ingredient,Step
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
def add_recipe(title,description,cooking_time,servings,num_ingredients, num_steps ,meal_type,cuisine,difficulty):
    session=Session()
    recipe=Recipe(title=title, description=description, cooking_time=cooking_time, servings=servings,meal_type=meal_type, cuisine=cuisine ,difficulty=difficulty) 

    # for adding a new recipe to the data base
    session.add(recipe) 
    # for saving recipe to the data base
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
        
        
        
        if recipe.steps:
            click.echo("Steps:")
            for step in sorted(recipe.steps, key=lambda s: s.step_number):
                click.echo(f"  {step.step_number}. {step.instruction}")
        else:
            click.echo("No steps available.")
        
        if recipe.ingredients:
            click.echo("Ingredients:")
            for ri in recipe.ingredients:
                click.echo(f"  {ri.quantity} {ri.unit} of {ri.name}")
        else:
            click.echo("No ingredients added.")
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
    session = Session()
    """Delete recipe steps"""
    rows_deleted = session.query(Step).filter_by(recipe_id=recipe_id).delete()

        
    session.commit()

    if rows_deleted > 0:
        print(f"Successfully deleted {rows_deleted} step(s) for recipe with ID: {recipe_id}")
    else:
        print(f"No steps found for recipe with ID: {recipe_id}")
    
    """Delete a recipe from the database."""
    recipe = session.query(Recipe).get(recipe_id)
    if recipe:
        session.delete(recipe)
        session.commit()
        click.echo("Recipe deleted successfully!")
    else:
        click.echo("Recipe not found.")

 # updating recipe 
@click.command()
@click.argument('recipe_id', type=int)
@click.option('--title', type=str, help="Update the recipe's title")
@click.option('--description', type=str, help="Update the recipe's description")
@click.option('--cooking_time', type=int, help="Update the cooking time")
@click.option('--servings', type=int, help="Update the number of servings")
@click.option('--meal_type', type=str, help="Update the meal type")
@click.option('--cuisine', type=str, help="Update the cuisine")
@click.option('--difficulty', type=str, help="Update the difficulty")
def update_recipe(recipe_id, title, description, cooking_time, servings, meal_type, cuisine, difficulty):
    """Update a recipe's general information."""
    # Fetch the recipe from the database
    session = Session()

    recipe = session.query(Recipe).filter_by(recipe_id=recipe_id).first()

    if not recipe:
        click.echo(f"Recipe with ID {recipe_id} not found.")
        return

    # Update recipe fields if provided
    if title:
        recipe.title = title
    if description:
        recipe.description = description
    if cooking_time is not None:
        recipe.cooking_time = cooking_time
    if servings is not None:
        recipe.servings = servings
    if meal_type:
        recipe.meal_type = meal_type
    if cuisine:
        recipe.cuisine = cuisine
    if difficulty:
        recipe.difficulty = difficulty

    # Commit the changes
    session.commit()
    click.echo(f"Recipe with ID {recipe_id} has been updated.")




# # Add all commands to the CLI group

cli.add_command(add_recipe)
cli.add_command(list_recipes)
cli.add_command(view_recipe)
cli.add_command(search_recipes)
cli.add_command(delete_recipe)
cli.add_command(update_recipe)

if __name__ == "__main__":
    cli()