from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base,Recipe,RecipeCategory,RecipeNutrition,Author,Ingredient,RecipeIngredient,Step,Category,RecipeCategory

def main():

    # create the database engine 
    engine = create_engine('sqlite:///Personal-Recipe.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()


    def add_author():
    name = input("Enter author name: ")
    bio = input("Enter author bio: ")
    author = Author(name=name, bio=bio)
    session.add(author)
    session.commit()
    print("Author added successfully! ID:", author.author_id)

def add_recipe():
    title = input("Enter recipe title: ")
    description = input("Enter recipe description: ")
    try:
        cooking_time = int(input("Enter cooking time (in minutes): "))
    except ValueError:
        cooking_time = 0
    try:
        servings = int(input("Enter number of servings: "))
    except ValueError:
        servings = 0
    image = input("Enter image filename (optional): ")
    try:
        author_id = int(input("Enter author ID: "))
    except ValueError:
        print("Invalid author ID.")
        return

    recipe = Recipe(title=title, description=description, cooking_time=cooking_time,
                    servings=servings, image=image, author_id=author_id)
    session.add(recipe)
    session.commit()
    print("Recipe added successfully! Recipe ID:", recipe.recipe_id)

def list_recipes():
    recipes = session.query(Recipe).all()
    if recipes:
        print("Recipes:")
        for recipe in recipes:
            print(f"ID: {recipe.recipe_id}, Title: {recipe.title}, Description: {recipe.description}")
    else:
        print("No recipes found.")

def view_recipe():
    try:
        recipe_id = int(input("Enter recipe ID to view: "))
    except ValueError:
        print("Invalid recipe ID.")
        return

    recipe = session.query(Recipe).get(recipe_id)
    if recipe:
        print(f"\nRecipe ID: {recipe.recipe_id}")
        print(f"Title: {recipe.title}")
        print(f"Description: {recipe.description}")
        print(f"Cooking Time: {recipe.cooking_time} minutes, Servings: {recipe.servings}")
        print("Author:", recipe.author.name if recipe.author else "Unknown")
        # Display nutrition if available
        if recipe.nutrition:
            print(f"Nutrition - Calories: {recipe.nutrition.calories}, Fat: {recipe.nutrition.fat}, "
                  f"Protein: {recipe.nutrition.protein}, Carbs: {recipe.nutrition.carbs}")
        else:
            print("No nutrition information.")
        # Display steps in order
        if recipe.steps:
            print("Steps:")
            for step in sorted(recipe.steps, key=lambda s: s.step_number):
                print(f"  {step.step_number}. {step.instruction}")
        else:
            print("No steps available.")
        # Display ingredients with quantities
        if recipe.recipe_ingredients:
            print("Ingredients:")
            for ri in recipe.recipe_ingredients:
                print(f"  {ri.quantity} {ri.unit} of {ri.ingredient.name}")
        else:
            print("No ingredients added.")
        # Display categories
        if recipe.recipe_categories:
            print("Categories:")
            for rc in recipe.recipe_categories:
                print(f"  {rc.category.name}")
        else:
            print("No categories assigned.")
    else:
        print("Recipe not found.")

def delete_recipe():
    try:
        recipe_id = int(input("Enter recipe ID to delete: "))
    except ValueError:
        print("Invalid recipe ID.")
        return

    recipe = session.query(Recipe).get(recipe_id)
    if recipe:
        session.delete(recipe)
        session.commit()
        print("Recipe deleted successfully!")
    else:
        print("Recipe not found.")

    while True:
        print("\n=== Personal Recipe Organizer ===")
        print("1. Add Author")
        print("2. Add Recipe")
        print("3. List Recipes")
        print("4. View Recipe Details")
        print("5. Delete Recipe")
        print("6. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_author()
        elif choice == "2":
            add_recipe()
        elif choice == "3":
            list_recipes()
        elif choice == "4":
            view_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


