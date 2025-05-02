import api from './api';

export interface InventoryItem {
  id: number;
  item_name: string;
  category: string;
  quantity: number;
  reorder_level: number;
  expiry_date: string;
  supplier_id: number;
  supplier_name?: string;
  last_updated: string;
}

export const getInventory = async (): Promise<InventoryItem[]> => {
  const response = await api.get('/inventory.php');
  return response.data;
};

export const getInventoryItem = async (id: number): Promise<InventoryItem> => {
  const response = await api.get(`/inventory.php?id=${id}`);
  return response.data;
};

export const createInventoryItem = async (item: Omit<InventoryItem, 'id' | 'last_updated'>): Promise<{ id: number }> => {
  const response = await api.post('/inventory.php', item);
  return response.data;
};

export const updateInventoryItem = async (id: number, item: Partial<InventoryItem>): Promise<{ success: boolean }> => {
  const response = await api.put(`/inventory.php?id=${id}`, item);
  return response.data;
};

export const deleteInventoryItem = async (id: number): Promise<{ success: boolean }> => {
  const response = await api.delete(`/inventory.php?id=${id}`);
  return response.data;
};