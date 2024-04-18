from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('All names have a name')
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError('No two authors have the same name.')
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError('Author phone number must be exactly ten digits.')
        return phone_number

       

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post title is required.")
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Post title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return title
    
        
    @validates('content')
    def validate_post_content(self, key, value):
        if not value or len(value.strip()) < 250:
             raise ValueError('Post content is at least 250 characters long.')
        return value
    
    @validates('summary')
    def validate_post_summary(self, key, value):
        if value and len(value.strip()) > 250:
            raise ValueError('Post summary must be at most 250 characters long.')
        return value
    
    @validates('category')
    def validate_Post_category(self, key, category):
         if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'")
         return category
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
