"""
Review Routes
Handles product reviews and ratings
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Review, Order, Product
from bson import ObjectId
from utils.errors import BadRequestError, UnauthorizedError, NotFoundError
from utils.decorators import role_required, get_identity
from datetime import datetime

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')


@reviews_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['consumer', 'buyer'])
def create_review():
    """Create a new review"""
    try:
        identity = get_identity()
        user_id = identity.get('user_id')
        data = request.get_json()
        
        # Validation
        product_id = data.get('product_id')
        rating = data.get('rating')
        comment = data.get('comment')
        
        if not product_id:
            raise BadRequestError("Product ID is required")
        
        if not rating or rating < 1 or rating > 5:
            raise BadRequestError("Rating must be between 1 and 5")
        
        # Check if user purchased this product
        try:
            buyer_obj = ObjectId(user_id)
        except Exception:
            buyer_obj = user_id

        order = Order.find_one({'buyer_id': buyer_obj, 'items.product_id': product_id})
        if not order:
            raise UnauthorizedError("You can only review products you have purchased")
        
        # Create review
        # Review.create_review expects (product_id, buyer_id, rating, comment)
        review_id = Review.create_review(product_id, user_id, rating, comment or "")
        
        # Update product rating
        # Ensure product_id is an ObjectId for queries
        try:
            prod_obj = ObjectId(product_id)
        except Exception:
            prod_obj = product_id

        reviews = Review.find_many({'product_id': prod_obj})
        avg_rating = sum(r.get('rating', 0) for r in reviews) / len(reviews) if reviews else 0
        Product.update(product_id, {
            'rating': round(avg_rating, 1),
            'review_count': len(reviews)
        })
        
        return jsonify({
            'status': 'success',
            'message': 'Review created successfully',
            'review_id': str(review_id)
        }), 201
    
    except (BadRequestError, UnauthorizedError) as e:
        status_code = 400 if isinstance(e, BadRequestError) else 403
        return jsonify({'status': 'error', 'message': str(e)}), status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    """Get reviews for a product"""
    try:
        product_id = request.args.get('product_id')
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        if not product_id:
            raise BadRequestError("Product ID is required")
        
        skip = (page - 1) * limit
        reviews = Review.find_many({'product_id': product_id}, limit=limit, skip=skip)
        total = Review.count({'product_id': product_id})
        
        reviews_list = [
            {
                'review_id': str(r['_id']),
                'product_id': str(r.get('product_id')) if r.get('product_id') else None,
                'rating': r.get('rating'),
                'comment': r.get('comment'),
                'user_name': r.get('user_name'),
                'created_at': r.get('created_at')
            }
            for r in reviews
        ]
        
        return jsonify({
            'status': 'success',
            'data': reviews_list,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
    
    except BadRequestError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@reviews_bp.route('/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Update a review"""
    try:
        identity = get_identity()
        user_id = identity.get('user_id')
        data = request.get_json()
        
        # Check ownership
        review = Review.find_by_id(review_id)
        if not review:
            raise NotFoundError("Review not found")
        
        # Model stores buyer id under 'buyer_id'
        if str(review.get('buyer_id')) != str(user_id):
            raise UnauthorizedError("You can only edit your own reviews")
        
        # Update
        update_data = {}
        if 'rating' in data and 1 <= data['rating'] <= 5:
            update_data['rating'] = data['rating']
        if 'comment' in data:
            update_data['comment'] = data['comment']
        
        if update_data:
            Review.update(review_id, update_data)
            
            # Recalculate product rating
            product_id = review.get('product_id')
            try:
                prod_obj = ObjectId(product_id)
            except Exception:
                prod_obj = product_id
            reviews = Review.find_many({'product_id': prod_obj})
            avg_rating = sum(r.get('rating', 0) for r in reviews) / len(reviews) if reviews else 0
            Product.update(product_id, {
                'rating': round(avg_rating, 1),
                'review_count': len(reviews)
            })
        
        return jsonify({
            'status': 'success',
            'message': 'Review updated successfully'
        }), 200
    
    except (NotFoundError, UnauthorizedError) as e:
        status_code = 404 if isinstance(e, NotFoundError) else 403
        return jsonify({'status': 'error', 'message': str(e)}), status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@reviews_bp.route('/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review"""
    try:
        identity = get_identity()
        user_id = identity.get('user_id')
        
        review = Review.find_by_id(review_id)
        if not review:
            raise NotFoundError("Review not found")
        
        if str(review.get('buyer_id')) != str(user_id):
            raise UnauthorizedError("You can only delete your own reviews")
        
        product_id = review.get('product_id')
        Review.delete(review_id)
        
        # Recalculate product rating
        try:
            prod_obj = ObjectId(product_id)
        except Exception:
            prod_obj = product_id
        reviews = Review.find_many({'product_id': prod_obj})
        avg_rating = sum(r.get('rating', 0) for r in reviews) / len(reviews) if reviews else 0
        Product.update(product_id, {
            'rating': round(avg_rating, 1) if avg_rating > 0 else 0,
            'review_count': len(reviews)
        })
        
        return jsonify({
            'status': 'success',
            'message': 'Review deleted successfully'
        }), 200
    
    except (NotFoundError, UnauthorizedError) as e:
        status_code = 404 if isinstance(e, NotFoundError) else 403
        return jsonify({'status': 'error', 'message': str(e)}), status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
