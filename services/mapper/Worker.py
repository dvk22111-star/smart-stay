from models.book import Book
from exceptions.exceptions import BookAlreadyExistsException, MissingTitleException, BookNotFoundException

class BookService:
    def __init__(self, repo):
        self.repo = repo

    def add_book(self, dto):
        if not dto.title:
            raise MissingTitleException()
        if self.repo.exists_by_title(dto.title):
            raise BookAlreadyExistsException(dto.title)
        self.repo.add(Book(title=dto.title, author=dto.author, year=dto.year))

    def get_all_books(self):
        return self.repo.get_all()

    def get_book_by_id(self, book_id):
        book = self.repo.get_by_id(book_id)
        if not book:
            raise BookNotFoundException(book_id)
        return book

    def update_book(self, book_id, dto):
        book = self.repo.update(book_id, Book(title=dto.title, author=dto.author, year=dto.year))
        if not book:
            raise BookNotFoundException(book_id)
        return book

    def delete_book(self, book_id):
        book = self.repo.delete(book_id)
        if not book:
            raise BookNotFoundException(book_id)