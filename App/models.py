from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  reviews = db.relationship('Review', backref='user', lazy=True)

  def __init__(self, username, password):
    self.username= username
    self.set_password(password)

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)


    
class Book(db.Model):
  isbn = db.Column(db.String, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  author = db.Column(db.String(50), nullable=False)
  publisher = db.Column(db.String(50), nullable=False)
  reviews = db.relationship('Review', backref='book', lazy=True)

  def __init__(self, isbn, title, author, publisher, reviews):
    self.isbn = isbn
    self.title = title
    self.author = author
    self.publisher = publisher
    self.reviews = reviews
  def __repr__(self):
    return f'<Book {self.title}>'

  def create_review(self, user_id, text, rating):
    review = Review(user_id=user_id, isbn=self.isbn, text=text, rating=rating)
    db.session.add(review)


  
class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  isbn = db.Column(db.String, db.ForeignKey('book.isbn'), nullable=False)
  text = db.Column(db.String(500), nullable=False)
  rating = db.Column(db.Integer, nullable=False)

  def __init__(self, user_id, isbn, text, rating):
    self.user_id = user_id
    self.isbn = isbn
    self.text = text
    self.rating = rating