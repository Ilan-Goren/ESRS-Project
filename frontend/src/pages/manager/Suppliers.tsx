import React, { useEffect, useState } from 'react';
import Layout from '../../components/layout/Layout';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const SupplierPage = () => {
  const [list, setList] = useState([]);
  const [search, setSearch] = useState('');
  const [form, setForm] = useState({ name: '', email: '', phone: '', contact: '' });
  const [showForm, setShowForm] = useState(false);
  const [editId, setEditId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      load();
    }
  }, [isAuthenticated]);

  async function load() {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.get(`/suppliers/?search=${encodeURIComponent(search)}`);
      setList(response.data);
    } catch (err) {
      console.error('Error loading suppliers:', err);
      setError('Failed to load suppliers. Please check your connection.');
    } finally {
      setLoading(false);
    }
  }

  async function save() {
    try {
      if (editId) {
        await api.put(`/suppliers/${editId}/`, { ...form });
      } else {
        await api.post('/suppliers/', { ...form });
      }
      
      load();
      setForm({ name: '', email: '', phone: '', contact: '' });
      setEditId(null);
      setShowForm(false);
    } catch (err) {
      console.error('Error saving supplier:', err);
      alert('Failed to save supplier');
    }
  }

  async function remove(id) {
    if (!window.confirm('Delete this supplier?')) return;
    
    try {
      await api.delete(`/suppliers/${id}/`);
      load();
    } catch (err) {
      console.error('Error deleting supplier:', err);
      alert('Failed to delete supplier');
    }
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-gray-800">Suppliers</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <div className="flex gap-2 mb-4">
          <input
            className="border px-2 py-1 rounded w-full"
            placeholder="Search..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button onClick={load} className="px-3 py-1 bg-blue-500 text-white rounded">Search</button>
        </div>

        <button
          onClick={() => {
            setShowForm(true);
            setForm({ name: '', email: '', phone: '', contact: '' });
            setEditId(null);
          }}
          className="mb-4 bg-green-500 text-white px-3 py-1 rounded"
        >+ Add</button>

        {loading ? (
          <p>Loading suppliers...</p>
        ) : (
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
              {list.map((s, i) => (
                <tr key={s.id}>
                  <td className="border p-1 text-center">{i + 1}</td>
                  <td className="border p-1">{s.name}</td>
                  <td className="border p-1">{s.email}</td>
                  <td className="border p-1">{s.phone}</td>
                  <td className="border p-1">{s.contact_info || ''}</td>
                  <td className="border p-1 text-center">
                    <button
                      onClick={() => {
                        setForm({ 
                          name: s.name, 
                          email: s.email, 
                          phone: s.phone || '', 
                          contact: s.contact_info || '' 
                        });
                        setEditId(s.id);
                        setShowForm(true);
                      }}
                      className="text-blue-600 text-xs mr-2"
                    >Edit</button>
                    <button
                      onClick={() => remove(s.id)}
                      className="text-red-600 text-xs"
                    >Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
            <div className="bg-white p-4 rounded w-72">
              <h3 className="text-md font-bold mb-2">{editId ? 'Edit' : 'Add'} Supplier</h3>
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Name"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Phone"
                value={form.phone}
                onChange={(e) => setForm({ ...form, phone: e.target.value })}
              />
              <input
                className="border w-full mb-4 px-2 py-1"
                placeholder="Contact Info"
                value={form.contact}
                onChange={(e) => setForm({ ...form, contact: e.target.value })}
              />
              <div className="flex justify-end">
                <button onClick={() => setShowForm(false)} className="px-2 py-1 mr-2 bg-gray-300 rounded">Cancel</button>
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