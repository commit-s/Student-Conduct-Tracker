from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from abc import ABC

class User(db.Model, UserMixin):
    ID = db.Column(db.Integer, primary_key=True)
    UniId = db.Column(db.String(10), nullable=False, unique=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    user_type = db.Column(db.String(20), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type,
    }

    def __init__(self, UniId, firstname, lastname, email, password):
        self.UniId = UniId
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.ID,
            'UniId': self.UniId,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
        }
    
    def get_id(self):
        return self.ID

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

