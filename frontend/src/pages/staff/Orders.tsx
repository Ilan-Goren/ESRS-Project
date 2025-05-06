import React, { useEffect, useState } from 'react';
import Layout from '../../components/layout/Layout';
import api from '../../services/api';

const OrderPage = () => {
  const [items, setItems] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [itemId, setItemId] = useState('');
  const [supplierId, setSupplierId] = useState('');
  const [qty, setQty] = useState(1);
  const [msg, setMsg] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError('');
        
        // Fetch inventory items
        const itemsResponse = await api.get('/inventory/');
        setItems(itemsResponse.data);
        
        // Fetch suppliers
        const suppliersResponse = await api.get('/suppliers/');
        setSuppliers(suppliersResponse.data);
      } catch (err) {
        console.error('Failed to load data:', err);
        setError('Failed to load necessary data. Please refresh and try again.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  async function submit(e) {
    e.preventDefault();
    
    if (!itemId || !supplierId || qty <= 0) {
      setError('Please fill out all fields with valid values');
      return;
    }
    
    setError('');
    setMsg('');
    
    try {
      await api.post('/orders/', {
        inventory_id: itemId,
        quantity_ordered: qty,
        supplier_id: supplierId,
      });
      
      setMsg('Order submitted successfully');
      // Reset form
      setItemId('');
      setSupplierId('');
      setQty(1);
    } catch (err) {
      console.error('Failed to submit order:', err);
      setError('Failed to submit order. Please try again.');
    }
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-gray-800 text-center">New Order</h2>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 max-w-md mx-auto">
            {error}
          </div>
        )}

        {loading ? (
          <p className="text-center">Loading...</p>
        ) : (
          <form onSubmit={submit} className="bg-white p-4 rounded border w-full max-w-md mx-auto">
            <div className="mb-3">
              <label className="block text-sm mb-1">Item</label>
              <select
                className="border px-2 py-1 rounded w-full"
                value={itemId}
                onChange={(e) => setItemId(e.target.value)}
              >
                <option value="">Choose</option>
                {items.map((item) => (
                  <option key={item.id} value={item.id}>{item.item_name}</option>
                ))}
              </select>
            </div>

            <div className="mb-3">
              <label className="block text-sm mb-1">Supplier</label>
              <select
                className="border px-2 py-1 rounded w-full"
                value={supplierId}
                onChange={(e) => setSupplierId(e.target.value)}
              >
                <option value="">Choose</option>
                {suppliers.map((supplier) => (
                  <option key={supplier.id} value={supplier.id}>{supplier.name}</option>
                ))}
              </select>
            </div>

            <div className="mb-3">
              <label className="block text-sm mb-1">Quantity</label>
              <input
                type="number"
                className="border px-2 py-1 rounded w-full"
                value={qty}
                min="1"
                onChange={(e) => setQty(parseInt(e.target.value) || 1)}
              />
            </div>

            <button type="submit" className="w-full bg-blue-500 text-white py-1 rounded">
              Submit Order
            </button>
            
            {msg && (
              <p className="text-green-600 mt-2 text-center text-sm">{msg}</p>
            )}
          </form>
        )}
      </div>
    </Layout>
  );
};

export default OrderPage;