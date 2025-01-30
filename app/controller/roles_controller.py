from flask import Blueprint, request, jsonify
from app.Model.roles import Roles
from app import db
from sqlalchemy.exc import IntegrityError
import logging

roles_bp = Blueprint('roles', __name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Helper function for validation
def validate_role_data(data):
    """Validates the role data."""
    if 'name' not in data or not data['name']:
        return False, "The 'name' field is required and cannot be empty."
    return True, None

# Route to get all roles
@roles_bp.route('/roles', methods=['GET'])
def get_all_roles():
    roles = Roles.query.all()
    if not roles:
        return jsonify({"message": "No roles found in the database."}), 404
    return jsonify([{"id": role.id, "name": role.name} for role in roles]), 200

# Route to get a role by ID
@roles_bp.route('/role/<int:role_id>', methods=['GET'])
def get_role_by_id(role_id):
    role = Roles.query.get(role_id)
    if not role:
        return jsonify({"message": "No role found with the given ID."}), 404
    return jsonify({"id": role.id, "name": role.name}), 200

# Route to add a new role
@roles_bp.route('/role', methods=['POST'])
def add_role():
    data = request.get_json()
    
    # Validate required fields
    is_valid, error_message = validate_role_data(data)
    if not is_valid:
        return jsonify({"message": error_message}), 400

    new_role = Roles(name=data['name'])

    try:
        db.session.add(new_role)
        db.session.commit()
        return jsonify({"id": new_role.id, "name": new_role.name}), 201
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"IntegrityError: {str(e)}")
        return jsonify({"message": "Role name must be unique."}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500

# Route to edit an existing role
@roles_bp.route('/role/<int:role_id>', methods=['PUT'])
def edit_role(role_id):
    data = request.get_json()
    try:
        role = Roles.query.get_or_404(role_id)
        
        # Update role details
        if 'name' in data and data['name']:
            role.name = data['name']

        db.session.commit()
        return jsonify({"id": role.id, "name": role.name}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500

# Route to delete a role
@roles_bp.route('/role/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    try:
        role = Roles.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()
        return jsonify({"message": "Role deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500
