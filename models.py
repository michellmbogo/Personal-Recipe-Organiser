import sys
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Define the base class for declarative models
Base = declarative_base()

# One-to-Many: Author and Recipes
class Author(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    bio = Column(Text)

    recipes = relationship("Recipe", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Author(id={self.author_id}, name={self.name})>"



class Recipe(Base):
    __tablename__ = 'recipes'
    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    cooking_time = Column(Integer)
    servings = Column(Integer)
    image = Column(String)
    author_id = Column(Integer, ForeignKey('authors.author_id'))

    # Relationships
    author = relationship("Author", back_populates="recipes")
    nutrition = relationship("RecipeNutrition", uselist=False, back_populates="recipe", cascade="all, delete-orphan")
    steps = relationship("Step", back_populates="recipe", cascade="all, delete-orphan")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    recipe_categories = relationship("RecipeCategory", back_populates="recipe", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Recipe(id={self.recipe_id}, title={self.title})>"


# One to One: Recipe and RecipeNutrition
class RecipeNutrition(Base):
    __tablename__ = 'recipe_nutrition'
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), primary_key=True)
    calories = Column(Integer)
    fat = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)

    recipe = relationship("Recipe", back_populates="nutrition")

    def __repr__(self):
        return f"<RecipeNutrition(recipe_id={self.recipe_id}, calories={self.calories})>"


# Ingredient and Many to Many via RecipeIngredient
class Ingredient(Base):
    __tablename__ = 'ingredients'
    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Ingredient(id={self.ingredient_id}, name={self.name})>"

class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'
    recipe_ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), nullable=False)
    quantity = Column(Float)
    unit = Column(String)

    recipe = relationship("Recipe", back_populates="recipe_ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")

    def __repr__(self):
        return (f"<RecipeIngredient(recipe_id={self.recipe_id}, "
                f"ingredient_id={self.ingredient_id}, quantity={self.quantity}, unit={self.unit})>")


# One-to-Many: Recipe → Steps
class Step(Base):
    __tablename__ = 'steps'
    step_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), nullable=False)
    step_number = Column(Integer)
    instruction = Column(Text, nullable=False)

    recipe = relationship("Recipe", back_populates="steps")

    def __repr__(self):
        return f"<Step(recipe_id={self.recipe_id}, step_number={self.step_number})>"


# Many-to-Many: Recipe ↔ Category via RecipeCategory
class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    recipe_categories = relationship("RecipeCategory", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.category_id}, name={self.name})>"

class RecipeCategory(Base):
    __tablename__ = 'recipe_categories'
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), primary_key=True)

    recipe = relationship("Recipe", back_populates="recipe_categories")
    category = relationship("Category", back_populates="recipe_categories")

    def __repr__(self):
        return f"<RecipeCategory(recipe_id={self.recipe_id}, category_id={self.category_id})>"




# Command-Line Interface Functions



    