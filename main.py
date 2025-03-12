from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry
from models import Author,Recipe,RecipeNutrition,Ingredient,Step,Category
import click

registry = registry()

    # create the database engine 
engine = create_engine('sqlite:///Personal-Recipe.db')

SessionLocal = sessionmaker(bind=engine)

# creating a CLI using click
@click.group()
def cli():
    """
    CLI for  Personal Recipe Organizer.
    """
    pass

# command to add a new author.
@click.command()
@click.option('--name',prompt='Enter author name')
@click.option('--bio',prompt='Enter author bio')
def add_author(name,bio):
    session=SessionLocal()
    author=Author(name=name, bio=bio)

    # for adding a new author to the data base
    session.add(author) 
    # for saving author to the data base
    session.commit()
    click.echo(f"Author added successfully! ID: {author.name}")

    session.close()

# command to add a new recipe
@click.command()
@click.option('--title',prompt='Enter recipe title')
@click.option('--description',prompt='Enter recipe description')
@click.option('--cooking_time',prompt='Enter cooking time (in minutes)', type=int, default=0)
@click.option('--servings',prompt='Enter number of servings', type=int, default=0)
@click.option('--author_id',prompt='Enter author ID', type=int)
def add_recipe(title,description,cooking_time,servings,author_id):
    session=SessionLocal()
    recipe=Recipe(title=title, description=description, cooking_time=cooking_time, servings=servings, author_id=author_id)

    # for adding a new author to the data base
    session.add(recipe) 
    # for saving author to the data base
    session.commit()
    click.echo(f"Recipe added successfully! ID: {recipe.recipe_id}")

    session.close()

# @click.command()
# def list_recipes():
#     """List all recipes in the database."""
#     recipes = session.query(Recipe).all()
#     if recipes:
#         click.echo("Recipes:")
#         for recipe in recipes:
#             click.echo(f"ID: {recipe.recipe_id}, Title: {recipe.title}, Description: {recipe.description}")
#     else:
#         click.echo("No recipes found.")

# @click.command()
# @click.argument('recipe_id', type=int)
# def view_recipe(recipe_id):
#     """View details of a specific recipe by its ID."""
#     recipe = session.query(Recipe).get(recipe_id)
#     if recipe:
#         click.echo(f"\nRecipe ID: {recipe.recipe_id}")
#         click.echo(f"Title: {recipe.title}")
#         click.echo(f"Description: {recipe.description}")
#         click.echo(f"Cooking Time: {recipe.cooking_time} minutes, Servings: {recipe.servings}")
#         click.echo("Author:", recipe.author.name if recipe.author else "Unknown")
        
#         if recipe.nutrition:
#             click.echo(f"Nutrition - Calories: {recipe.nutrition.calories}, Fat: {recipe.nutrition.fat}, "
#                        f"Protein: {recipe.nutrition.protein}, Carbs: {recipe.nutrition.carbs}")
#         else:
#             click.echo("No nutrition information.")
        
#         if recipe.steps:
#             click.echo("Steps:")
#             for step in sorted(recipe.steps, key=lambda s: s.step_number):
#                 click.echo(f"  {step.step_number}. {step.instruction}")
#         else:
#             click.echo("No steps available.")
        
#         if recipe.recipe_ingredients:
#             click.echo("Ingredients:")
#             for ri in recipe.recipe_ingredients:
#                 click.echo(f"  {ri.quantity} {ri.unit} of {ri.ingredient.name}")
#         else:
#             click.echo("No ingredients added.")
        
#         if recipe.recipe_categories:
#             click.echo("Categories:")
#             for rc in recipe.recipe_categories:
#                 click.echo(f"  {rc.category.name}")
#         else:
#             click.echo("No categories assigned.")
#     else:
#         click.echo("Recipe not found.")

# @click.command()
# @click.argument('recipe_id', type=int)
# def delete_recipe(recipe_id):
#     """Delete a recipe from the database."""
#     recipe = session.query(Recipe).get(recipe_id)
#     if recipe:
#         session.delete(recipe)
#         session.commit()
#         click.echo("Recipe deleted successfully!")
#     else:
#         click.echo("Recipe not found.")

# @click.group()
# def cli():
#     """Personal Recipe Organizer CLI."""
#     pass

# # Add all commands to the CLI group
cli.add_command(add_author)
cli.add_command(add_recipe)
# cli.add_command(list_recipes)
# cli.add_command(view_recipe)
# cli.add_command(delete_recipe)

if __name__ == "__main__":
    cli()