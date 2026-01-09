import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { orderService } from '../api/services';
import { formatPrice, formatDate } from '../utils/helpers';
import { Loader } from '../components/Loader';

export const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [statusFilter, setStatusFilter] = useState('');

  // Fetch orders
  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true);
        setError('');
        
        const filters = statusFilter ? { status: statusFilter } : {};
        const response = await orderService.getOrders(page, 10, filters);
        
        setOrders(response.data.data || []);
        setTotalPages(response.data.pagination?.pages || 1);
      } catch (err) {
        const message = err.response?.data?.message || 'Failed to load orders';
        setError(message);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [page, statusFilter]);

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      processing: 'bg-blue-100 text-blue-800',
      shipped: 'bg-purple-100 text-purple-800',
      delivered: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusIcon = (status) => {
    const icons = {
      pending: '⏳',
      processing: '⚙️',
      shipped: '🚚',
      delivered: '✅',
      cancelled: '❌'
    };
    return icons[status] || '📦';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Orders</h1>
          <p className="text-gray-600 mt-2">Track and manage your orders</p>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {/* Status Filter */}
        <div className="mb-6 flex gap-2 flex-wrap">
          <button
            onClick={() => { setStatusFilter(''); setPage(1); }}
            className={`px-4 py-2 rounded-lg font-semibold transition ${
              statusFilter === ''
                ? 'bg-green-600 text-white'
                : 'bg-white border border-gray-300 hover:border-green-600'
            }`}
          >
            All
          </button>
          {['pending', 'processing', 'shipped', 'delivered', 'cancelled'].map(status => (
            <button
              key={status}
              onClick={() => { setStatusFilter(status); setPage(1); }}
              className={`px-4 py-2 rounded-lg font-semibold transition capitalize ${
                statusFilter === status
                  ? 'bg-green-600 text-white'
                  : 'bg-white border border-gray-300 hover:border-green-600'
              }`}
            >
              {status}
            </button>
          ))}
        </div>

        {/* Loading */}
        {loading ? (
          <Loader />
        ) : orders.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-lg text-gray-600 mb-6">No orders found</p>
            <Link
              to="/marketplace"
              className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition inline-block"
            >
              Start Shopping
            </Link>
          </div>
        ) : (
          <>
            {/* Orders List */}
            <div className="space-y-4">
              {orders.map(order => (
                <div key={order.order_id} className="bg-white rounded-lg shadow hover:shadow-lg transition p-6">
                  <div className="grid grid-cols-1 md:grid-cols-5 gap-4 items-start">
                    {/* Order ID & Date */}
                    <div>
                      <p className="text-sm text-gray-600">Order ID</p>
                      <p className="text-lg font-bold text-gray-900">#{order.order_id?.slice(0, 8)}</p>
                      <p className="text-sm text-gray-600 mt-1">
                        {formatDate(order.created_at)}
                      </p>
                    </div>

                    {/* Items Count */}
                    <div>
                      <p className="text-sm text-gray-600">Items</p>
                      <p className="text-lg font-bold text-gray-900">
                        {order.items?.length || 0} product{order.items?.length !== 1 ? 's' : ''}
                      </p>
                    </div>

                    {/* Amount */}
                    <div>
                      <p className="text-sm text-gray-600">Total Amount</p>
                      <p className="text-lg font-bold text-green-600">
                        {formatPrice(order.total_amount)}
                      </p>
                    </div>

                    {/* Status */}
                    <div>
                      <p className="text-sm text-gray-600">Status</p>
                      <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-semibold mt-1 ${getStatusColor(order.status)}`}>
                        {getStatusIcon(order.status)} {order.status?.charAt(0).toUpperCase() + order.status?.slice(1)}
                      </span>
                    </div>

                    {/* Action */}
                    <div className="text-right">
                      <Link
                        to={`/orders/${order.order_id}`}
                        className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition inline-block"
                      >
                        View Details
                      </Link>
                    </div>
                  </div>

                  {/* Items Preview */}
                  {order.items && order.items.length > 0 && (
                    <div className="mt-4 pt-4 border-t">
                      <p className="text-sm font-semibold text-gray-700 mb-2">Items:</p>
                      <div className="flex gap-2 flex-wrap">
                        {order.items.slice(0, 3).map((item, idx) => (
                          <span key={idx} className="px-2 py-1 bg-gray-100 rounded text-sm text-gray-700">
                            {item.name}
                          </span>
                        ))}
                        {order.items.length > 3 && (
                          <span className="px-2 py-1 bg-gray-100 rounded text-sm text-gray-700">
                            +{order.items.length - 3} more
                          </span>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-8 flex justify-center items-center space-x-2">
                <button
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-4 py-2 bg-white border border-gray-300 rounded-lg disabled:opacity-50"
                >
                  Previous
                </button>

                {Array.from({ length: totalPages }, (_, i) => i + 1).map(p => (
                  <button
                    key={p}
                    onClick={() => setPage(p)}
                    className={`px-4 py-2 rounded-lg font-semibold transition ${
                      p === page
                        ? 'bg-green-600 text-white'
                        : 'bg-white border border-gray-300 hover:border-green-600'
                    }`}
                  >
                    {p}
                  </button>
                ))}

                <button
                  onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-4 py-2 bg-white border border-gray-300 rounded-lg disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};
