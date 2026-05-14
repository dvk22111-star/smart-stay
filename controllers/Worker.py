from flask import Blueprint, request, jsonify
from dto.book_dto import BookDTO
from services.book_service import BookService
from repository.book_repository import BookRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.book import Base

engine = create_engine('sqlite:///books.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = BookRepository(session)
service = BookService(repo)

book_blueprint = Blueprint('books', __name__)

@book_blueprint.route('', methods=['POST'])
def add_book():
    dto = BookDTO(**request.get_json())
    service.add_book(dto)
    return jsonify({'message': 'Book added'}), 201

@book_blueprint.route('', methods=['GET'])
def get_books():
    books = service.get_all_books()
    return jsonify([{'id': b.id, 'title': b.title, 'author': b.author, 'year': b.year} for b in books])

@book_blueprint.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = service.get_book_by_id(book_id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year})

@book_blueprint.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    dto = BookDTO(**request.get_json())
    book = service.update_book(book_id, dto)
    return jsonify({'message': 'Book updated'})

@book_blueprint.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    service.delete_book(book_id)
    return jsonify({'message': 'Book deleted'})