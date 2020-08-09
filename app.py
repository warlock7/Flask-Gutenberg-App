from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload, aliased
from sqlalchemy import or_, and_
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *

@app.route('/allbooks', methods=['POST', 'GET'])
def get_all_books():   
    books=Book.query.order_by(Book.download_count.desc().nullslast()).limit(1).all()
    return  jsonify([e.serializeBookWithDetails() for e in books])

@app.route('/authors')
def get_all_authors():
    author=Author.query.limit(1).all()
    return  jsonify([e.serializeAuthorWithDetails() for e in author])

@app.route('/book_authors')
def get_all_books_author():
    book_author=Book_Author.query.limit(10).all()
    return  jsonify([e.serialize() for e in book_author])

@app.route('/languages')
def get_all_languages():
    languages=Language.query.limit(1).all()
    return  jsonify([e.serializeLanguageWithDetails() for e in languages])

@app.route('/format')
def get_all_format():
    book_format=Book_Format.query.limit(5).all()
    return  jsonify([e.serialize() for e in book_format])

@app.route('/books', methods=['POST', 'GET'])
def view():
    

	return jsonify(get_paginated_list(
		Book, 
		'/books', 
		start=request.args.get('start', 1), 
		limit=request.args.get('limit', 25)
	))

def get_paginated_list(klass, url, start, limit):
    # check if page exists
    if request.method == 'POST':
        data = request.get_json()
        if data:
            filter_book_id = data["book_id"]
            filter_language = data["language"]
            filter_mime_type = data["mime-type"]
            filter_title = data["title"]
        else:
            return jsonify({"message":"Bad request"}), 400
        
        query = klass.query

        join_statement = []
        if filter_language:
            join_statement.append(Language.book)
        if filter_mime_type:
            join_statement.append(klass.book_format)

        options_statement = []
        if filter_mime_type:
            options_statement.append(joinedload(klass.book_format))

        conditions = []
        if filter_book_id:
            conditions.append(klass.id == filter_book_id)
        if filter_language:
            conditions.append(Language.code == filter_language) 
        if filter_title:
            conditions.append(klass.title.like('%'+filter_title+'%')) 
        if filter_mime_type:
            conditions.append(Book_Format.mime_type.like(filter_mime_type)) 

        results = query.join(*join_statement).options(*options_statement).filter(and_(*conditions)).order_by(klass.download_count.desc().nullslast()).all()
    else:
        results = klass.query.order_by(klass.download_count.desc().nullslast()).all()
    count = len(results)
    start = int(start)
    limit = int(limit)
    if (count < start):
        return {'Error': 'Start value greater than count of total records!'}
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = [e.serializeBookWithDetails() for e in results[(start - 1):(start - 1 + limit)]]
    
    return obj

@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    return jsonify({'message':'Page not found'}), 404

if __name__ == '__main__':
    app.run()
