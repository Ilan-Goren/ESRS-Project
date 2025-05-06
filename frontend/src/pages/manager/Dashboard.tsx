import Layout from '../../components/layout/Layout';
import { useEffect, useState } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const ManagerDashboard = () => {
  const [info, setInfo] = useState({
    inventory: 0,
    delivered: 0,
    pending: 0,
    shipped: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      loadDashboardData();
    }
  }, [isAuthenticated]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Try the manager dashboard endpoint
      const response = await api.get('/dashboard/manager/');
      
      setInfo({
        inventory: response.data.totalInventory || 0,
        delivered: response.data.ordersDelivered || 0,
        pending: response.data.ordersPending || 0,
        shipped: response.data.ordersShipped || 0,
      });
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      setError('Failed to load dashboard data');
      
      // Use sample data as fallback
      setInfo({
        inventory: 127,
        delivered: 45,
        pending: 12,
        shipped: 18
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-5 text-gray-800">Manager Dashboard</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-4">Loading dashboard data...</div>
        ) : (
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
        )}
      </div>
    </Layout>
  );
};

export default ManagerDashboard;