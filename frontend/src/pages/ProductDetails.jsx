import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { productService, reviewService, cartService, mlService } from '../api/services';
import { formatPrice } from '../utils/helpers';
import { Loader } from '../components/Loader';
import { useAuth } from '../auth/AuthContext';

export const ProductDetails = () => {
  const { productId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [notification, setNotification] = useState('');
  const [reviewForm, setReviewForm] = useState({
    rating: 5,
    comment: ''
  });
  const [submittingReview, setSubmittingReview] = useState(false);

  // Fetch product details
  useEffect(() => {
    const fetchProductDetails = async () => {
      try {
        setLoading(true);
        setError('');

        const response = await productService.getProduct(productId);
        setProduct(response.data.data);

        // Fetch reviews
        const reviewsResponse = await reviewService.getReviews(productId);
        setReviews(reviewsResponse.data.data || []);

        // Fetch recommendations
        const recsResponse = await mlService.recommendProducts(3);
        setRecommendations(recsResponse.data.data || []);
      } catch (err) {
        const message = err.response?.data?.message || 'Failed to load product';
        setError(message);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProductDetails();
  }, [productId]);

  const handleAddToCart = () => {
    if (!product) return;

    cartService.addToCart({
      product_id: product.product_id,
      name: product.name,
      price: product.price,
      image_url: product.image_url
    });

    setNotification(`${product.name} added to cart!`);
    setTimeout(() => setNotification(''), 3000);
  };

  const handleSubmitReview = async () => {
    if (!user) {
      setError('Please login to submit a review');
      return;
    }

    if (!reviewForm.comment.trim()) {
      setError('Please write a review');
      return;
    }

    setSubmittingReview(true);
    setError('');

    try {
      const reviewData = {
        rating: reviewForm.rating,
        comment: reviewForm.comment
      };

      await reviewService.createReview(productId, reviewData);
      setNotification('Review submitted successfully!');
      setReviewForm({ rating: 5, comment: '' });

      // Refresh reviews
      const reviewsResponse = await reviewService.getReviews(productId);
      setReviews(reviewsResponse.data.data || []);
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to submit review';
      setError(message);
    } finally {
      setSubmittingReview(false);
    }
  };

  if (loading) return <Loader fullScreen />;

  if (error && !product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-lg mb-6">{error}</p>
          <button
            onClick={() => navigate('/marketplace')}
            className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg"
          >
            Back to Marketplace
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      {/* Notification */}
      {notification && (
        <div className="fixed top-20 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-40">
          {notification}
        </div>
      )}

      <div className="max-w-6xl mx-auto px-4">
        {/* Back Button */}
        <button
          onClick={() => navigate('/marketplace')}
          className="mb-6 text-green-600 hover:text-green-700 font-semibold"
        >
          ← Back to Marketplace
        </button>

        {product && (
          <>
            {/* Product Details */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
              {/* Image */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="h-96 bg-gradient-to-br from-green-100 to-green-50 rounded-lg flex items-center justify-center overflow-hidden">
                  {product.image_url ? (
                    <img
                      src={product.image_url}
                      alt={product.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <span className="text-6xl">🌽</span>
                  )}
                </div>
              </div>

              {/* Details */}
              <div className="bg-white rounded-lg shadow p-6">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
                <p className="text-sm text-gray-600 mb-4">
                  {product.category && `📁 ${product.category}`}
                </p>

                {/* Rating */}
                {product.rating && (
                  <div className="flex items-center gap-2 mb-6">
                    <span className="text-yellow-500 text-xl">★</span>
                    <span className="font-bold text-lg">{product.rating.toFixed(1)}</span>
                    {product.review_count && (
                      <span className="text-gray-600">({product.review_count} reviews)</span>
                    )}
                  </div>
                )}

                {/* Price */}
                <div className="mb-6">
                  <p className="text-sm text-gray-600 mb-2">Price per Unit</p>
                  <p className="text-4xl font-bold text-green-600">{formatPrice(product.price)}</p>
                </div>

                {/* Stock */}
                <div className="mb-6">
                  <p className="text-sm text-gray-600 mb-2">Available Stock</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {product.quantity} units
                  </p>
                </div>

                {/* Details Grid */}
                {(product.soil_type || product.season || product.quality_grade) && (
                  <div className="grid grid-cols-3 gap-4 mb-6">
                    {product.soil_type && (
                      <div className="bg-green-50 p-3 rounded-lg">
                        <p className="text-xs text-gray-600">Soil Type</p>
                        <p className="font-semibold text-gray-900">{product.soil_type}</p>
                      </div>
                    )}
                    {product.season && (
                      <div className="bg-green-50 p-3 rounded-lg">
                        <p className="text-xs text-gray-600">Season</p>
                        <p className="font-semibold text-gray-900">{product.season}</p>
                      </div>
                    )}
                    {product.quality_grade && (
                      <div className="bg-green-50 p-3 rounded-lg">
                        <p className="text-xs text-gray-600">Grade</p>
                        <p className="font-semibold text-gray-900">{product.quality_grade}</p>
                      </div>
                    )}
                  </div>
                )}

                {/* Description */}
                <div className="mb-8">
                  <h2 className="text-lg font-bold text-gray-900 mb-2">Description</h2>
                  <p className="text-gray-700 leading-relaxed">{product.description}</p>
                </div>

                {/* Add to Cart */}
                <div className="space-y-4">
                  <div className="flex items-center gap-4">
                    <label className="text-sm font-medium text-gray-700">Quantity:</label>
                    <div className="flex items-center border border-gray-300 rounded-lg">
                      <button
                        onClick={() => setQuantity(Math.max(1, quantity - 1))}
                        className="px-4 py-2 hover:bg-gray-100"
                      >
                        −
                      </button>
                      <span className="px-6 py-2 border-l border-r border-gray-300">{quantity}</span>
                      <button
                        onClick={() => setQuantity(quantity + 1)}
                        className="px-4 py-2 hover:bg-gray-100"
                      >
                        +
                      </button>
                    </div>
                  </div>

                  <button
                    onClick={handleAddToCart}
                    disabled={product.quantity === 0}
                    className="w-full px-6 py-4 bg-green-600 hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold rounded-lg transition text-lg"
                  >
                    {product.quantity === 0 ? 'Out of Stock' : 'Add to Cart'}
                  </button>
                </div>
              </div>
            </div>

            {/* Reviews Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 bg-white rounded-lg shadow p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Customer Reviews</h2>

                {/* Review Form */}
                {user && (
                  <div className="mb-8 pb-8 border-b">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Leave a Review</h3>
                    {error && (
                      <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
                        {error}
                      </div>
                    )}

                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Rating
                        </label>
                        <select
                          value={reviewForm.rating}
                          onChange={(e) => setReviewForm({ ...reviewForm, rating: parseInt(e.target.value) })}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                        >
                          <option value="5">⭐⭐⭐⭐⭐ Excellent</option>
                          <option value="4">⭐⭐⭐⭐ Good</option>
                          <option value="3">⭐⭐⭐ Average</option>
                          <option value="2">⭐⭐ Poor</option>
                          <option value="1">⭐ Terrible</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Your Review
                        </label>
                        <textarea
                          value={reviewForm.comment}
                          onChange={(e) => setReviewForm({ ...reviewForm, comment: e.target.value })}
                          placeholder="Share your experience..."
                          rows="4"
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                        />
                      </div>

                      <button
                        onClick={handleSubmitReview}
                        disabled={submittingReview}
                        className="px-6 py-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white font-semibold rounded-lg transition"
                      >
                        {submittingReview ? 'Submitting...' : 'Submit Review'}
                      </button>
                    </div>
                  </div>
                )}

                {/* Reviews List */}
                {reviews.length === 0 ? (
                  <p className="text-gray-600">No reviews yet. Be the first to review!</p>
                ) : (
                  <div className="space-y-4">
                    {reviews.map(review => (
                      <div key={review._id} className="pb-4 border-b last:border-b-0">
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <p className="font-semibold text-gray-900">{review.user_name}</p>
                            <p className="text-sm text-yellow-500">
                              {'⭐'.repeat(review.rating)}
                            </p>
                          </div>
                          <p className="text-sm text-gray-600">
                            {new Date(review.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <p className="text-gray-700">{review.comment}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Recommendations */}
              {recommendations.length > 0 && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-lg font-bold text-gray-900 mb-4">You Might Also Like</h2>
                  <div className="space-y-4">
                    {recommendations.map(rec => (
                      <div
                        key={rec.product_id}
                        onClick={() => navigate(`/product/${rec.product_id}`)}
                        className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition cursor-pointer"
                      >
                        <h3 className="font-semibold text-gray-900 truncate">{rec.name}</h3>
                        <p className="text-green-600 font-bold mt-2">{formatPrice(rec.price)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};
