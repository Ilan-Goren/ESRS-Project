import React, { useState, useEffect } from 'react';
import Layout from '../../components/layout/Layout';

type User = {
  id: number;
  name: string;
  email: string;
  role: string;
};


const ManagerUserPage = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [editUser, setEditUser] = useState<User | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [newUser, setNewUser] = useState({ name: '', email: '', password: '', role: 'admin' });
  const [showAdd, setShowAdd] = useState(false);
  const [editForm, setEditForm] = useState({ name: '', role: 'admin' });

  const getUsers = async (search = '') => {
    const query = search ? `?search=${encodeURIComponent(search)}` : '';
    const res = await fetch(`http://localhost/inventory-api/managerUser.php${query}`);
    const data = await res.json();
    setUsers(data);
  };

  const handleSearch = (e:React.FormEvent) => {
    e.preventDefault();
    getUsers(searchTerm);
  };

  const addUser = async () => {
    await fetch('http://localhost/inventory-api/managerUser.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newUser)
    });
    setShowAdd(false);
    setNewUser({ name: '', email: '', password: '', role: 'admin' });
    getUsers();
  };

  const updateUser = async () => {
    await fetch('http://localhost/inventory-api/managerUser.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'update',
        id: editUser?.id,
        name: editForm.name,
        role: editForm.role
      })
    });
    setEditUser(null);
    getUsers();
  };

  const deleteUser = async (id: number) => {
    if (!window.confirm('Delete this user?')) return;
    await fetch(`http://localhost/inventory-api/managerUser.php?id=${id}`, { method: 'DELETE' });
    getUsers();
  };

  useEffect(() => { getUsers(); }, []);

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">User Management</h1>

      {/* Search bar */}
      <form onSubmit={handleSearch} className="mb-4 flex items-center gap-2 w-full">
        <input
          type="text"
          placeholder="Search by name, email or role"
          className="border px-4 py-2 rounded text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 w-full"
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
        />
        <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Search</button>
      </form>

      <button onClick={() => setShowAdd(true)} className="mb-4 px-4 py-2 bg-green-600 text-white rounded">+ Add User</button>

      <table className="w-full border">
        <thead>
          <tr>
            <th className="border p-2">ID</th>
            <th className="border p-2">Name</th>
            <th className="border p-2">Email</th>
            <th className="border p-2">Role</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td className="border p-2">{u.id}</td>
              <td className="border p-2">{u.name}</td>
              <td className="border p-2">{u.email}</td>
              <td className="border p-2">{u.role}</td>
              <td className="border p-2">
                <button className="text-blue-500 mr-2" onClick={() => { setEditUser(u); setEditForm({ name: u.name, role: u.role }); }}>Edit</button>
                <button className="text-red-500" onClick={() => deleteUser(u.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {showAdd && (
        <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-4 rounded w-80">
            <h2 className="text-lg font-bold mb-2">Add User</h2>
            <input className="border w-full mb-2 px-2 py-1" placeholder="Name" value={newUser.name} onChange={e => setNewUser({ ...newUser, name: e.target.value })} />
            <input className="border w-full mb-2 px-2 py-1" placeholder="Email" value={newUser.email} onChange={e => setNewUser({ ...newUser, email: e.target.value })} />
            <input className="border w-full mb-2 px-2 py-1" placeholder="Password" value={newUser.password} onChange={e => setNewUser({ ...newUser, password: e.target.value })} />
            <select className="border w-full mb-4 px-2 py-1" value={newUser.role} onChange={e => setNewUser({ ...newUser, role: e.target.value })}>
              <option value="admin">Admin</option>
              <option value="manager">Manager</option>
              <option value="staff">Staff</option>
              <option value="supplier">Supplier</option>
            </select>
            <div className="flex justify-end">
              <button className="mr-2 px-3 py-1 bg-gray-300 rounded" onClick={() => setShowAdd(false)}>Cancel</button>
              <button className="px-3 py-1 bg-green-600 text-white rounded" onClick={addUser}>Add</button>
            </div>
          </div>
        </div>
      )}

      {editUser && (
        <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-4 rounded w-80">
            <h2 className="text-lg font-bold mb-2">Edit User</h2>
            <input className="border w-full mb-2 px-2 py-1" value={editForm.name} onChange={e => setEditForm({ ...editForm, name: e.target.value })} />
            <input className="border w-full mb-2 px-2 py-1 bg-gray-100" disabled value={editUser.email} />
            <select className="border w-full mb-4 px-2 py-1" value={editForm.role} onChange={e => setEditForm({ ...editForm, role: e.target.value })}>
              <option value="admin">Admin</option>
              <option value="manager">Manager</option>
              <option value="staff">Staff</option>
              <option value="supplier">Supplier</option>
            </select>
            <div className="flex justify-end">
              <button className="mr-2 px-3 py-1 bg-gray-300 rounded" onClick={() => setEditUser(null)}>Cancel</button>
              <button className="px-3 py-1 bg-blue-500 text-white rounded" onClick={updateUser}>Save</button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
};

export default ManagerUserPage;
