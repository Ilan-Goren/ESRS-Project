import Layout from '../../components/layout/Layout';
import StatisticsRow from '../../components/dashboard/StatisticsRow';

const AdminDashboard = () => {
  const stats = [
    {
      title: "Test",
      value: 5,
      comparison: "Test2",
      color: 'green' as 'green',
    }
  ]

  return (
    <Layout>
      <div className="card">
        <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
        <p>Welcome to the admin dashboard!</p>
      </div>
      <StatisticsRow data={stats}/>
    </Layout>
  );
};

export default AdminDashboard;