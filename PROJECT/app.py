from flask import Flask, render_template
from views import main, result, search

def create_app() :
    app = Flask(__name__)

    app.register_blueprint(main.bp)
    app.register_blueprint(result.bp)
    app.register_blueprint(search.bp)

    @app.route('/')
    def home() :
        return render_template('main.html')

    return app

if __name__ == "__main__" : 
    app = create_app()
    app.run(debug=True)