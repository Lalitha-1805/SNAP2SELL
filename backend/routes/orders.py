"""
Order Routes
Handles order creation and management
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import get_identity, role_required
from models import Order, Product
from utils.errors import BadRequestError, UnauthorizedError, NotFoundError

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')


@orders_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['buyer', 'consumer'])
def create_order():
    """Create a new order"""
    try:
        identity = get_identity()
        buyer_id = identity.get('user_id')
        data = request.get_json()
        
        # Validation
        if not data.get('items') or not isinstance(data['items'], list):
            raise BadRequestError("Items list is required and must be a list")
        
        if not data.get('shipping_address'):
            raise BadRequestError("Shipping address is required")
        
        # Calculate total price and validate items
        items = []
        total_price = 0
        
        for item in data['items']:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            
            if not product_id or not quantity or quantity <= 0:
                raise BadRequestError("Each item must have valid product_id and quantity")
            
            # Get product
            product = Product.find_by_id(product_id)
            
            if not product:
                raise NotFoundError(f"Product {product_id} not found")
            
            if product['quantity'] < quantity:
                raise BadRequestError(f"Insufficient stock for product {product['name']}")
            
            item_price = product['price'] * quantity
            total_price += item_price
            
            items.append({
                'product_id': product_id,
                'product_name': product['name'],
                'quantity': quantity,
                'price': product['price'],
                'total': item_price
            })
        
        # Create order
        order_id = Order.create_order(
            buyer_id=buyer_id,
            items=items,
            total_price=total_price,
            shipping_address=data['shipping_address']
        )
        
        # Update product quantities
        for item in items:
            product = Product.find_by_id(item['product_id'])
            new_quantity = product['quantity'] - item['quantity']
            Product.update(item['product_id'], {'quantity': new_quantity})
        
        return jsonify({
            'status': 'success',
            'message': 'Order created successfully',
            'order_id': str(order_id),
            'total_price': total_price
        }), 201
    
    except (BadRequestError, NotFoundError) as e:
        status_code = 400 if isinstance(e, BadRequestError) else 404
        return jsonify({'status': 'error', 'message': str(e)}), status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user orders with pagination"""
    try:
        identity = get_identity()
        user_id = identity.get('user_id')
        user_role = identity.get('role')
        
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        status = request.args.get('status', None)
        
        skip = (page - 1) * limit
        
        # Build query based on user role
        if user_role in ['buyer', 'consumer']:
            query = {'buyer_id': ObjectId(user_id) if isinstance(user_id, str) else user_id}
        else:
            # Farmers can't view buyer orders directly
            raise UnauthorizedError("Buyers only")
        
        if status and status in Order.STATUSES:
            query['status'] = status
        
        # Get orders
        orders = Order.find_many(query, limit=limit, skip=skip)
        total = Order.count(query)
        
        orders_list = [
            {
                'order_id': str(o['_id']),
                'items': o.get('items'),
                'total_price': o.get('total_price'),
                'status': o.get('status'),
                'created_at': o.get('created_at').isoformat() if o.get('created_at') else None
            }
            for o in orders
        ]
        
        return jsonify({
            'status': 'success',
            'data': orders_list,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
    
    except UnauthorizedError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 403
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@orders_bp.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order details"""
    try:
        identity = get_identity()
        user_id = identity.get('user_id')
        user_role = identity.get('role')
        
        order = Order.find_by_id(order_id)
        
        if not order:
            raise NotFoundError("Order not found")
        
        # Check authorization
        if user_role == 'buyer' and str(order['buyer_id']) != user_id:
            raise UnauthorizedError("You can only view your own orders")
        
        return jsonify({
            'status': 'success',
            'data': {
                'order_id': str(order['_id']),
                'items': order.get('items'),
                'total_price': order.get('total_price'),
                'status': order.get('status'),
                'shipping_address': order.get('shipping_address'),
                'created_at': order.get('created_at').isoformat() if order.get('created_at') else None,
                'updated_at': order.get('updated_at').isoformat() if order.get('updated_at') else None
            }
        }), 200
    
    except (NotFoundError, UnauthorizedError) as e:
        status_code = 404 if isinstance(e, NotFoundError) else 403
        return jsonify({'status': 'error', 'message': str(e)}), status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@orders_bp.route('/<order_id>/status', methods=['PUT'])
@jwt_required()
@role_required(['admin'])
def update_order_status(order_id):
    """Update order status (admin only)"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status or new_status not in Order.STATUSES:
            raise BadRequestError(f"Invalid status. Must be one of {Order.STATUSES}")
        
        order = Order.find_by_id(order_id)
        
        if not order:
            raise NotFoundError("Order not found")
        
        Order.update_status(order_id, new_status)
        
        return jsonify({
            'status': 'success',
            'message': f'Order status updated to {new_status}'
        }), 200
    
    except (BadRequestError, NotFoundError) as e:
        status_code = 400 if isinstance(e, BadRequestError) else 404
        return jsonify({'status': 'error', 'message': str(e)}), status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@orders_bp.route('/<order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order"""
    try:
        identity = get_identity()
        user_id = identity.get('user_id')
        
        order = Order.find_by_id(order_id)
        
        if not order:
            raise NotFoundError("Order not found")
        
        # Check ownership
        if str(order['buyer_id']) != user_id:
            raise UnauthorizedError("You can only cancel your own orders")
        
        # Can only cancel pending orders
        if order['status'] != 'pending':
            raise BadRequestError("Only pending orders can be cancelled")
        
        Order.update_status(order_id, 'cancelled')
        
        # Restore product quantities
        for item in order.get('items', []):
            product = Product.find_by_id(item['product_id'])
            new_quantity = product['quantity'] + item['quantity']
            Product.update(item['product_id'], {'quantity': new_quantity})
        
        return jsonify({
            'status': 'success',
            'message': 'Order cancelled successfully'
        }), 200
    
    except (NotFoundError, UnauthorizedError, BadRequestError) as e:
        if isinstance(e, NotFoundError):
            status_code = 404
        elif isinstance(e, UnauthorizedError):
            status_code = 403
        else:
            status_code = 400
        return jsonify({'status': 'error', 'message': str(e)}), status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
