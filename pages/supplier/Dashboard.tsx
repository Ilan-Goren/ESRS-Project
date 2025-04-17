import Layout from '../../components/layout/Layout';
import StatisticsRow from '../../components/dashboard/StatisticsRow';

const SupplierDashboard = () => {
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
        <h1 className="text-2xl font-bold mb-4">Supplier Dashboard</h1>
        <p>Welcome to the supplier dashboard!</p>
      </div>
      <StatisticsRow data={stats}/>
    </Layout>
  );
};

export default SupplierDashboard;