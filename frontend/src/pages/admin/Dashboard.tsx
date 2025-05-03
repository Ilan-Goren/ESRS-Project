import Layout from '../../components/layout/Layout';
import { useEffect, useState } from 'react';

const AdminDashboard = () => {
  const [info, setInfo] = useState({
    users: 0,
    suppliers: 0,
    roles: 0,
    uptime: 0,
  });

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    console.log("Token available:", !!token);
    
    fetch('http://127.0.0.1:8000/api/dashboard/', {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      }
    })
      .then(res => {
        console.log("API response status:", res.status);
        if (!res.ok) {
          throw new Error(`Status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        console.log("Dashboard data received:", data);
        setInfo({
          users: data.totalUsers || 0,
          suppliers: data.suppliers || 0,
          roles: data.totalRoles || 0,
          uptime: data.systemUptimeDays || 0,
        });
      })
      .catch(error => {
        console.error('Failed to load dashboard data:', error);
      });
  }, []);

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-5 text-gray-800">Dashboard</h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Users</p>
            <p className="text-xl text-blue-500">{info.users}</p>
          </div>

          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Suppliers</p>
            <p className="text-xl text-green-500">{info.suppliers}</p>
          </div>

          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Roles</p>
            <p className="text-xl text-purple-500">{info.roles}</p>
          </div>

          <div className="bg-white p-4 rounded border text-center">
            <p className="text-sm text-gray-600">Uptime (Days)</p>
            <p className="text-xl text-orange-500">{info.uptime}</p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default AdminDashboard;