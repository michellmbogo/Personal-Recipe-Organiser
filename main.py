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
@click.option('--title', help="Update the recipe's title")
@click.option('--description',help="Update the recipe's description")
@click.option('--cooking_time',help="Update the cooking time", type=int)
@click.option('--servings',help="Update the number of servings",type=int)
@click.option('--meal_type',help="Update the meal type")
@click.option('--cuisine', help="Update the cuisine")
@click.option('--difficulty',help="Update the difficulty")
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
# CRUD Operations for Ingredient Table

#add Ingredients
@cli.command()
@click.option('--name', prompt = 'Enter Ingredient name')
@click.option('--quantity', prompt = 'Enter Ingredient quantity', type=int)
@click.option('--unit', prompt = 'Enter Ingredient unit')


def add_ingredient(name, quantity, unit):
    session = Session()
    ingredient = Ingredient(name=name, quantity=quantity, unit=unit)

    session.add(ingredient)
    session.commit()

    click.echo("Added Ingredient")

#view Ingredient
@click.command()
@click.argument('ingredient_id', type=int)
def view_ingredient(ingredient_id):
    """View details of a specific ingredient by its ID."""
    session = Session()
    ingredient = session.get(Ingredient,ingredient_id)
    if ingredient:
        click.echo(f"Ingredient ID: {ingredient.ingredient_id}")
        click.echo(f"name: {ingredient.name}")
        click.echo(f"Quantity: {ingredient.quantity}")
        click.echo(f"Unit: {ingredient.unit}")
    else:
       click.echo ("Ingredient not found") 
#List Ingredients

@click.command()
def list_ingredients():
    """List all ingredients in the database."""
    session = Session()
    ingredients = session.query(Ingredient).all()
    if ingredients:
        click.echo("Ingredients:")
        for ingredient in ingredients:
            click.echo(f"ID: {ingredient.ingredient_id}, name: {ingredient.name}, quantity: {ingredient.quantity}, unit: {ingredient.unit}")
    else:
        click.echo("No ingredient found.")
        
#Updating Ingredients
@click.command()
@click.argument('ingredient_id', type=int)
@click.option('--name', help="Update the ingredient name")
@click.option('--unit',help="Update the ingredient unit")
@click.option('--quantity',help="Update the ingredient quantity", type=int)

def update_ingredient(ingredient_id, name, unit, quantity):

    session = Session()

    ingredient = session.query(Ingredient).filter_by(ingredient_id=ingredient_id).first()

    if not ingredient:
        click.echo(f"Ingredient with ID {ingredient_id} not found.")
        return

    # Update recipe fields if provided
    if name:
        ingredient.name = name
    if unit:
        ingredient.unit = unit
    if quantity is not None:
        ingredient.quantity = quantity
   
        
    # Commit the changes
    session.commit()
    click.echo(f"Ingredient with ID {ingredient_id} has been updated.")


# Deleting Ingredients
@click.command()
@click.argument('ingredient_id', type=int)
def delete_ingredient(ingredient_id):
    session = Session()
    
    """Delete an ingredient from the database."""
    ingredient = session.query(Ingredient).get(ingredient_id)
    if ingredient:
        session.delete(ingredient)
        session.commit()
        click.echo("Ingredient deleted successfully!")
    else:
        click.echo("Ingredient not found.")

# CRUD for Steps

# Add steps
@cli.command()
@click.option('--recipe_id', prompt = 'Enter recipe id')
@click.option('--step_number', prompt = 'Enter step number', type=int)
@click.option('--instruction', prompt = 'Enter step instruction')


def add_step(recipe_id, step_number, instruction):
    session = Session()
    step = Step(recipe_id = recipe_id, step_number=step_number, instruction=instruction)

    session.add(step)
    session.commit()

    click.echo("Added Step")

#view Step
@click.command()
@click.argument('step_id', type=int)
def view_step(step_id):
    """View details of a specific step by its ID."""
    session = Session()
    step = session.get(Step,step_id)
    if step:
        click.echo(f"Step ID: {step.step_id}")
        click.echo(f"step_number: {step.step_number}")
        click.echo(f"Instruction: {step.instruction}")
        click.echo(f"recipe_id: {step.recipe_id}")
    else:
       click.echo ("step not found") 

#List Steps

@click.command()
def list_steps():
    """List all steps in the database."""
    session = Session()
    steps = session.query(Step).all()
    if steps:
        click.echo("Steps:")
        for step in steps:
            click.echo(f"ID: {step.step_id}, recipe_id: {step.recipe_id}, instruction: {step.instruction}, step_number: {step.step_number}")
    else:
        click.echo("No step found.")

#Updating Ingredients
@click.command()
@click.argument('step_id', type=int)
@click.option('--step_number', help="Update the step number")
@click.option('--instruction',help="Update the step instruction")


def update_step(step_id, step_number, instruction, ):

    session = Session()

    step = session.query(Step).filter_by(step_id = step_id).first()

    if not step:
        click.echo(f"Step with ID {step_id} not found.")
        return

    # Update recipe fields if provided
    if step_number:
        step.step_number = step_number
    if instruction:
        step.instruction = instruction
    
    # Commit the changes
    session.commit()
    click.echo(f"Step with ID {step_id} has been updated.")

# Deleting Ingredients
@click.command()
@click.argument('step_id', type=int)
def delete_step(step_id):
    session = Session()
    
    """Delete a step from the database."""
    step = session.query(Step).get(step_id)
    if step:
        session.delete(step)
        session.commit()
        click.echo("Step deleted successfully!")
    else:
        click.echo("Step not found.")

# # Add all commands to the CLI group

cli.add_command(add_recipe)
cli.add_command(list_recipes)
cli.add_command(view_recipe)
cli.add_command(search_recipes)
cli.add_command(delete_recipe)
cli.add_command(update_recipe)
cli.add_command(add_ingredient)
cli.add_command(view_ingredient)
cli.add_command(list_ingredients)
cli.add_command(update_ingredient)
cli.add_command(delete_ingredient)
cli.add_command(add_step)
cli.add_command(view_step)
cli.add_command(list_steps)
cli.add_command(update_step)
cli.add_command(delete_step)

if __name__ == "__main__":
    cli()