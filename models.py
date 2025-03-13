
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey,Table
from sqlalchemy.orm import relationship,declarative_base

# Define the base class for declarative models
Base = declarative_base()

# An association table that links Recipe and Category with NOT NULL foreign keys
recipe_categories_association = Table(
    'recipe_categories', Base.metadata,
    # a primary key that enables many to many relationship
    Column('id', Integer, primary_key=True, autoincrement=True), 
    Column('recipe_id', Integer, ForeignKey('recipes.recipe_id'), nullable=False),  
    Column('category_id', Integer, ForeignKey('categories.category_id'), nullable=False)  
)

# Association table that links Recipe and Ingredient with NOT NULL foreign keys
recipe_ingredients_association = Table(
    'recipe_ingredients', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, ForeignKey('recipes.recipe_id'), nullable=False),  # Foreign key to recipes table, NOT NULL
    Column('ingredient_id', Integer, ForeignKey('ingredients.ingredient_id'), nullable=False)  # Foreign key to ingredients table, NOT NULL
)


class Recipe(Base):
    __tablename__ = 'recipes'
    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    cooking_time = Column(Integer)
    servings = Column(Integer)
    meal_type = Column(Text)
    cuisine = Column(Text)
    difficulty = Column(Text)

    # Relationships
    steps = relationship("Step", back_populates="recipe")
    categories = relationship("Category",
                              secondary=recipe_categories_association, back_populates="recipes")
    ingredients = relationship("Ingredient",
                              secondary=recipe_ingredients_association, back_populates="recipes")
   

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







    