from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    __table_args__ = (
        db.CheckConstraint("length(phone_number) = 10"),
    )

    @validates('name')
    def validate_name(self, key, name):
        authors=Author.query.all()
        names = []
        for author in authors:
            names.append(author.name)
        if name is None or name == "":
            raise ValueError("Name is required")
        if name in names:
            raise ValueError("Name is not unique")
        return name
    
    @validates('phone_number')
    def validates_number(self, key, phone_number):
        if phone_number is None:
            raise ValueError("Phone number is required")
        if len(phone_number) != 10:
            raise ValueError("Phone number must be 10 digits")
        if not phone_number.isdigit():
            raise ValueError("Phone number must be only numbers")
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    __table_args__ = (
        db.CheckConstraint("length(content) >= 250"),
        db.CheckConstraint("length(summary) <= 250"),
        db.CheckConstraint("category IN ('Fiction', 'Non-Fiction')"),
        db.CheckConstraint("title LIKE '%Won''t Believe%' " "OR title LIKE '%Secret%' " "OR title LIKE '%Top%' " "OR title LIKE '%Guess%'"),
    )

    @validates('title')
    def validate_title(self, key, title):
        if not title or title == "":
            raise ValueError("Title must exist")
        if "Secret" not in title and "Top" not in title and "Won't Believe" not in title and "Guess" not in title:
            raise ValueError("Title is not click bait enough")
        return title
    
    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError("Post content must be 250 characters")

    @validates('summary')
    def validate_summary(self, key, summary):
        if not summary or len(summary) > 250:
            raise ValueError("Summary must exist and be less than 250 characters")
    
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction'")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
