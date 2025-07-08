from flask import Flask, render_template
from views import main, result, search
from dotenv import load_dotenv
import os, config

load_dotenv() 

def create_app() :
    app = Flask(__name__)

    app.config['API_KEY'] = os.getenv("API_KEY")
    app.secret_key = config.SECRET_KEY
    print("API_KEY from .env:", os.getenv("API_KEY"))
    app.register_blueprint(main.bp)
    app.register_blueprint(result.bp)
    app.register_blueprint(search.bp)
    @app.route('/')
    def root() :
        return render_template('main.html')

    return app

if __name__ == "__main__" : 
    app = create_app()
    app.run(debug=True)