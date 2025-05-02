import React, { useState } from 'react';
import Layout from '../../components/layout/Layout';

const SettingPage = () => {
  const [name, setName] = useState('Inventory Management System');
  const [lang, setLang] = useState('English');
  const [registration, setRegistration] = useState(true);
  const [exportFmt, setExportFmt] = useState('CSV');
  const [launchDate, setLaunchDate] = useState('2024-12-31');

  async function handleSave() {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/settings/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          name,
          lang,
          registration,
          exportFmt,
          launchDate
        })
      });

      if (response.ok) {
        alert('Settings saved');
      } else {
        alert('Failed to save settings');
      }
    } catch (error) {
      alert('Error while saving settings');
    }
  }

  function handleReset() {
    setName('Inventory Management System');
    setLang('English');
    setRegistration(true);
    setExportFmt('CSV');
    setLaunchDate('2024-12-31');
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold text-gray-800 mb-5">Settings</h2>

        <div className="space-y-4">
          <div className="flex gap-4 items-center">
            <label htmlFor="name" className="w-1/4 text-gray-700">Name</label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={function(e) { setName(e.target.value); }}
              className="w-3/4 p-2 border rounded-md"
            />
          </div>

          <div className="flex gap-4 items-center">
            <label htmlFor="lang" className="w-1/4 text-gray-700">Language</label>
            <select
              id="lang"
              value={lang}
              onChange={function(e) { setLang(e.target.value); }}
              className="w-3/4 p-2 border rounded-md"
            >
              <option value="English">English</option>
              <option value="Chinese">Chinese</option>
            </select>
          </div>

          <div className="flex gap-4 items-center">
            <label htmlFor="exportFmt" className="w-1/4 text-gray-700">Export Format</label>
            <select
              id="exportFmt"
              value={exportFmt}
              onChange={function(e) { setExportFmt(e.target.value); }}
              className="w-3/4 p-2 border rounded-md"
            >
              <option value="CSV">CSV</option>
              <option value="Excel">Excel</option>
            </select>
          </div>

          <div className="flex gap-4 items-center">
            <label htmlFor="launchDate" className="w-1/4 text-gray-700">Launch Date</label>
            <input
              id="launchDate"
              type="date"
              value={launchDate}
              onChange={function(e) { setLaunchDate(e.target.value); }}
              className="w-3/4 p-2 border rounded-md"
            />
          </div>
        </div>

        <div className="flex justify-between mt-6">
          <button
            onClick={handleSave}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Save
          </button>
          <button
            onClick={handleReset}
            className="px-4 py-2 bg-gray-400 text-white rounded-md hover:bg-gray-500"
          >
            Reset
          </button>
        </div>
      </div>
    </Layout>
  );
};

export default SettingPage;