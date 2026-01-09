import React from 'react';
import { Link } from 'react-router-dom';
import { formatPrice } from '../utils/helpers';

export const ProductCard = ({ product, onAddToCart }) => {
  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden">
      {/* Product Image */}
      <div className="h-40 bg-gradient-to-br from-green-100 to-green-50 flex items-center justify-center relative overflow-hidden">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover hover:scale-110 transition-transform duration-300"
          />
        ) : (
          <span className="text-4xl">🌽</span>
        )}
      </div>

      {/* Product Info */}
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 truncate">{product.name}</h3>

        <p className="text-sm text-gray-600 mt-1 truncate">
          {product.category && `📁 ${product.category}`}
        </p>

        <p className="text-sm text-gray-500 mt-2 h-10 line-clamp-2">
          {product.description}
        </p>

        {/* Rating */}
        {product.rating && (
          <div className="flex items-center mt-2">
            <span className="text-yellow-500">★</span>
            <span className="text-sm font-semibold ml-1">
              {product.rating.toFixed(1)}
            </span>
            {product.review_count && (
              <span className="text-sm text-gray-500 ml-1">
                ({product.review_count})
              </span>
            )}
          </div>
        )}

        {/* Price */}
        <div className="mt-4 flex items-baseline justify-between">
          <span className="text-2xl font-bold text-green-600">
            {formatPrice(product.price)}
          </span>
          {product.quantity && (
            <span className="text-sm text-gray-600">
              Stock: {product.quantity}
            </span>
          )}
        </div>

        {/* Actions */}
        <div className="mt-4 space-y-2">
          <Link
            to={`/product/${product.product_id}`}
            className="block text-center px-4 py-2 bg-white border-2 border-green-600 text-green-600 font-semibold rounded-lg hover:bg-green-50 transition"
          >
            View Details
          </Link>

          {onAddToCart && (
            <button
              onClick={() => onAddToCart(product)}
              className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition"
            >
              Add to Cart
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
