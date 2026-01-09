"""
Machine Learning Routes
Provides API endpoints for ML predictions
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ml.models import crop_recommender, price_predictor, product_recommender
from utils.errors import BadRequestError

ml_bp = Blueprint('ml', __name__, url_prefix='/api/ml')


@ml_bp.route('/crop-recommendation', methods=['POST'])
def recommend_crops():
    """Get crop recommendations based on environmental factors"""
    try:
        data = request.get_json()
        
        # Validation
        required = ['soil_type', 'season', 'rainfall', 'temperature', 'humidity']
        if not all(field in data for field in required):
            raise BadRequestError(f"Missing required fields: {required}")
        
        # Get recommendations
        recommendations = crop_recommender.predict(
            soil_type=data['soil_type'],
            season=data['season'],
            rainfall=data['rainfall'],
            temperature=int(data['temperature']),
            humidity=int(data['humidity'])
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'recommendations': recommendations,
                'input_params': {
                    'soil_type': data['soil_type'],
                    'season': data['season'],
                    'rainfall': data['rainfall'],
                    'temperature': data['temperature'],
                    'humidity': data['humidity']
                }
            }
        }), 200
    
    except BadRequestError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@ml_bp.route('/price-prediction', methods=['POST'])
def predict_price():
    """Predict future crop prices"""
    try:
        data = request.get_json()
        
        days = int(data.get('days_from_now', 7))
        season = int(data.get('season', 0))
        category = int(data.get('category', 0))
        quantity = int(data.get('quantity', 100))
        
        if days < 0 or days > 365:
            raise BadRequestError("Days must be between 0 and 365")
        
        if quantity <= 0:
            raise BadRequestError("Quantity must be positive")
        
        prediction = price_predictor.predict(
            days_from_now=days,
            season=season,
            category=category,
            quantity=quantity
        )
        
        return jsonify({
            'status': 'success',
            'data': prediction
        }), 200
    
    except BadRequestError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@ml_bp.route('/product-recommendation', methods=['POST'])
@jwt_required()
def recommend_products():
    """Get personalized product recommendations for a buyer"""
    try:
        from utils.decorators import get_identity
        identity = get_identity()
        buyer_id = identity.get('user_id')
        
        data = request.get_json()
        n_recommendations = int(data.get('n_recommendations', 5))
        
        if n_recommendations < 1 or n_recommendations > 20:
            raise BadRequestError("n_recommendations must be between 1 and 20")
        
        recommendations = product_recommender.recommend_products(buyer_id, n_recommendations)
        
        return jsonify({
            'status': 'success',
            'data': {
                'recommendations': recommendations,
                'count': len(recommendations)
            }
        }), 200
    
    except BadRequestError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@ml_bp.route('/model-info', methods=['GET'])
def get_model_info():
    """Get information about available ML models"""
    return jsonify({
        'status': 'success',
        'data': {
            'models': [
                {
                    'name': 'Crop Recommendation',
                    'endpoint': '/api/ml/crop-recommendation',
                    'method': 'POST',
                    'description': 'Recommends suitable crops based on environmental factors',
                    'requires_auth': False
                },
                {
                    'name': 'Price Prediction',
                    'endpoint': '/api/ml/price-prediction',
                    'method': 'POST',
                    'description': 'Predicts future crop prices',
                    'requires_auth': False
                },
                {
                    'name': 'Product Recommendation',
                    'endpoint': '/api/ml/product-recommendation',
                    'method': 'POST',
                    'description': 'Recommends products based on buyer preferences',
                    'requires_auth': True
                }
            ]
        }
    }), 200
