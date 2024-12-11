# Admin API's 

from flask import request, jsonify
from run import app, bcrypt
from models import db, User, Book, Request
from auth import token_required


# Admin - Create a new user
def add_user(data):
    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Incomplete data!"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User Already Exits!"}), 400
    
    pw_hashed = bcrypt.generate_password_hash(data['password'])
    new_user = User(email=data['email'], password=pw_hashed, is_admin=data.get('is_admin', False))
    
    # Add new admin to the database
    db.session.add(new_user)
    db.session.commit()

    return 200

# Admin - Sign up
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    msg = add_user(data)
    if msg == 200:
        return jsonify({"message": "Admin account created successfully!"}), 200
    return msg

# Admin - Add New User using Email and Password
@app.route("/add-user", methods=['POST'])
@token_required(admin_only=True)
def create_user(current_user):

    data = request.json
    msg = add_user(data)

    if msg == 200:
        return jsonify({"message": "User account created successfully!"}), 200
    return msg

# Admin - Add New Book
@app.route("/add-book", methods=['POST'])
@token_required(admin_only=True)
def add_book(current_user):

    data = request.json
    title = data.get('title')
    author = data.get('author')
    yop = data.get('published_year')

    if not title or not author or not yop:
        return jsonify({"message": "Incomplete Data!"}), 400
    
    new_book = Book(title=title, author=author, published_year=yop)
    
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Book added successfully!"}), 200

# Admin - View all book borrowing requests.
@app.route('/requests', methods=['GET'])
@token_required(admin_only=True)
def view_requests(current_user):

    requests = Request.query.all()
    return jsonify([{
        "id": request.id,
        "user_id": request.user_id,
        "user_email": request.user.email,
        "book_title": request.book.title,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "status": request.status
    } for request in requests]), 200



# Admin - Approve or deny a borrow request
@app.route('/requests/<int:request_id>', methods=['PUT'])
@token_required(admin_only=True)
def approve_request(current_user, request_id):
    
    borrow_request = Request.query.get(request_id)

    if not borrow_request:
        return jsonify({"message": "Request not found!"}), 404
    
    # Check the request status
    request_status = borrow_request.status

    if request_status == 'Pending':
    
        # Check if other users have already borrowed books.
        borrowed_books = Request.query.filter(
            Request.book_id == borrow_request.book.id,
            Request.status == 'Approved',
            Request.user_id != borrow_request.user_id,
            Request.start_date <= borrow_request.end_date,
            Request.end_date >= borrow_request.start_date
        ).first()

        if borrowed_books:
            borrow_request.status = 'Denied'
        else:
            borrow_request.status = 'Approved'
        db.session.commit()
    return jsonify({"message": f"Request {borrow_request.status.lower()}!"})


# Admin - View user's book borrowing history.
@app.route('/users/<int:user_id>/history', methods=['GET'])
@token_required(admin_only=True)
def view_user_borrow_history(current_user, user_id):

    borrow_history = Request.query.filter_by(user_id = user_id, status='Approved').all()
    
    if borrow_history:
        
        return jsonify([{
            "id": record.id,
            "user_email": record.user.email,
            "book_title": record.book.title,
            "start_date": record.start_date,
            "end_date": record.end_date,
            "status": record.status
        } for record in borrow_history]), 200
    
    return jsonify({"message": f"The user {user_id} has no borrow history in the library system."}), 200

