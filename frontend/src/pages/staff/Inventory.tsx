import React, { useState, useEffect } from 'react';
import Layout from '../../components/layout/Layout';

const InventoryView = () => {
  const [list, setList] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(function() {
    load();
  }, []);

  function load() {
    fetch('http://localhost/inventory-api/managerInventory.php?search=' + encodeURIComponent(search))
      .then(function(res) { return res.json(); })
      .then(function(data) { setList(data); })
      .catch(function() { alert('Failed to load'); });
  }

  function handleSearch(e) {
    e.preventDefault();
    load();
  }

  return (
    <Layout>
      <div className="p-5">
        <h2 className="text-lg font-bold mb-4 text-gray-800">Inventory</h2>

        <form onSubmit={handleSearch} className="mb-4 flex gap-2">
          <input
            type="text"
            placeholder="Search..."
            className="border px-2 py-1 rounded w-full"
            value={search}
            onChange={function(e) { setSearch(e.target.value); }}
          />
          <button type="submit" className="bg-blue-500 text-white px-3 py-1 rounded">Search</button>
        </form>

        <table className="w-full border text-sm">
          <thead>
            <tr>
              <th className="border p-1">#</th>
              <th className="border p-1">Product</th>
              <th className="border p-1">Qty</th>
              <th className="border p-1">Supplier</th>
            </tr>
          </thead>
          <tbody>
            {list.map(function(item, i) {
              return (
                <tr key={item.id}>
                  <td className="border p-1 text-center">{i + 1}</td>
                  <td className="border p-1">{item.productName}</td>
                  <td className="border p-1 text-center">{item.quantity}</td>
                  <td className="border p-1">{item.supplier}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Layout>
  );
};

export default InventoryView;