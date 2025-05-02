import React, { useState } from 'react';
import Layout from '../../components/layout/Layout';

const ReportPage = () => {
  const [type, setType] = useState('inventory');
  const [range, setRange] = useState('last7Days');
  const [format, setFormat] = useState('csv');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  async function exportReport() {
    setLoading(true);
    setMessage('');
    try {
      const response = await fetch('http://127.0.0.1:8000/api/reports/export/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ type, range, format }),
      });

      if (response.ok) {
        setMessage('Export done successfully!');
      } else {
        setMessage('Failed to export report.');
      }
    } catch (error) {
      setMessage('Failed to export report.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Layout>
      <h2 className="text-lg font-bold text-gray-800 mb-5">Report Export</h2>

      <div className="space-y-4">
        <div className="flex gap-4 items-center">
          <label htmlFor="type" className="w-1/4 text-gray-700">Type</label>
          <select
            id="type"
            value={type}
            onChange={function(e) { setType(e.target.value); }}
            className="w-3/4 p-2 border rounded-md"
          >
            <option value="inventory">Inventory</option>
            <option value="sales">Sales</option>
          </select>
        </div>

        <div className="flex gap-4 items-center">
          <label htmlFor="range" className="w-1/4 text-gray-700">Range</label>
          <select
            id="range"
            value={range}
            onChange={function(e) { setRange(e.target.value); }}
            className="w-3/4 p-2 border rounded-md"
          >
            <option value="last7Days">Last 7 Days</option>
            <option value="last30Days">Last 30 Days</option>
          </select>
        </div>

        <div className="flex gap-4 items-center">
          <label htmlFor="format" className="w-1/4 text-gray-700">Format</label>
          <select
            id="format"
            value={format}
            onChange={function(e) { setFormat(e.target.value); }}
            className="w-3/4 p-2 border rounded-md"
          >
            <option value="csv">CSV</option>
            <option value="excel">Excel</option>
          </select>
        </div>
      </div>

      <div className="mt-6">
        <button
          onClick={exportReport}
          disabled={loading}
          className={`w-full py-2 text-white rounded-md ${loading ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'}`}
        >
          {loading ? 'Exporting...' : 'Export'}
        </button>
        {message && <p className={`${loading ? 'text-red-500' : 'text-green-500'} mt-2`}>{message}</p>}
      </div>
    </Layout>
  );
};

export default ReportPage;