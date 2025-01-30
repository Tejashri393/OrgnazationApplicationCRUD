
from app import db

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(50))
    org_code = db.Column(db.Integer, db.ForeignKey('organisations.code'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # Foreign key to the Roles table

   

    def to_dict(self):
        return {
            "id": self.id,
            "fname": self.fname,
            "lname": self.lname,
            "email": self.email,
            "address": self.address,
            "org_code": self.org_code,
            "role_id": self.role_id,  # Add the role_id in the dict output
        }