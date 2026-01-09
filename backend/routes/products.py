"""
Product Routes
Handles product listing, creation, and management
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import get_identity, role_required
from models import Product
from utils.errors import BadRequestError, UnauthorizedError, NotFoundError

products_bp = Blueprint('products', __name__, url_prefix='/api/products')


@products_bp.route('/', methods=['GET'])
def get_products():
    """Get all products with pagination and filters"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        category = request.args.get('category', None)
        search = request.args.get('search', None)
        
        skip = (page - 1) * limit
        
        # Build query
        query = {'is_active': True}
        
        if category and category in Product.CATEGORIES:
            query['category'] = category
        
        if search:
            query['$text'] = {'$search': search}
        
        # Get products
        products = Product.find_many(query, limit=limit, skip=skip)
        total = Product.count(query)
        
        # Format response
        products_list = [
            {
                'product_id': str(p['_id']),
                'name': p.get('name'),
                'category': p.get('category'),
                'description': p.get('description'),
                'price': p.get('price'),
                'quantity': p.get('quantity'),
                'rating': p.get('rating'),
                'image_url': p.get('image_url')
            }
            for p in products
        ]
        
        return jsonify({
            'status': 'success',
            'data': products_list,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product details"""
    try:
        product = Product.find_by_id(product_id)
        
        if not product:
            raise NotFoundError("Product not found")
        
        return jsonify({
            'status': 'success',
            'data': {
                'product_id': str(product['_id']),
                'name': product.get('name'),
                'category': product.get('category'),
                'description': product.get('description'),
                'price': product.get('price'),
                'quantity': product.get('quantity'),
                'soil_type': product.get('soil_type'),
                'season': product.get('season'),
                'quality_grade': product.get('quality_grade'),
                'rating': product.get('rating'),
                'review_count': product.get('review_count'),
                'image_url': product.get('image_url')
            }
        }), 200
    
    except NotFoundError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@products_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['farmer'])
def create_product():
    """Create a new product"""
    try:
        identity = get_identity()
        farmer_id = identity.get('user_id')
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'category', 'description', 'price', 'quantity']
        if not all(field in data for field in required_fields):
            raise BadRequestError(f"Missing required fields: {required_fields}")
        
        if data['category'] not in Product.CATEGORIES:
            raise BadRequestError(f"Invalid category. Must be one of {Product.CATEGORIES}")
        
        if data['price'] <= 0 or data['quantity'] < 0:
            raise BadRequestError("Price must be positive and quantity must be non-negative")
        
        # Create product
        product_id = Product.create_product(
            farmer_id=farmer_id,
            name=data['name'],
            category=data['category'],
            description=data['description'],
            price=data['price'],
            quantity=data['quantity'],
            soil_type=data.get('soil_type'),
            season=data.get('season'),
            quality_grade=data.get('quality_grade'),
            image_url=data.get('image_url')
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Product created successfully',
            'product_id': str(product_id)
        }), 201
    
    except BadRequestError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except UnauthorizedError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 403
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@products_bp.route('/<product_id>', methods=['PUT'])
@jwt_required()
@role_required(['farmer'])
def update_product(product_id):
    """Update product details"""
    try:
        identity = get_identity()
        farmer_id = identity.get('user_id')
        
        product = Product.find_by_id(product_id)
        
        if not product:
            raise NotFoundError("Product not found")
        
        # Check ownership
        if str(product['farmer_id']) != farmer_id:
            raise UnauthorizedError("You can only update your own products")
        
        data = request.get_json()
        
        # Only allow certain fields to be updated
        allowed_fields = ['name', 'description', 'price', 'quantity', 'soil_type', 'season', 'quality_grade', 'image_url']
        update_data = {field: data[field] for field in allowed_fields if field in data}
        
        if not update_data:
            raise BadRequestError("No valid fields to update")
        
        Product.update(product_id, update_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Product updated successfully'
        }), 200
    
    except (BadRequestError, NotFoundError, UnauthorizedError) as e:
        status_code = 400 if isinstance(e, BadRequestError) else (404 if isinstance(e, NotFoundError) else 403)
        return jsonify({'status': 'error', 'message': str(e)}), status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@products_bp.route('/<product_id>', methods=['DELETE'])
@jwt_required()
@role_required(['farmer'])
def delete_product(product_id):
    """Delete a product"""
    try:
        identity = get_identity()
        farmer_id = identity.get('user_id')
        
        product = Product.find_by_id(product_id)
        
        if not product:
            raise NotFoundError("Product not found")
        
        # Check ownership
        if str(product['farmer_id']) != farmer_id:
            raise UnauthorizedError("You can only delete your own products")
        
        # Soft delete (mark as inactive)
        Product.update(product_id, {'is_active': False})
        
        return jsonify({
            'status': 'success',
            'message': 'Product deleted successfully'
        }), 200
    
    except (NotFoundError, UnauthorizedError) as e:
        status_code = 404 if isinstance(e, NotFoundError) else 403
        return jsonify({'status': 'error', 'message': str(e)}), status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@products_bp.route('/farmer/<farmer_id>', methods=['GET'])
def get_farmer_products(farmer_id):
    """Get all products from a specific farmer"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        skip = (page - 1) * limit
        
        products = Product.find_by_farmer(farmer_id, limit=limit, skip=skip)
        total = Product.count({'farmer_id': farmer_id, 'is_active': True})
        
        products_list = [
            {
                'product_id': str(p['_id']),
                'name': p.get('name'),
                'category': p.get('category'),
                'price': p.get('price'),
                'quantity': p.get('quantity'),
                'rating': p.get('rating')
            }
            for p in products
        ]
        
        return jsonify({
            'status': 'success',
            'data': products_list,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
