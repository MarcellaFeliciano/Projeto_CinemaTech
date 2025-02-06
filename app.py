from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
# importa e registra o blueprint
#from controllers import user
#from models.users import User
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'muitodificil'

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()     

@app.route ('/')
def index ():
    return render_template ('index.html')

                                                                                        

#app.register_blueprint(user.bp)