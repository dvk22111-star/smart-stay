
from models.book import Book
from sqlalchemy.orm import Session

class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, book: Book):
        self.session.add(book)
        self.session.commit()

    def get_all(self):
        return self.session.query(Book).all()

    def get_by_id(self, book_id):
        return self.session.query(Book).get(book_id)

    def update(self, book_id, new_data: Book):
        book = self.get_by_id(book_id)
        if book:
            book.title = new_data.title
            book.author = new_data.author
            book.year = new_data.year
            self.session.commit()
        return book

    def delete(self, book_id):
        book = self.get_by_id(book_id)
        if book:
            self.session.delete(book)
            self.session.commit()
        return book

    def exists_by_title(self, title):
        return self.session.query(Book).filter_by(title=title).first() is not None

