import Layout from '../../components/layout/Layout';
import { useEffect, useState } from 'react';

const AdminDashboard = () => {
  const [info, setInfo] = useState({
    users: 0,
    suppliers: 0,
    roles: 0,
    uptime: 0,
  });

  useEffect(function() {
    fetch('http://localhost/inventory-api/adminDashboard.php')
      .then(function(res) { return res.json(); })
      .then(function(data) {
        setInfo({
          users: data.totalUsers,
          suppliers: data.suppliers,
          roles: data.totalRoles,
          uptime: data.systemUptimeDays,
        });
      })
      .catch(function() { alert('Failed to load'); });
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