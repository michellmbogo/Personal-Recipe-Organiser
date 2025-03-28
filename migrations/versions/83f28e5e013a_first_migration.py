"""first migration

Revision ID: 83f28e5e013a
Revises: 
Create Date: 2025-03-12 23:43:38.534024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83f28e5e013a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('author_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('author_id')
    )
    op.create_table('categories',
    sa.Column('category_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('category_id')
    )
    op.create_table('ingredients',
    sa.Column('ingredient_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.Column('unit', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('ingredient_id')
    )
    op.create_table('recipes',
    sa.Column('recipe_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('cooking_time', sa.Integer(), nullable=True),
    sa.Column('servings', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.author_id'], ),
    sa.PrimaryKeyConstraint('recipe_id')
    )
    op.create_table('recipe_categories',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'category_id')
    )
    op.create_table('recipe_ingredients',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('ingredient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.ingredient_id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ),
    sa.PrimaryKeyConstraint('recipe_id')
    )
    op.create_table('recipe_nutrition',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('calories', sa.Integer(), nullable=True),
    sa.Column('fat', sa.Float(), nullable=True),
    sa.Column('protein', sa.Float(), nullable=True),
    sa.Column('carbs', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ),
    sa.PrimaryKeyConstraint('recipe_id')
    )
    op.create_table('steps',
    sa.Column('step_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('step_number', sa.Integer(), nullable=True),
    sa.Column('instruction', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ),
    sa.PrimaryKeyConstraint('step_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('steps')
    op.drop_table('recipe_nutrition')
    op.drop_table('recipe_ingredients')
    op.drop_table('recipe_categories')
    op.drop_table('recipes')
    op.drop_table('ingredients')
    op.drop_table('categories')
    op.drop_table('authors')
    # ### end Alembic commands ###
