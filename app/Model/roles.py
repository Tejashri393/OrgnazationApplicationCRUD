  
from app import db
class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    department = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,  
            "department": self.department
        }
