import React, { useState, useEffect } from 'react';
import Layout from '../../components/layout/Layout';
import AdvancedSearch from '../../components/inventory/AdvancedSearch';

interface ManagerUserItem {
  id: number;
  name: string;
  email: string;
  password_hash: string;
  role: string;
  created_at: string;
}

const ManagerUserPage = () => {
  const [items, setItems] = useState<ManagerUserItem[]>([]);
  
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
    console.log('handleSearch called with:', filters);
    try {
      const queryParams = new URLSearchParams();

      if (filters.searchTerm) queryParams.append('search', filters.searchTerm);
      if (filters.category) queryParams.append('category', filters.category);
      if (filters.supplier) queryParams.append('supplier', filters.supplier);
      if (filters.minStock !== '' && filters.minStock !== undefined) queryParams.append('minStock', filters.minStock);
      if (filters.maxStock !== '' && filters.maxStock !== undefined) queryParams.append('maxStock', filters.maxStock);

      console.log('Final query:', queryParams.toString());

      const response = await fetch(`http://localhost/inventory-api/managerUser.php?${queryParams.toString()}`, {
        method: 'GET'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('API Response:', data);
    
      setItems(data);
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
      <h1 className="text-2xl font-bold mb-4">Management Page</h1>
      
      <AdvancedSearch 
        categories={categories} 
        suppliers={suppliers} 
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
                <th className="border border-gray-300 p-2">User Name</th>
                <th className="border border-gray-300 p-2">User Email</th>
                <th className="border border-gray-300 p-2">password_hash</th>
                <th className="border border-gray-300 p-2">role</th>
                <th className="border border-gray-300 p-2">created_at</th>
              </tr>
            </thead>
            <tbody>
              {items.map(item => (
                <tr key={item.id}>
                  <td className="border border-gray-300 p-2">{item.id}</td>
                  <td className="border border-gray-300 p-2">{item.name}</td>
                  <td className="border border-gray-300 p-2">{item.email}</td>
                  <td className="border border-gray-300 p-2">{item.password_hash}</td>
                  <td className="border border-gray-300 p-2">{item.role}</td>
                  <td className="border border-gray-300 p-2">{item.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </Layout>
  );
};

export default ManagerUserPage;