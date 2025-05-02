import React, { useEffect, useState } from 'react';
import Layout from '../../components/layout/Layout';

const SupplierPage = () => {
  const [list, setList] = useState([]);
  const [search, setSearch] = useState('');
  const [form, setForm] = useState({ name: '', email: '', phone: '', contact: '' });
  const [showForm, setShowForm] = useState(false);
  const [editId, setEditId] = useState(null);

  useEffect(function() {
    load();
  }, []);

  function load() {
    fetch('http://localhost/inventory-api/supplierManager.php?search=' + encodeURIComponent(search))
      .then(function(res) { return res.json(); })
      .then(function(data) { setList(data); });
  }

  function save() {
    var data = { ...form };
    if (editId) {
      data.id = editId;
      data.action = 'update';
    }
    fetch('http://localhost/inventory-api/supplierManager.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(function() {
      load();
      setForm({ name: '', email: '', phone: '', contact: '' });
      setEditId(null);
      setShowForm(false);
    });
  }

  function remove(id) {
    if (!window.confirm('Delete this supplier?')) return;
    fetch('http://localhost/inventory-api/supplierManager.php?id=' + id, {
      method: 'DELETE'
    }).then(function() { load(); });
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-gray-800">Suppliers</h2>

        <div className="flex gap-2 mb-4">
          <input
            className="border px-2 py-1 rounded w-full"
            placeholder="Search..."
            value={search}
            onChange={function(e) { setSearch(e.target.value); }}
          />
          <button onClick={load} className="px-3 py-1 bg-blue-500 text-white rounded">Search</button>
        </div>

        <button
          onClick={function() {
            setShowForm(true);
            setForm({ name: '', email: '', phone: '', contact: '' });
            setEditId(null);
          }}
          className="mb-4 bg-green-500 text-white px-3 py-1 rounded"
        >+ Add</button>

        <table className="w-full border text-sm">
          <thead>
            <tr>
              <th className="border p-1">#</th>
              <th className="border p-1">Name</th>
              <th className="border p-1">Email</th>
              <th className="border p-1">Phone</th>
              <th className="border p-1">Contact Info</th>
              <th className="border p-1">Action</th>
            </tr>
          </thead>
          <tbody>
            {list.map(function(s, i) {
              return (
                <tr key={s.id}>
                  <td className="border p-1 text-center">{i + 1}</td>
                  <td className="border p-1">{s.name}</td>
                  <td className="border p-1">{s.email}</td>
                  <td className="border p-1">{s.phone}</td>
                  <td className="border p-1">{s.contact_info || ''}</td>
                  <td className="border p-1 text-center">
                    <button
                      onClick={function() {
                        setForm({ name: s.name, email: s.email, phone: s.phone || '', contact: s.contact_info || '' });
                        setEditId(s.id);
                        setShowForm(true);
                      }}
                      className="text-blue-600 text-xs mr-2"
                    >Edit</button>
                    <button
                      onClick={function() { remove(s.id); }}
                      className="text-red-600 text-xs"
                    >Delete</button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
            <div className="bg-white p-4 rounded w-72">
              <h3 className="text-md font-bold mb-2">{editId ? 'Edit' : 'Add'} Supplier</h3>
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Name"
                value={form.name}
                onChange={function(e) { setForm({ ...form, name: e.target.value }); }}
              />
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Email"
                value={form.email}
                onChange={function(e) { setForm({ ...form, email: e.target.value }); }}
              />
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Phone"
                value={form.phone}
                onChange={function(e) { setForm({ ...form, phone: e.target.value }); }}
              />
              <input
                className="border w-full mb-4 px-2 py-1"
                placeholder="Contact Info"
                value={form.contact}
                onChange={function(e) { setForm({ ...form, contact: e.target.value }); }}
              />
              <div className="flex justify-end">
                <button onClick={function() { setShowForm(false); }} className="px-2 py-1 mr-2 bg-gray-300 rounded">Cancel</button>
                <button onClick={save} className="px-2 py-1 bg-blue-500 text-white rounded">Save</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default SupplierPage;