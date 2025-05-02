import React, { useEffect, useState } from 'react';
import Layout from '../../components/layout/Layout';

const OrderPage = () => {
  const [items, setItems] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [itemId, setItemId] = useState('');
  const [supplierId, setSupplierId] = useState('');
  const [qty, setQty] = useState(1);
  const [msg, setMsg] = useState('');

  useEffect(function() {
    fetch('http://127.0.0.1:8000/api/inventory/', {
      credentials: 'include'
    })
      .then(function(res) { return res.json(); })
      .then(function(data) { setItems(data); });

    fetch('http://127.0.0.1:8000/api/suppliers/', {
      credentials: 'include'
    })
      .then(function(res) { return res.json(); })
      .then(function(data) { setSuppliers(data); });
  }, []);

  function submit(e) {
    e.preventDefault();
    if (!itemId || !supplierId || qty <= 0) return;

    fetch('http://127.0.0.1:8000/api/orders/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        inventory_id: itemId,
        quantity_ordered: qty,
        supplier_id: supplierId,
      })
    }).then(function() {
      setMsg('Order submitted');
      setItemId('');
      setSupplierId('');
      setQty(1);
    });
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-gray-800 text-center">New Order</h2>

        <form onSubmit={submit} className="bg-white p-4 rounded border w-full max-w-md mx-auto">
          <div className="mb-3">
            <label className="block text-sm mb-1">Item</label>
            <select
              className="border px-2 py-1 rounded w-full"
              value={itemId}
              onChange={function(e) { setItemId(e.target.value); }}
            >
              <option value="">Choose</option>
              {items.map(function(it) {
                return (
                  <option key={it.id} value={it.id}>{it.item_name}</option>
                );
              })}
            </select>
          </div>

          <div className="mb-3">
            <label className="block text-sm mb-1">Supplier</label>
            <select
              className="border px-2 py-1 rounded w-full"
              value={supplierId}
              onChange={function(e) { setSupplierId(e.target.value); }}
            >
              <option value="">Choose</option>
              {suppliers.map(function(s) {
                return (
                  <option key={s.id} value={s.id}>{s.name}</option>
                );
              })}
            </select>
          </div>

          <div className="mb-3">
            <label className="block text-sm mb-1">Qty</label>
            <input
              type="number"
              className="border px-2 py-1 rounded w-full"
              value={qty}
              onChange={function(e) { setQty(parseInt(e.target.value) || 1); }}
            />
          </div>

          <button type="submit" className="w-full bg-blue-500 text-white py-1 rounded">Submit</button>
          {msg && <p className="text-green-600 mt-2 text-center text-sm">{msg}</p>}
        </form>
      </div>
    </Layout>
  );
};

export default OrderPage;