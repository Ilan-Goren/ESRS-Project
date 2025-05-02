import React, { useEffect, useState } from 'react';
import Layout from '../../components/layout/Layout';

const DeliveriesPage = () => {
  const [orders, setOrders] = useState([]);
  const [msg, setMsg] = useState('');

  useEffect(function() {
    load();
  }, []);

  function load() {
    fetch('http://127.0.0.1:8000/api/orders/supplier/', {
      credentials: 'include'
    })
      .then(function(res) { return res.json(); })
      .then(function(data) { setOrders(data); })
      .catch(function() { alert('Load failed'); });
  }

  function update(id, status) {
    fetch(`http://127.0.0.1:8000/api/orders/${id}/status/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ status })
    })
      .then(function(res) { return res.json(); })
      .then(function(data) {
        setMsg(data.message || data.error || 'Updated');
        load();
      });
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-center text-gray-800">Deliveries</h2>
        {msg && <p className="text-center text-sm text-green-600 mb-2">{msg}</p>}

        <div className="overflow-x-auto">
          <table className="w-full border text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="border p-1 text-left">Order</th>
                <th className="border p-1 text-left">Item</th>
                <th className="border p-1 text-left">Qty</th>
                <th className="border p-1 text-left">Status</th>
                <th className="border p-1 text-left">Action</th>
              </tr>
            </thead>
            <tbody>
              {orders.length === 0 ? (
                <tr>
                  <td colSpan={5} className="text-center py-4">No orders</td>
                </tr>
              ) : (
                orders.map(function(o) {
                  return (
                    <tr key={o.id}>
                      <td className="border p-1">{o.id}</td>
                      <td className="border p-1">{o.item_name}</td>
                      <td className="border p-1">{o.quantity_ordered}</td>
                      <td className="border p-1">{o.status}</td>
                      <td className="border p-1 space-x-2">
                        <button
                          className="bg-blue-500 text-white px-2 py-1 rounded text-xs"
                          onClick={function() { update(o.id, 'shipped'); }}
                        >shipped</button>
                        <button
                          className="bg-green-600 text-white px-2 py-1 rounded text-xs"
                          onClick={function() { update(o.id, 'delivered'); }}
                        >delivered</button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
};

export default DeliveriesPage;