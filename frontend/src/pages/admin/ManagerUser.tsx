import React, { useState, useEffect } from 'react';
import Layout from '../../components/layout/Layout';

const ManagerUserPage = () => {
  const [users, setUsers] = useState([]);
  const [search, setSearch] = useState('');
  const [newUser, setNewUser] = useState({ name: '', email: '', password: '', role: 'admin' });
  const [showAdd, setShowAdd] = useState(false);
  const [editUser, setEditUser] = useState(null);
  const [editForm, setEditForm] = useState({ name: '', role: 'admin' });

  useEffect(function() {
    load();
  }, []);

  function load() {
    fetch('http://localhost/inventory-api/managerUser.php?search=' + encodeURIComponent(search))
      .then(function(res) { return res.json(); })
      .then(function(data) { setUsers(data); })
      .catch(function() { alert('Load failed'); });
  }

  function addUser() {
    fetch('http://localhost/inventory-api/managerUser.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newUser)
    }).then(function() {
      setShowAdd(false);
      setNewUser({ name: '', email: '', password: '', role: 'admin' });
      load();
    });
  }

  function updateUser() {
    fetch('http://localhost/inventory-api/managerUser.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'update',
        id: editUser.id,
        name: editForm.name,
        role: editForm.role
      })
    }).then(function() {
      setEditUser(null);
      load();
    });
  }

  function removeUser(id) {
    if (!window.confirm('Delete this user?')) return;
    fetch('http://localhost/inventory-api/managerUser.php?id=' + id, {
      method: 'DELETE'
    }).then(function() { load(); });
  }

  function handleSearch(e) {
    e.preventDefault();
    load();
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-gray-800">Users</h2>

        <form onSubmit={handleSearch} className="flex gap-2 mb-4">
          <input
            className="border px-2 py-1 rounded w-full"
            placeholder="Search..."
            value={search}
            onChange={function(e) { setSearch(e.target.value); }}
          />
          <button className="bg-blue-500 text-white px-3 py-1 rounded">Search</button>
        </form>

        <button
          onClick={function() { setShowAdd(true); }}
          className="mb-4 bg-green-500 text-white px-3 py-1 rounded"
        >+ Add</button>

        <table className="w-full border text-sm">
          <thead>
            <tr>
              <th className="border p-1">#</th>
              <th className="border p-1">Name</th>
              <th className="border p-1">Email</th>
              <th className="border p-1">Role</th>
              <th className="border p-1">Action</th>
            </tr>
          </thead>
          <tbody>
            {users.map(function(u, i) {
              return (
                <tr key={u.id}>
                  <td className="border p-1 text-center">{i + 1}</td>
                  <td className="border p-1">{u.name}</td>
                  <td className="border p-1">{u.email}</td>
                  <td className="border p-1">{u.role}</td>
                  <td className="border p-1 text-center">
                    <button
                      className="text-blue-600 text-xs mr-2"
                      onClick={function() {
                        setEditUser(u);
                        setEditForm({ name: u.name, role: u.role });
                      }}
                    >Edit</button>
                    <button
                      className="text-red-600 text-xs"
                      onClick={function() { removeUser(u.id); }}
                    >Delete</button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {showAdd && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
            <div className="bg-white p-4 rounded w-72">
              <h3 className="text-md font-bold mb-2">Add User</h3>
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Name"
                value={newUser.name}
                onChange={function(e) { setNewUser({ ...newUser, name: e.target.value }); }}
              />
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Email"
                value={newUser.email}
                onChange={function(e) { setNewUser({ ...newUser, email: e.target.value }); }}
              />
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Password"
                value={newUser.password}
                onChange={function(e) { setNewUser({ ...newUser, password: e.target.value }); }}
              />
              <select
                className="border w-full mb-4 px-2 py-1"
                value={newUser.role}
                onChange={function(e) { setNewUser({ ...newUser, role: e.target.value }); }}
              >
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
                <option value="staff">Staff</option>
                <option value="supplier">Supplier</option>
              </select>
              <div className="flex justify-end">
                <button onClick={function() { setShowAdd(false); }} className="px-2 py-1 mr-2 bg-gray-300 rounded">Cancel</button>
                <button onClick={addUser} className="px-2 py-1 bg-green-500 text-white rounded">Add</button>
              </div>
            </div>
          </div>
        )}

        {editUser && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
            <div className="bg-white p-4 rounded w-72">
              <h3 className="text-md font-bold mb-2">Edit User</h3>
              <input
                className="border w-full mb-2 px-2 py-1"
                value={editForm.name}
                onChange={function(e) { setEditForm({ ...editForm, name: e.target.value }); }}
              />
              <input
                className="border w-full mb-2 px-2 py-1 bg-gray-100"
                value={editUser.email}
                disabled
              />
              <select
                className="border w-full mb-4 px-2 py-1"
                value={editForm.role}
                onChange={function(e) { setEditForm({ ...editForm, role: e.target.value }); }}
              >
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
                <option value="staff">Staff</option>
                <option value="supplier">Supplier</option>
              </select>
              <div className="flex justify-end">
                <button onClick={function() { setEditUser(null); }} className="px-2 py-1 mr-2 bg-gray-300 rounded">Cancel</button>
                <button onClick={updateUser} className="px-2 py-1 bg-blue-500 text-white rounded">Save</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default ManagerUserPage;