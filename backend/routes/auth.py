"""
Authentication Routes
Handles user signup, login, token refresh
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from utils.decorators import get_identity
import json
from models import User
from utils.validators import validate_email, validate_password
from utils.errors import BadRequestError, UnauthorizedError
from bson import ObjectId

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('email') or not data.get('password') or not data.get('name'):
            raise BadRequestError("Email, password, and name are required")
        
        if not validate_email(data['email']):
            raise BadRequestError("Invalid email format")
        
        if not validate_password(data['password']):
            raise BadRequestError("Password must be at least 6 characters")
        
        # Create user
        role = data.get('role', 'buyer')
        if role not in User.ROLES:
            raise BadRequestError(f"Invalid role. Must be one of {User.ROLES}")
        
        user_id = User.create_user(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            role=role,
            phone=data.get('phone'),
            address=data.get('address')
        )
        
        # Fetch created user to get full details
        user = User.find_by_id(user_id)
        
        # Create tokens
        identity_payload = {
            'user_id': str(user['_id']),
            'email': user['email'],
            'role': user['role']
        }
        # Store identity as JSON string inside the token subject to avoid subject type issues
        access_token = create_access_token(identity=json.dumps(identity_payload))
        refresh_token = create_refresh_token(identity=json.dumps(identity_payload))
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'user_id': str(user['_id']),
                'email': user['email'],
                'name': user['name'],
                'role': user['role']
            }
        }), 201
    
    except BadRequestError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Signup failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            raise BadRequestError("Email and password are required")
        
        # Find user
        user = User.find_by_email(data['email'])
        
        if not user or not User.verify_password(user, data['password']):
            raise UnauthorizedError("Invalid email or password")
        
        if not user.get('is_active', True):
            raise UnauthorizedError("User account is inactive")
        
        # Create tokens
        identity_payload = {
            'user_id': str(user['_id']),
            'email': user['email'],
            'role': user['role']
        }
        # Store identity as JSON string inside the token subject to avoid subject type issues
        access_token = create_access_token(identity=json.dumps(identity_payload))
        refresh_token = create_refresh_token(identity=json.dumps(identity_payload))
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'user_id': str(user['_id']),
                'email': user['email'],
                'name': user['name'],
                'role': user['role']
            }
        }), 200
    
    except BadRequestError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except UnauthorizedError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        identity = get_identity()
        
        # Preserve identity format stored in token (stringified JSON or dict)
        access_token = create_access_token(identity=json.dumps(identity) if not isinstance(identity, str) else identity)
        
        return jsonify({
            'status': 'success',
            'access_token': access_token
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Token refresh failed: {str(e)}'}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        identity = get_identity()
        user_id = identity.get('user_id')
        
        user = User.find_by_id(user_id)
        
        if not user:
            raise UnauthorizedError("User not found")
        
        return jsonify({
            'status': 'success',
            'user': {
                'user_id': str(user['_id']),
                'email': user['email'],
                'name': user['name'],
                'role': user['role'],
                'phone': user.get('phone'),
                'address': user.get('address'),
                'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
            }
        }), 200
    
    except UnauthorizedError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Profile fetch failed: {str(e)}'}), 500


@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        identity = get_identity()
        user_id = identity.get('user_id')
        data = request.get_json()
        
        # Only allow updating certain fields
        allowed_fields = ['name', 'phone', 'address']
        update_data = {field: data[field] for field in allowed_fields if field in data}
        
        if not update_data:
            raise BadRequestError("No valid fields to update")
        
        success = User.update(user_id, update_data)
        
        if not success:
            raise ValueError("User not found")
        
        return jsonify({
            'status': 'success',
            'message': 'Profile updated successfully'
        }), 200
    
    except BadRequestError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Update failed: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (token invalidation handled client-side)"""
    return jsonify({
        'status': 'success',
        'message': 'Logged out successfully'
    }), 200
