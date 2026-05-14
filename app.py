from flask import Flask
from controllers.book_controller import book_blueprint
from error_handlers.error_handlers import register_error_handlers

app = Flask(__name__)
app.register_blueprint(book_blueprint, url_prefix='/api/books')
register_error_handlers(app)

if __name__ == '__main__':
    app.run(debug=True)
