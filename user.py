# User's APIs
from flask import request, jsonify, make_response

from run import app
from models import db, Book, Request
from auth import token_required
from datetime import datetime

# User - Get the list of books
@app.route('/books', methods=['GET'])
@token_required()
def get_list_books(current_user):
    # Get all books data
    books = Book.query.all()

    return jsonify([{
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year_of_publication": book.published_year,
    } for book in books])


# User - Submit Borrow Request
@app.route('/request-book', methods=['POST'])
@token_required()
def submit_request(current_user):

    data = request.json
    book_id = data.get('book_id')
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

    # Check if book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
    
    # Check if request has been already submitted by same user.
    existing_requests = Request.query.filter(
        Request.user_id == current_user.id,
        Request.book_id == book_id,
        Request.status == 'Pending'
    )

    if existing_requests:
        return jsonify({
            "message" : "Request is already submitted!"
        }), 400


    # Check for overslapping borrow requests
    overlapping_request = Request.query.filter(
        Request.user_id != current_user.id,
        Request.book_id == book_id,
        Request.status == 'Approved',
        Request.end_date >= start_date,
        Request.start_date <= end_date
    ).first()

    if overlapping_request:
        return jsonify({"message":"Book is already borrowed for the selected dates!"}), 400
    

    borrow_request = Request(
        user_id = current_user.id,
        book_id = book_id,
        start_date = start_date,
        end_date = end_date
    )

    db.session.add(borrow_request)
    db.session.commit()
    return jsonify({"message": "Borrow request submitted!"})
    

# User - View personal borrow history
@app.route('/user/history', methods=['GET'])
@token_required()
def view_history(current_user):
    return jsonify([{
        "book_title" : req.book.title,
        "start_date": req.start_date,
        "end_date": req.end_date,
        "status": req.status
    } for req in current_user.requests])


# User - Download borrow history as CSV
@app.route('/user/download-history', methods=['GET'])
@token_required() 
def download_borrow_history(current_user):
    
    # Get the user's borrow history from the database
    borrow_history = Request.query.filter_by(user_id=current_user.id).all()

    # If no borrow history exists
    if not borrow_history:
        return jsonify({"message": "No borrow history found"}), 404

    # Create a CSV response
    output = []
    header = ["Book Title","Book Author", "Borrow Start Date", "Borrow End Date", "Status"]
    output.append(header) 

    for record in borrow_history:
        output.append([
            record.book.title,
            record.book.author,
            record.start_date.strftime('%Y-%m-%d'),
            record.end_date.strftime('%Y-%m-%d'),
            record.status
        ])

    # Use make_response to return the CSV as a file download
    response = make_response('\n'.join([','.join(row) for row in output]))
    response.headers['Content-Disposition'] = 'attachment; filename=borrow_history.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response
