
from flask import Blueprint, request, jsonify
from app.Model.roles import Roles
from app import db



role_bp = Blueprint('role', __name__)



# Helper function for validation
def validate_role_data(data, required_fields):
    """Validates the role data."""
    for field in required_fields:
        if field not in data or not data[field]:  # Checks if the field is missing or empty
            return False, f"The field '{field}' is required and cannot be empty."
    return True, None

# Route to get all roles
@role_bp.route('/roles', methods=['GET'])
def get_all_roles():
    roles = Roles.query.all()
    if not roles:
        return jsonify({"message": "No roles found in the database."}), 404
    return jsonify([role.to_dict() for role in roles]), 200

# Route to get a role by id
@role_bp.route('/role/<int:id>', methods=['GET'])
def get_role_by_id(id):
    try:
        role = Roles.query.get_or_404(id)
        return jsonify(role.to_dict()), 200
    except Exception as e:
        return jsonify({"message": "Role not found"}),404

# Route to add a new role
@role_bp.route('/role', methods=['POST'])
def add_role():
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'department']
    is_valid, error_message = validate_role_data(data, required_fields)
    if not is_valid:
        return jsonify({"message": error_message}), 400

    new_role = Roles(
        name=data['name'],
        department=data['department']
    )

    try:
        db.session.add(new_role)
        db.session.commit()
        return jsonify(new_role.to_dict()), 201
   
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 404

# Route to edit a role
@role_bp.route('/role/<int:id>', methods=['PUT'])
def edit_role(id):
    data = request.get_json()
    try:
        role = Roles.query.get_or_404(id)

        # Update role details
        for key, value in data.items():
            if hasattr(role, key):
                setattr(role, key, value)

        db.session.commit()
        return jsonify(role.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Role not found for update"}), 404

# Route to delete a role
@role_bp.route('/role/<int:id>', methods=['DELETE'])
def delete_role(id):
    try:
        role = Roles.query.get_or_404(id)
        db.session.delete(role)
        db.session.commit()
        return jsonify({"message": "Role deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Role not found for delete"}), 404
