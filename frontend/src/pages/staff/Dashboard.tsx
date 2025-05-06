import React, { useEffect, useState } from 'react';
import Layout from '../../components/layout/Layout';
import api from '../../services/api';

const StaffDashboard = () => {
  const [info, setInfo] = useState({
    lowStock: 0,
    myTransactions: 0,
    additions: 0,
    removals: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    
    // FIXED: Removed the /api prefix since it's already in the base URL
    api.get('/dashboard/staff/')
      .then(response => {
        console.log("Dashboard data received:", response.data);
        setInfo({
          lowStock: response.data.lowStockCount || 0,
          myTransactions: response.data.myTransactions || 0,
          additions: response.data.totalAdditions || 0,
          removals: response.data.totalRemovals || 0
        });
        setLoading(false);
      })
      .catch(error => {
        console.error('Failed to load dashboard data:', error);
        setError('Failed to load dashboard data. Please try again later.');
        setLoading(false);
        
        // FIXED: Removed the /api prefix here too
        api.get('/test-dashboard/')
          .then(testResponse => {
            console.log("Test endpoint works:", testResponse.data);
          })
          .catch(testError => {
            console.error("Test endpoint also failed:", testError);
            
            // Try one more endpoint for debugging
            api.get('/users/')
              .then(usersResponse => {
                console.log("Users endpoint works:", usersResponse.data);
              })
              .catch(usersError => {
                console.error("All API endpoints failed, check server:", usersError);
              });
          });
      });
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="p-5">
          <h2 className="text-lg font-bold mb-5 text-gray-800">Dashboard</h2>
          <p>Loading dashboard data...</p>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="p-5">
          <h2 className="text-lg font-bold mb-5 text-gray-800">Dashboard</h2>
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-5 text-gray-800">Dashboard</h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Low Stock Items</p>
            <p className="text-xl text-green-500">{info.lowStock}</p>
          </div>

          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">My Transactions</p>
            <p className="text-xl text-purple-500">{info.myTransactions}</p>
          </div>

          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Total Additions</p>
            <p className="text-xl text-blue-500">{info.additions}</p>
          </div>

          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Total Removals</p>
            <p className="text-xl text-orange-500">{info.removals}</p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default StaffDashboard;