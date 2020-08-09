from app import db

class Book(db.Model):
    __tablename__ = 'books_book'

    id = db.Column(db.Integer, primary_key=True)
    download_count = db.Column(db.Integer)
    gutenberg_id = db.Column(db.Integer)
    media_type = db.Column(db.String())
    title = db.Column(db.String())    
    book_format = db.relationship('Book_Format', backref = db.backref('book', lazy='joined'))

    def __init__(self, download_count, gutenberg_id, media_type, title):
        self.download_count = download_count
        self.gutenberg_id = gutenberg_id
        self.media_type = media_type
        self.title = title

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'download_count': self.download_count, 
            'gutenberg_id': self.gutenberg_id,
            'media_type': self.media_type,
            'title':self.title
        }

    def serializeBookWithDetails(self):
        return {
            'id': self.id,
            'download_count': self.download_count, 
            'gutenberg_id': self.gutenberg_id,
            'media_type': self.media_type,
            'title':self.title,
            'author': [e.serialize() for e in self.author],
            'language': [e.serialize() for e in self.language],
            'subject': [e.serialize() for e in self.subject],
            'bookshelf': [e.serialize() for e in self.bookshelf],
            'book_format': [e.serialize() for e in self.book_format]
        }

class Author(db.Model):
    __tablename__ = 'books_author'

    id = db.Column(db.Integer, primary_key=True)
    birth_year = db.Column(db.Integer)
    death_year = db.Column(db.Integer)
    name = db.Column(db.String())
    book = db.relationship('Book', secondary='books_book_authors', backref = db.backref('author', lazy='dynamic'))

    def __init__(self, birth_year, death_year, name):
        self.birth_year = birth_year
        self.death_year = death_year
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'birth_year': self.birth_year, 
            'death_year': self.death_year,
            'name': self.name
        }
    
    def serializeAuthorWithDetails(self):
        return {
            'id': self.id,
            'birth_year': self.birth_year, 
            'death_year': self.death_year,
            'name': self.name,
            'book': [e.serialize() for e in self.book]
        }

class Book_Author(db.Model):
    __tablename__ = 'books_book_authors'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books_book.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('books_author.id'))
    # book = db.relationship('Book', foreign_keys=[book_id])
    # book = db.relationship('Book', primaryjoin="Book_Author.book_id == Book.id")
    # author = db.relationship('Author',foreign_keys=[author_id])

    def __init__(self, book_id, author_id):
        self.book_id = book_id
        self.author_id = author_id

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'book_id': self.book_id, 
            'author_id': self.author_id
            # ,
            # 'book': self.book.title
        }

class Language(db.Model):
    __tablename__ = 'books_language'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())    
    book = db.relationship('Book', secondary='books_book_languages', backref = db.backref('language', lazy='dynamic'))

    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'code': self.code
        }
    
    def serializeLanguageWithDetails(self):
        return {
            'id': self.id,
            'code': self.code,
            'book': [e.serialize() for e in self.book]
        }

class Book_Language(db.Model):
    __tablename__ = 'books_book_languages'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books_book.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('books_language.id'))
    # book = db.relationship('Book', foreign_keys=[book_id])
    # book = db.relationship('Book', primaryjoin="Book_Author.book_id == Book.id")
    # author = db.relationship('Author',foreign_keys=[author_id])

    def __init__(self, book_id, language_id):
        self.book_id = book_id
        self.language_id = language_id

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'book_id': self.book_id, 
            'language_id': self.language_id
            # ,
            # 'book': self.book.title
        }

class Subject(db.Model):
    __tablename__ = 'books_subject'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())    
    book = db.relationship('Book', secondary='books_book_subjects', backref = db.backref('subject', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def serializeSubjectWithDetails(self):
        return {
            'id': self.id,
            'name': self.name,
            'book': [e.serialize() for e in self.book]
        }

class Book_Subject(db.Model):
    __tablename__ = 'books_book_subjects'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books_book.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('books_subject.id'))
    # book = db.relationship('Book', foreign_keys=[book_id])
    # book = db.relationship('Book', primaryjoin="Book_Author.book_id == Book.id")
    # author = db.relationship('Author',foreign_keys=[author_id])

    def __init__(self, book_id, subject_id):
        self.book_id = book_id
        self.subject_id = subject_id

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'book_id': self.book_id, 
            'subject_id': self.subject_id
            # ,
            # 'book': self.book.title
        }

class BookShelf(db.Model):
    __tablename__ = 'books_bookshelf'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())    
    book = db.relationship('Book', secondary='books_book_bookshelves', backref = db.backref('bookshelf', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def serializeSubjectWithDetails(self):
        return {
            'id': self.id,
            'name': self.name,
            'book': [e.serialize() for e in self.book]
        }

class Book_BookShelf(db.Model):
    __tablename__ = 'books_book_bookshelves'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books_book.id'))
    bookshelf_id = db.Column(db.Integer, db.ForeignKey('books_bookshelf.id'))
    # book = db.relationship('Book', foreign_keys=[book_id])
    # book = db.relationship('Book', primaryjoin="Book_Author.book_id == Book.id")
    # author = db.relationship('Author',foreign_keys=[author_id])

    def __init__(self, book_id, bookshelf_id):
        self.book_id = book_id
        self.bookshelf_id = bookshelf_id

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'book_id': self.book_id, 
            'bookshelf_id': self.bookshelf_id
            # ,
            # 'book': self.book.title
        }

class Book_Format(db.Model):
    __tablename__ = 'books_format'

    id = db.Column(db.Integer, primary_key=True)
    mime_type = db.Column(db.String())    
    url = db.Column(db.String())    
    book_id = db.Column(db.Integer, db.ForeignKey('books_book.id'))

    def __init__(self, mime_type, url, book_id):
        self.mime_type = mime_type
        self.url = url
        self.book_id = book_id

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'mime_type': self.mime_type,
            'url': self.url
        }