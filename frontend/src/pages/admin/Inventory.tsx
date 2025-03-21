import React, { useState, useEffect } from 'react';
import Layout from '../../components/layout/Layout';
import AdvancedSearch from '../../components/inventory/AdvancedSearch';
import api from '../../services/api';

interface InventoryItem {
  id: number;
  sku: string | null;
  item_name: string;
  category: string;
  quantity: number;
  reorder_level: number;
  expiry_date: string;
  supplier: number | null;
}

const InventoryPage = () => {
  const [items, setItems] = useState<InventoryItem[]>([]);
  
  const categories = [
    { id: 'Vegetables', name: 'Vegetables' },
    { id: 'Dairy', name: 'Dairy' },
    { id: 'Meat', name: 'Meat' }
  ];

  const handleSearch = async (filters: any) => {
    console.log('handleSearch called with:', filters);
    try {
      const queryParams = new URLSearchParams();

      if (filters.searchTerm) queryParams.append('search', filters.searchTerm);
      if (filters.category) queryParams.append('category', filters.category);
      if (filters.supplier) queryParams.append('supplier', filters.supplier);
      if (filters.minStock !== '' && filters.minStock !== undefined) queryParams.append('min_quantity', filters.minStock);
      if (filters.maxStock !== '' && filters.maxStock !== undefined) queryParams.append('max_quantity', filters.maxStock);

      console.log('Final query:', queryParams.toString());

    const response = await api.get(`inventory/?${queryParams.toString()}`);

      console.log('API Response:', response.data);
    
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching inventory:', error);
    }
  };

  // Optional: load everything on first page load
  useEffect(() => {
    handleSearch({});
  }, []);

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Inventory Management</h1>
      
      <AdvancedSearch 
        categories={categories} 
        suppliers={[]} 
        onSearch={handleSearch} 
      />

      {/* Inventory Table */}
      <div className="mt-6">
        {items.length === 0 ? (
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
              </tr>
            </thead>
            <tbody>
              {items.map(item => (
                <tr key={item.id}>
                  <td className="border border-gray-300 p-2">{item.id}</td>
                  <td className="border border-gray-300 p-2">{item.item_name}</td>
                  <td className="border border-gray-300 p-2">{item.category}</td>
                  <td className="border border-gray-300 p-2">{item.quantity}</td>
                  <td className="border border-gray-300 p-2">{item.reorder_level}</td>
                  <td className="border border-gray-300 p-2">{item.expiry_date}</td>
                  <td className="border border-gray-300 p-2">{item.supplier}</td>
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