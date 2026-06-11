from models import RecipeCategory
from exts import db

def init_recipe_category():
    categories = ['American','Chinese','Korean','Japanese','Mexican','Middle East','Indian','Others']
    category_models = [RecipeCategory(name = category) for category in categories]
    db.session.add_all(category_models)
    db.session.commit()
    print('Recipes inite successful!')