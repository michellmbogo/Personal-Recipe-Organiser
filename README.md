# Personal Recipe Organiser
The Personal Recipe Organiser is a user-friendly application that helps you manage your cooking collection effortlessly. You can easily add new recipes, categorize them by mealtype,cuisine and difficulty or search for specific recipes when needed. Additionally, the app allows you to delete recipes you no longer need, keeping your recipe collection organized and clutter-free. Perfect for home chefs looking to streamline their cooking experience!


## Features

- View Recipe : This feature enables one to vie the recipes they inputed.


- Recipe Entry :feature allows users to add new recipes into the system. Users can input relevant information about each recipe.


- List Recipes : This feature list all the recipes that have been added to the system.
- Categorisation: allows users to sort and group their recipes based on different categories.
- Search : The Search feature allows users to quickly locate a recipe by entering Title, Cuisine or meal type .
- Delete: The Delete feature allows users to remove recipes from their collection if the recipe is no longer needed.
- Updating : Allows users to update the recipe's title, description, cooking time, servings,mealtype, cuisine and difficulty fields.

## Installation

 ### Prerequisites

- Python 3.x
- pipenv (for virtual environment and dependency management)
- SQLite (built-in with Python, but required for ORM functionality)
- SQLAlchemy (for ORM database management)
- Click (for building the CLI interface)

## Steps to Install

1. *Clone the Repository*:
~~~bash
git clone git@github.com:michellmbogo/Personal-Recipe-Organiser.git
~~~
2. *Navigate into the directory *:
~~~bash
cd Personal-Recipe-Organiser
~~~

3. *Create a virtual environment and install dependencies* :
~~~bash
python -m venv env
source env/bin/activate
~~~

4. *Install necessary Python packages:*:
~~~bash
pipenv install sqlalchemy
pipenv install click  # For CLI handling
~~~

5. *Set up the database*:
~~~bash
python lib/models/init_db.py
~~~
6. *Run the application*:
~~~bash
python lib/cli.py
~~~

## Usage
Once the program is running, use the following to run:

## Recipe Commands

 1. *Add Recipe*:
   ~~~bash
    python main.py add-recipe
~~~
 2. *List Recipes*:
   ~~~bash
    python main.py list-recipes
~~~
 3. *View Recipe*:
   ~~~bash
    python main.py view-recipe ID

    eg. python main.py view-recipe 16
~~~
 4. *Search Recipe*:
   ~~~bash
    python main.py search-recipes
~~~

 5. *Delete Recipe*:
   ~~~bash
    python main.py delete-recipe ID

    eg. python main.py delete-recipe 16
~~~

 6. *Update Recipe*:
   ~~~bash
    python main.py update-recipe ID --field to be updted "new update"

    eg python main.py update-recipe 16 --description "This a meal that is common among the masaai community in kenya"
~~~
 
 ## Ingredient Commands:
 
1. *Add Ingredient*:
   ~~~bash
    python main.py add-ingredient
~~~
 2. *List Ingredients*:
   ~~~bash
    python main.py list-ingredients
~~~
 3. *View Ingredient*:
   ~~~bash
    python main.py view-ingredient ID

    eg. python main.py view-ingredient 16
~~~
 
 5. *Delete Ingredient*:
   ~~~bash
    python main.py delete-ingredient ID

    eg. python main.py delete-ingredient 16
~~~

 6. *Update Ingredient*:
   ~~~bash
    python main.py update-ingredient ID --field to be updted "new update"

    eg python main.py update-ingredient 16 --name "Chicken"
~~~

 ## Step Commands:

 1. *Add Step*:
   ~~~bash
    python main.py add-step
~~~
 2. *List Steps*:
   ~~~bash
    python main.py list-steps
~~~
 3. *View Step*:
   ~~~bash
    python main.py view-step ID

    eg. python main.py view-step 16
~~~

 5. *Delete Step*:
   ~~~bash
    python main.py delete-step ID

    eg. python main.py delete-step 16
~~~

 6. *Update Step*:
   ~~~bash
    python main.py update-step ID --field to be updted "new update"

    eg python main.py update-recipe 16 --instruction "Add salt to taste"
~~~

 
## Contribution
Contributions are welcome! Please follow this steps
1. **Fork the repository**

2. **Create a new branch**
   ~~~bash
   git checkout -b feature/yourFeature
   ~~~
3. **Commit your Changes**
   ~~~bash
   git commit -m "Add a new feature"
   ~~~
4. ** push to the branch**
  ~~~bash
   git push origin feature/YourFeatue
   ~~~
5. **Open a pull request**

## License

Distributed under the MIT license

## Contact

Name : Michell mbogo
Email : michellwambui.m@gmail.com