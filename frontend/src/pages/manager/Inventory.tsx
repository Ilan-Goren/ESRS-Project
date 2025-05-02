import React, { useState, useEffect } from 'react';
import Layout from '../../components/layout/Layout';

const InventoryPage = () => {
  const [list, setList] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [search, setSearch] = useState('');
  const [showAdd, setShowAdd] = useState(false);
  const [addForm, setAddForm] = useState({ product: '', quantity: 0, supplier: '' });
  const [editForm, setEditForm] = useState({ id: null, productName: '', quantity: 0, supplier: '' });
  const [showEdit, setShowEdit] = useState(false);

  useEffect(function () {
    fetchData();
    fetchSuppliers();
  }, []);

  function fetchData() {
    fetch('http://localhost/inventory-api/managerInventory.php?search=' + encodeURIComponent(search))
      .then(res => res.json())
      .then(data => {
        console.log('[Inventory List]', data);
        setList(data);
      });
  }

  function fetchSuppliers() {
    fetch('http://localhost/inventory-api/suppliers.php')
      .then(res => res.json())
      .then(data => setSuppliers(data));
  }

  function addItem() {
    fetch('http://localhost/inventory-api/managerInventory.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: addForm.product,
        quantity: addForm.quantity,
        supplier: addForm.supplier,
      })
    }).then(() => {
      setAddForm({ product: '', quantity: 0, supplier: '' });
      setShowAdd(false);
      fetchData();
    });
  }

  function updateItem() {
    fetch('http://localhost/inventory-api/managerInventory.php?action=update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: editForm.id,
        item_name: editForm.productName,
        quantity: editForm.quantity,
        supplier: editForm.supplier
      })
    }).then(() => {
      setShowEdit(false);
      fetchData();
    });
  }

  function delItem(id) {
    if (!window.confirm('Delete this item?')) return;
    fetch('http://localhost/inventory-api/managerInventory.php?id=' + id, {
      method: 'DELETE'
    }).then(() => fetchData());
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-gray-800">Inventory</h2>

        <div className="flex gap-2 mb-4">
          <input
            className="border px-2 py-1 rounded w-full"
            placeholder="Search..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <button
            onClick={fetchData}
            className="px-3 py-1 bg-blue-500 text-white rounded"
          >Search</button>
        </div>

        <button
          onClick={() => setShowAdd(true)}
          className="mb-4 bg-green-500 text-white px-3 py-1 rounded"
        >+ Add</button>

        <table className="w-full border text-sm">
          <thead>
            <tr>
              <th className="border p-1">#</th>
              <th className="border p-1">Product</th>
              <th className="border p-1">Qty</th>
              <th className="border p-1">Supplier</th>
              <th className="border p-1">Action</th>
            </tr>
          </thead>
          <tbody>
            {list.map((item, idx) => (
              <tr key={item.id}>
                <td className="border p-1 text-center">{idx + 1}</td>
                <td className="border p-1">{item.item_name}</td>
                <td className="border p-1 text-center">{item.quantity}</td>
                <td className="border p-1">{item.supplier}</td>
                <td className="border p-1 text-center">
                  <button
                    onClick={() => {
                      setEditForm({
                        id: item.id,
                        productName: item.item_name,
                        quantity: item.quantity,
                        supplier: item.supplier
                      });
                      setShowEdit(true);
                    }}
                    className="text-blue-600 text-xs mr-2"
                  >Edit</button>
                  <button
                    onClick={() => delItem(item.id)}
                    className="text-red-600 text-xs"
                  >Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {showAdd && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
            <div className="bg-white p-4 rounded w-72">
              <h3 className="text-md font-bold mb-2">Add Item</h3>
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Product"
                value={addForm.product}
                onChange={e => setAddForm({ ...addForm, product: e.target.value })}
              />
              <input
                className="border w-full mb-2 px-2 py-1"
                type="number"
                placeholder="Quantity"
                value={addForm.quantity}
                onChange={e => setAddForm({ ...addForm, quantity: parseInt(e.target.value) || 0 })}
              />
              <select
                className="border w-full mb-2 px-2 py-1"
                value={addForm.supplier}
                onChange={e => setAddForm({ ...addForm, supplier: e.target.value })}
              >
                <option value="">Select Supplier</option>
                {suppliers.map(s => (
                  <option key={s.id} value={s.name}>{s.name}</option>
                ))}
              </select>
              <div className="flex justify-end">
                <button onClick={() => setShowAdd(false)} className="px-2 py-1 mr-2 bg-gray-300 rounded">Cancel</button>
                <button onClick={addItem} className="px-2 py-1 bg-green-500 text-white rounded">Add</button>
              </div>
            </div>
          </div>
        )}

        {showEdit && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
            <div className="bg-white p-4 rounded w-72">
              <h3 className="text-md font-bold mb-2">Edit Item</h3>
              <input
                className="border w-full mb-2 px-2 py-1"
                placeholder="Product"
                value={editForm.productName}
                onChange={e => setEditForm({ ...editForm, productName: e.target.value })}
              />
              <input
                className="border w-full mb-2 px-2 py-1"
                type="number"
                placeholder="Quantity"
                value={editForm.quantity}
                onChange={e => setEditForm({ ...editForm, quantity: parseInt(e.target.value) || 0 })}
              />
              <select
                className="border w-full mb-2 px-2 py-1"
                value={editForm.supplier}
                onChange={e => setEditForm({ ...editForm, supplier: e.target.value })}
              >
                <option value="">Select Supplier</option>
                {suppliers.map(s => (
                  <option key={s.id} value={s.name}>{s.name}</option>
                ))}
              </select>
              <div className="flex justify-end">
                <button onClick={() => setShowEdit(false)} className="px-2 py-1 mr-2 bg-gray-300 rounded">Cancel</button>
                <button onClick={updateItem} className="px-2 py-1 bg-blue-500 text-white rounded">Update</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default InventoryPage;