import Layout from '../../components/layout/Layout';
import StatisticsRow from '../../components/dashboard/StatisticsRow';

const ManagerDashboard = () => {
  const stats = [
    {
      title: "Test",
      value: 5,
      comparison: "Test2",
      color: 'red' as 'red',
    }
  ]

  return (
    <Layout>
      <div className="card">
        <h1 className="text-2xl font-bold mb-4">Manager Dashboard</h1>
        <p>Welcome to the manager dashboard!</p>
      </div>
      <StatisticsRow data={stats}/>
    </Layout>
  );
};

export default ManagerDashboard;