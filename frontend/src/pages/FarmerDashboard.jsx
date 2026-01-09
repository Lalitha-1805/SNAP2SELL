import React, { useState, useEffect } from 'react';
import { mlService, productService, cartService } from '../api/services';
import { Loader } from '../components/Loader';
import { formatPrice } from '../utils/helpers';

export const FarmerDashboard = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Upload states
  const [imageFile, setImageFile] = useState(null);
  const [cropName, setCropName] = useState('');
  const [location, setLocation] = useState('');
  const [gettingLocation, setGettingLocation] = useState(false);

  // ML Results
  const [mlResults, setMlResults] = useState(null);
  const [description, setDescription] = useState('');
  const [suggestedPrice, setSuggestedPrice] = useState(0);
  const [quantity, setQuantity] = useState(10);
  const [category, setCategory] = useState('Vegetables');
  const [soilType, setSoilType] = useState('');
  const [season, setSeason] = useState('');
  const [qualityGrade, setQualityGrade] = useState('A');

  // Products list
  const [myProducts, setMyProducts] = useState([]);
  const [productsLoading, setProductsLoading] = useState(false);

  const categories = ['Vegetables', 'Fruits', 'Grains', 'Spices', 'Dairy', 'Organic'];

  // Get current location
  const getCurrentLocation = async () => {
    setGettingLocation(true);
    setError('');

    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject);
      });

      const { latitude, longitude } = position.coords;
      setLocation(`${latitude.toFixed(4)}, ${longitude.toFixed(4)}`);
      setSuccess('Location retrieved successfully');
    } catch (err) {
      setError('Could not get location. Please enable GPS or enter manually.');
    } finally {
      setGettingLocation(false);
    }
  };

  // Handle image upload and ML analysis
  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setImageFile(file);
    setLoading(true);
    setError('');
    setMlResults(null);

    try {
      const formData = new FormData();
      formData.append('image', file);

      const response = await mlService.analyzeImage(formData);
      
      if (response.data.status === 'success') {
        const data = response.data.data;
        setMlResults(data);
        setDescription(data.description || '');
        setSuggestedPrice(data.suggested_price || 500);
        setCropName(data.crop_name || '');
        setSuccess('Image analyzed successfully!');
      }
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to analyze image';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  // Handle crop name input
  const handleCropNameChange = async (e) => {
    const name = e.target.value;
    setCropName(name);

    if (name.length > 2) {
      setLoading(true);
      setError('');

      try {
        const response = await mlService.recommendCrops({
          crop_name: name
        });

        if (response.data.status === 'success') {
          const data = response.data.data;
          setDescription(data.description || '');
          setSuggestedPrice(data.suggested_price || 500);
        }
      } catch (err) {
        console.error('Error getting crop info:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  // Submit product
  const handleSubmitProduct = async () => {
    if (!cropName || !description) {
      setError('Crop name and description are required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const productData = {
        name: cropName,
        description,
        price: parseFloat(suggestedPrice),
        quantity: parseInt(quantity),
        category,
        soil_type: soilType,
        season,
        quality_grade: qualityGrade,
        location
      };

      const response = await productService.createProduct(productData);

      if (response.status === 201) {
        setSuccess('Product created successfully!');
        resetForm();
        // Refresh products list
        fetchMyProducts();
      }
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to create product';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch farmer's products
  const fetchMyProducts = async () => {
    setProductsLoading(true);
    try {
      // Get current user's products
      const response = await productService.getProducts(1, 50);
      // Filter to only this farmer's products (in a real app, would have a dedicated endpoint)
      setMyProducts(response.data.data || []);
    } catch (err) {
      console.error('Error fetching products:', err);
    } finally {
      setProductsLoading(false);
    }
  };

  // Load products on mount
  useEffect(() => {
    fetchMyProducts();
  }, []);

  const resetForm = () => {
    setImageFile(null);
    setCropName('');
    setDescription('');
    setSuggestedPrice(0);
    setQuantity(10);
    setLocation('');
    setMlResults(null);
    setCategory('Vegetables');
    setSoilType('');
    setSeason('');
    setQualityGrade('A');
    setTimeout(() => setSuccess(''), 3000);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Farmer Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage your agricultural products with AI assistance</p>
        </div>

        {/* Messages */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700">
            ✅ {success}
          </div>
        )}

        {/* Tabs */}
        <div className="mb-8 flex gap-4 border-b">
          <button
            onClick={() => setActiveTab('upload')}
            className={`px-4 py-3 font-semibold border-b-2 transition ${
              activeTab === 'upload'
                ? 'border-green-600 text-green-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            Upload Product
          </button>
          <button
            onClick={() => setActiveTab('products')}
            className={`px-4 py-3 font-semibold border-b-2 transition ${
              activeTab === 'products'
                ? 'border-green-600 text-green-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            My Products ({myProducts.length})
          </button>
        </div>

        {/* Upload Tab */}
        {activeTab === 'upload' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Side - Upload */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Add New Product</h2>

              {/* Image Upload */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Upload Crop Image (Optional)
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-green-500 transition">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                    id="imageUpload"
                  />
                  <label htmlFor="imageUpload" className="cursor-pointer block">
                    {imageFile ? (
                      <>
                        <span className="text-2xl mb-2 block">✅</span>
                        <p className="text-sm text-gray-700">{imageFile.name}</p>
                      </>
                    ) : (
                      <>
                        <span className="text-4xl mb-2 block">📷</span>
                        <p className="text-gray-600 font-semibold">Upload crop image</p>
                        <p className="text-sm text-gray-500">AI will analyze for description & price</p>
                      </>
                    )}
                  </label>
                </div>
              </div>

              {/* Crop Name */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Crop Name *
                </label>
                <input
                  type="text"
                  value={cropName}
                  onChange={handleCropNameChange}
                  placeholder="e.g., Tomato, Wheat, Carrot"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <p className="text-xs text-gray-500 mt-1">Start typing to get AI suggestions</p>
              </div>

              {/* Description */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description *
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe your crop..."
                  rows="4"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                {mlResults && (
                  <p className="text-xs text-green-600 mt-1">✅ AI-generated description</p>
                )}
              </div>

              {/* Location */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Farm Location
                </label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    placeholder="e.g., 28.6139, 77.2090"
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  />
                  <button
                    onClick={getCurrentLocation}
                    disabled={gettingLocation}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg transition"
                  >
                    📍 GPS
                  </button>
                </div>
              </div>
            </div>

            {/* Right Side - Details */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Product Details</h2>

              {/* Price */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Price per Unit (₹) *
                </label>
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    value={suggestedPrice}
                    onChange={(e) => setSuggestedPrice(parseFloat(e.target.value))}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  />
                  {mlResults && (
                    <span className="px-3 py-1 bg-green-100 text-green-700 rounded text-sm font-semibold">
                      AI Suggested
                    </span>
                  )}
                </div>
              </div>

              {/* Quantity */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Quantity (Units) *
                </label>
                <input
                  type="number"
                  value={quantity}
                  onChange={(e) => setQuantity(parseInt(e.target.value))}
                  min="1"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>

              {/* Category */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category *
                </label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              {/* Soil Type */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Soil Type (Optional)
                </label>
                <input
                  type="text"
                  value={soilType}
                  onChange={(e) => setSoilType(e.target.value)}
                  placeholder="e.g., Loam, Clay, Sandy"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>

              {/* Season */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Season (Optional)
                </label>
                <select
                  value={season}
                  onChange={(e) => setSeason(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="">Select Season</option>
                  <option value="Kharif">Kharif (Monsoon)</option>
                  <option value="Rabi">Rabi (Winter)</option>
                  <option value="Zaid">Zaid (Summer)</option>
                  <option value="Year-round">Year-round</option>
                </select>
              </div>

              {/* Quality Grade */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Quality Grade
                </label>
                <select
                  value={qualityGrade}
                  onChange={(e) => setQualityGrade(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="A">Grade A (Premium)</option>
                  <option value="B">Grade B (Good)</option>
                  <option value="C">Grade C (Standard)</option>
                </select>
              </div>

              {/* Submit Button */}
              <button
                onClick={handleSubmitProduct}
                disabled={loading || !cropName || !description}
                className="w-full px-6 py-3 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white font-bold rounded-lg transition"
              >
                {loading ? 'Creating Product...' : 'Create Product'}
              </button>
            </div>
          </div>
        )}

        {/* Products Tab */}
        {activeTab === 'products' && (
          <div>
            {productsLoading ? (
              <Loader />
            ) : myProducts.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-lg shadow">
                <p className="text-lg text-gray-600">No products yet</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {myProducts.map(product => (
                  <div key={product.product_id} className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-bold text-gray-900">{product.name}</h3>
                    <p className="text-sm text-gray-600 mt-2">{product.description?.substring(0, 100)}...</p>
                    <div className="mt-4 space-y-2">
                      <p className="text-sm">
                        <span className="font-semibold">Price:</span> {formatPrice(product.price)}
                      </p>
                      <p className="text-sm">
                        <span className="font-semibold">Stock:</span> {product.quantity} units
                      </p>
                      <p className="text-sm">
                        <span className="font-semibold">Category:</span> {product.category}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
