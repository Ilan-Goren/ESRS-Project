import React, { useEffect, useState } from 'react';
import Layout from '../../components/layout/Layout';

const SupplierOrders = () => {
  const [orders, setOrders] = useState([]);

  useEffect(function() {
    fetch('http://localhost/inventory-api/supplierOrders.php')
      .then(function(res) { return res.json(); })
      .then(function(data) { setOrders(data); })
      .catch(function() { alert('Load failed'); });
  }, []);

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-center text-gray-800">My Orders</h2>

        <div className="overflow-x-auto">
          <table className="w-full border text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="border p-1 text-left">ID</th>
                <th className="border p-1 text-left">Item</th>
                <th className="border p-1 text-left">Qty</th>
                <th className="border p-1 text-left">Status</th>
                <th className="border p-1 text-left">Date</th>
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
                      <td className="border p-1">{o.order_date}</td>
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

export default SupplierOrders;