
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey,Table
from sqlalchemy.orm import relationship,declarative_base

# Define the base class for declarative models
Base = declarative_base()

# An association table that links Recipe and category
recipe_categories_association = Table('recipe_categories', Base.metadata,
                                      Column('recipe_id',ForeignKey('recipes.recipe_id'),primary_key=True),
                                      Column('category_id',ForeignKey('categories.category_id'),primary_key=True))

recipe_ingredients_association = Table('recipe_ingredients', Base.metadata,
                                      Column('recipe_id',ForeignKey('recipes.recipe_id'),primary_key=True),
                                       Column('ingredient_id',ForeignKey('ingredients.ingredient_id'), nullable=False))

class Author(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    bio = Column(Text)

    #  one to many relationship with recipe
    recipes = relationship("Recipe", back_populates="author")


class Recipe(Base):
    __tablename__ = 'recipes'
    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    cooking_time = Column(Integer)
    servings = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.author_id'))

    # Relationships
    author = relationship("Author", back_populates="recipes")
    RecipeNutrition = relationship("RecipeNutrition", uselist=False, back_populates="recipe")
    steps = relationship("Step", back_populates="recipe")
    # recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe")
    categories = relationship("Category",
                              secondary=recipe_categories_association, back_populates="recipes")
    ingredients = relationship("Ingredient",
                              secondary=recipe_ingredients_association, back_populates="recipes")
   
class RecipeNutrition(Base):
    __tablename__ = 'recipe_nutrition'
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), primary_key=True)
    calories = Column(Integer)
    fat = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    
    # one to one relationship with recipe
    recipe = relationship("Recipe", back_populates="RecipeNutrition")

class Ingredient(Base):
    __tablename__ = 'ingredients'
    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    quantity = Column(Float)
    unit = Column(String)

    #  many to many relationship with recipe
    recipes = relationship("Recipe",
                              secondary=recipe_ingredients_association, back_populates="ingredients")

class Step(Base):
    __tablename__ = 'steps'
    step_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), nullable=False)
    step_number = Column(Integer)
    instruction = Column(Text, nullable=False)
    
    # one to many relationship with recipe
    recipe = relationship("Recipe", back_populates="steps")

class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    #  many to many relationship with recipe
    recipes = relationship("Recipe",
                              secondary=recipe_categories_association, back_populates="categories")







    