import React, { useState, useEffect } from 'react';
import Layout from '../../components/layout/Layout';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

interface NewUserData {
  name: string;
  email: string;
  password: string;
  role: string;
  username?: string;
}

interface EditUserData {
  name: string;
  role: string;
}

const ManagerUserPage = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [search, setSearch] = useState('');
  const [newUser, setNewUser] = useState<NewUserData>({ 
    name: '', 
    email: '', 
    password: '', 
    role: 'admin' 
  });
  const [showAdd, setShowAdd] = useState(false);
  const [editUser, setEditUser] = useState<User | null>(null);
  const [editForm, setEditForm] = useState<EditUserData>({ 
    name: '', 
    role: 'admin' 
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
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
      
      console.log('Auth status before fetch:', {
        isAuthenticated,
        tokenPresent: !!localStorage.getItem('access_token')
      });
      
      const response = await api.get(`/users/?search=${encodeURIComponent(search)}`);
      
      if (Array.isArray(response.data)) {
        setUsers(response.data);
      } else {
        console.error('Expected an array but got:', response.data);
        setUsers([]);
      }
    } catch (err) {
      console.error('Error loading users:', err);
      setError('Failed to load users. Please check your connection.');
    } finally {
      setLoading(false);
    }
  }

  async function addUser() {
    try {
      setError(null);
      
      // Prepare data for registration
      const userData = {
        name: newUser.name,
        email: newUser.email,
        password: newUser.password,
        role: newUser.role,
        username: newUser.email // Use email as username for Django
      };
      
      console.log('Sending user data:', { 
        ...userData, 
        password: '***', // Don't log the actual password
        role: userData.role // Explicitly log the role
      });
      
      const response = await api.post('/auth/register/', userData);
      
      console.log('User registration response:', response.status, response.data);
      
      // If successful, close the form and refresh the list
      setShowAdd(false);
      setNewUser({ name: '', email: '', password: '', role: 'admin' });
      
      // If the response contains the user data, add it to the list
      if (response.data.user) {
        setUsers([...users, response.data.user]);
      } else {
        // Otherwise, just reload the list
        await load();
      }
    } catch (err: any) {
      console.error('Error response:', err.response?.data);
      
      // Even if we get an error, the user might have been created anyway
      await load();
      
      // Display more specific error message if available
      const errorMessage = err.response?.data?.message || 
                           err.response?.data?.error || 
                           'Failed to add user. Check if the email is already in use.';
      setError(errorMessage);
    }
  }

  async function updateUser() {
    if (!editUser) return;
    
    try {
      setError(null);
      
      const userData = {
        name: editForm.name,
        role: editForm.role
      };
      
      console.log(`Updating user ${editUser.id} with data:`, userData);
      
      // Send the update request
      const response = await api.put(`/users/${editUser.id}/`, userData);
      
      console.log('User update response:', response.status, response.data);
      
      // Always reload the user list after update
      await load();
      // Close the edit form after the list is reloaded
      setEditUser(null);
    } catch (err: any) {
      console.error('Error updating user:', err);
      
      if (err.response?.status === 404) {
        console.error('API endpoint not found. Check your URLs in both frontend and backend.');
      }
      
      // Display more specific error message if available
      const errorMessage = err.response?.data?.message || 
                           err.response?.data?.error || 
                           'Failed to update user.';
      setError(errorMessage);
    }
  }

  async function removeUser(id: number) {
    if (!window.confirm('Delete this user?')) return;
    
    try {
      setError(null);
      
      await api.delete(`/users/${id}/`);
      
      // Remove the user from the list
      setUsers(users.filter(user => user.id !== id));
    } catch (err: any) {
      console.error('Error deleting user:', err);
      
      // Display more specific error message if available
      const errorMessage = err.response?.data?.message || 
                           err.response?.data?.error || 
                           'Failed to delete user.';
      setError(errorMessage);
    }
  }

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    load();
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-gray-800">Users</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSearch} className="flex gap-2 mb-4">
          <input
            className="border px-2 py-1 rounded w-full"
            placeholder="Search..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button className="bg-blue-500 text-white px-3 py-1 rounded">Search</button>
        </form>

        <button
          onClick={() => setShowAdd(true)}
          className="mb-4 bg-green-500 text-white px-3 py-1 rounded"
        >+ Add</button>

        {loading ? (
          <p>Loading users...</p>
        ) : users.length === 0 ? (
          <p>No users found.</p>
        ) : (
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
              {users.map((u, i) => (
                <tr key={u.id}>
                  <td className="border p-1 text-center">{i + 1}</td>
                  <td className="border p-1">{u.name}</td>
                  <td className="border p-1">{u.email}</td>
                  <td className="border p-1">{u.role}</td>
                  <td className="border p-1 text-center">
                    <button
                      className="text-blue-600 text-xs mr-2"
                      onClick={() => {
                        setEditUser(u);
                        setEditForm({ name: u.name, role: u.role });
                      }}
                    >Edit</button>
                    <button
                      className="text-red-600 text-xs"
                      onClick={() => removeUser(u.id)}
                    >Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {showAdd && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
            <div className="bg-white p-4 rounded w-72">
              <h3 className="text-md font-bold mb-2">Add User</h3>
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Name"
                value={newUser.name}
                onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
              />
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Email"
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
              />
              <input
                className="border w-full mb-2 px-2 py-1"
                type="password"
                placeholder="Password"
                value={newUser.password}
                onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
              />
              <select
                className="border w-full mb-4 px-2 py-1"
                value={newUser.role}
                onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
              >
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
                <option value="staff">Staff</option>
                <option value="supplier">Supplier</option>
              </select>
              <div className="flex justify-end">
                <button onClick={() => setShowAdd(false)} className="px-2 py-1 mr-2 bg-gray-300 rounded">Cancel</button>
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
                onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
              />
              <input
                className="border w-full mb-2 px-2 py-1 bg-gray-100"
                value={editUser.email}
                disabled
              />
              <select
                className="border w-full mb-4 px-2 py-1"
                value={editForm.role}
                onChange={(e) => setEditForm({ ...editForm, role: e.target.value })}
              >
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
                <option value="staff">Staff</option>
                <option value="supplier">Supplier</option>
              </select>
              <div className="flex justify-end">
                <button onClick={() => setEditUser(null)} className="px-2 py-1 mr-2 bg-gray-300 rounded">Cancel</button>
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