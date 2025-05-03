import Layout from '../../components/layout/Layout';
import { useEffect, useState } from 'react';

const StaffDashboard = () => {
  const [info, setInfo] = useState({
    inventory: 0,
    delivered: 0,
    pending: 0,
    shipped: 0,
  });

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    
    fetch('http://127.0.0.1:8000/api/dashboard/staff/', {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      }
    })
      .then(res => {
        if (!res.ok) {
          throw new Error(`Status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        setInfo({
          lowStock: data.lowStockCount || 0,
          myTransactions: data.myTransactions || 0,
          additions: data.totalAdditions || 0,
          removals: data.totalRemovals || 0,
        });
      })
      .catch(error => {
        console.error('Failed to load dashboard data:', error);
        // Don't show an alert, just leave the default zeros
      });
  }, []);

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-5 text-gray-800">Dashboard</h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Inventory</p>
            <p className="text-xl text-green-500">{info.inventory}</p>
          </div>

          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Delivered</p>
            <p className="text-xl text-purple-500">{info.delivered}</p>
          </div>

          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Pending</p>
            <p className="text-xl text-blue-500">{info.pending}</p>
          </div>

          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Shipped</p>
            <p className="text-xl text-orange-500">{info.shipped}</p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default StaffDashboard;