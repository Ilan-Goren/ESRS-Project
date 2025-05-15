import React, { useState, useEffect } from 'react';
import Layout from '../../components/layout/Layout';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const InventoryView = () => {
  const [list, setList] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      load();
    }
  }, [isAuthenticated]);

  async function load() {
    try {
      setLoading(true);
      setError(null);
      
      // Log authentication status for debugging
      console.log('Auth status before fetch:', {
        isAuthenticated,
        tokenPresent: !!localStorage.getItem('access_token')
      });
      
      // Use the API client
      const response = await api.get(`/inventory/${ search ? `?search=${encodeURIComponent(search)}` : '' }`);
      setList(response.data);
    } catch (err) {
      console.error('Failed to load inventory:', err);
      setError('Failed to load inventory. Please ensure you are logged in.');
    } finally {
      setLoading(false);
    }
  }

  function handleSearch(e) {
    e.preventDefault();
    load();
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-gray-800">Inventory</h2>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSearch} className="mb-4 flex gap-2">
          <input
            type="text"
            placeholder="Search..."
            className="border px-2 py-1 rounded w-full"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button type="submit" className="bg-blue-500 text-white px-3 py-1 rounded">Search</button>
        </form>

        {loading ? (
          <p>Loading inventory data...</p>
        ) : list.length === 0 ? (
          <p>No inventory items found.</p>
        ) : (
          <table className="w-full border text-sm">
            <thead>
              <tr>
                <th className="border p-1">#</th>
                <th className="border p-1">Product</th>
                <th className="border p-1">Qty</th>
                <th className="border p-1">Supplier</th>
              </tr>
            </thead>
            <tbody>
              {list.map((item, i) => (
                <tr key={item.id}>
                  <td className="border p-1 text-center">{i + 1}</td>
                  <td className="border p-1">{item.item_name}</td>
                  <td className="border p-1 text-center">{item.quantity}</td>
                  <td className="border p-1">{item.supplier}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </Layout>
  );
};

export default InventoryView;