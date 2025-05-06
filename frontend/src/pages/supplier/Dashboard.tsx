import Layout from '../../components/layout/Layout';
import { useEffect, useState } from 'react';
import api from '../../services/api';

const SupplierDashboard = () => {
  const [info, setInfo] = useState({
    totalOrders: 0,
    pendingOrders: 0,
    deliveredOrders: 0,
    inTransitOrders: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Load supplier dashboard data
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // First try the actual supplier endpoint
      try {
        const response = await api.get('/dashboard/supplier/');
        
        // If successful, use this data
        setInfo({
          totalOrders: response.data.totalOrders || 0,
          pendingOrders: response.data.pendingOrders || 0,
          deliveredOrders: response.data.deliveredOrders || 0,
          inTransitOrders: response.data.inTransitOrders || 0
        });
        return;
      } catch (specificError) {
        console.log('Supplier dashboard endpoint failed, trying generic endpoint');
      }
      
      // If the specific endpoint fails, try the generic dashboard endpoint
      const response = await api.get('/dashboard/');
      
      // Extract any relevant data for a supplier
      setInfo({
        totalOrders: response.data.totalOrders || 0,
        pendingOrders: response.data.ordersPending || 0,
        deliveredOrders: response.data.ordersDelivered || 0,
        inTransitOrders: response.data.ordersShipped || 0
      });
      
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      setError('Failed to load dashboard data');
      
      // Use sample data for demonstration
      setInfo({
        totalOrders: 42,
        pendingOrders: 7,
        deliveredOrders: 31,
        inTransitOrders: 4
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-5 text-gray-800">Supplier Dashboard</h2>
        
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
              <p className="text-sm text-gray-600">Total Orders</p>
              <p className="text-xl text-green-500">{info.totalOrders}</p>
            </div>

            <div className="bg-white p-4 rounded border text-center">
              <p className="text-sm text-gray-600">Delivered</p>
              <p className="text-xl text-purple-500">{info.deliveredOrders}</p>
            </div>

            <div className="bg-white p-4 rounded border text-center">
              <p className="text-sm text-gray-600">Pending</p>
              <p className="text-xl text-blue-500">{info.pendingOrders}</p>
            </div>

            <div className="bg-white p-4 rounded border text-center">
              <p className="text-sm text-gray-600">In Transit</p>
              <p className="text-xl text-orange-500">{info.inTransitOrders}</p>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default SupplierDashboard;