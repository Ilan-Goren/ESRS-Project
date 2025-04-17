import Layout from '../../components/layout/Layout';
import StatisticsRow from '../../components/dashboard/StatisticsRow';

const StaffDashboard = () => {
  const stats = [
    {
      title: "Test",
      value: 5,
      comparison: "Test2",
      color: 'yellow' as 'yellow',
    }
  ]

  return (
    <Layout>
      <div className="card">
        <h1 className="text-2xl font-bold mb-4">Staff Dashboard</h1>
        <p>Welcome to the staff dashboard!</p>
      </div>
      <StatisticsRow data={stats}/>
    </Layout>
  );
};

export default StaffDashboard;