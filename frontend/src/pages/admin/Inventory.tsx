import React, { useState, useEffect } from 'react';
import Layout from '../../components/layout/Layout';
import AdvancedSearch from '../../components/inventory/AdvancedSearch';
import inventoryService, { InventoryItem } from '../../services/inventoryService';
import { useAuth } from '../../context/AuthContext';

const InventoryPage = () => {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();
  
  const categories = [
    { id: 'Vegetables', name: 'Vegetables' },
    { id: 'Dairy', name: 'Dairy' },
    { id: 'Meat', name: 'Meat' }
  ];

  const suppliers = [
    { id: 1, name: 'Fresh Veggies Ltd.' },
    { id: 2, name: 'Dairy Co.' },
    { id: 3, name: 'Meat Distributors Inc.' }
  ];

  const handleSearch = async (filters: any) => {
    if (!isAuthenticated) {
      setError('You must be logged in to view inventory');
      setLoading(false);
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      console.log('handleSearch called with:', filters);
      
      // Log authentication status for debugging
      console.log('Auth token present:', !!localStorage.getItem('access_token'));
      console.log('Auth state:', { isAuthenticated });
      
      // Convert the filters to the format expected by the service
      const searchFilters = {
        searchTerm: filters.searchTerm,
        category: filters.category,
        supplier: filters.supplier,
        minStock: filters.minStock,
        maxStock: filters.maxStock
      };
      
      // Use the inventory service instead of direct fetch
      const data = await inventoryService.getInventory(searchFilters);
      
      console.log('API Response:', data);
      setItems(data);
    } catch (error) {
      console.error('Error fetching inventory:', error);
      setError('Failed to load inventory. Please ensure you are logged in and try again.');
    } finally {
      setLoading(false);
    }
  };

  // Load everything on first page load
  useEffect(() => {
    handleSearch({});
  }, [isAuthenticated]); // Re-run when authentication status changes

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Inventory Management</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <AdvancedSearch 
        categories={categories} 
        suppliers={suppliers} 
        onSearch={handleSearch} 
      />

      {/* Inventory Table */}
      <div className="mt-6">
        {loading ? (
          <p>Loading inventory data...</p>
        ) : items.length === 0 ? (
          <p>No items found.</p>
        ) : (
          <table className="w-full table-auto border-collapse border border-gray-300">
            <thead>
              <tr>
                <th className="border border-gray-300 p-2">ID</th>
                <th className="border border-gray-300 p-2">Item Name</th>
                <th className="border border-gray-300 p-2">Category</th>
                <th className="border border-gray-300 p-2">Quantity</th>
                <th className="border border-gray-300 p-2">Reorder Level</th>
                <th className="border border-gray-300 p-2">Expiry Date</th>
                <th className="border border-gray-300 p-2">Supplier</th>
                <th className="border border-gray-300 p-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.map(item => (
                <tr key={item.id}>
                  <td className="border border-gray-300 p-2">{item.id}</td>
                  <td className="border border-gray-300 p-2">{item.item_name}</td>
                  <td className="border border-gray-300 p-2">{item.category}</td>
                  <td className={`border border-gray-300 p-2 ${item.quantity <= item.reorder_level ? 'text-red-600 font-bold' : ''}`}>
                    {item.quantity}
                  </td>
                  <td className="border border-gray-300 p-2">{item.reorder_level}</td>
                  <td className="border border-gray-300 p-2">{item.expiry_date}</td>
                  <td className="border border-gray-300 p-2">{item.supplier_name}</td>
                  <td className="border border-gray-300 p-2">
                    <div className="flex space-x-2">
                      <button className="text-blue-500 hover:text-blue-700">Edit</button>
                      <button className="text-red-500 hover:text-red-700">Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </Layout>
  );
};

export default InventoryPage;