import api from './api';

export interface Supplier {
  id: number;
  name: string;
  contact_info: string;
  email: string;
  phone: string;
  created_at: string;
}

export const getSuppliers = async (): Promise<Supplier[]> => {
  const response = await api.get('/suppliers.php');
  return response.data;
};

export const getSupplier = async (id: number): Promise<Supplier> => {
  const response = await api.get(`/suppliers.php?id=${id}`);
  return response.data;
};

export const createSupplier = async (supplier: Omit<Supplier, 'id' | 'created_at'>): Promise<{ id: number }> => {
  const response = await api.post('/suppliers.php', supplier);
  return response.data;
};

export const updateSupplier = async (id: number, supplier: Partial<Supplier>): Promise<{ success: boolean }> => {
  const response = await api.put(`/suppliers.php?id=${id}`, supplier);
  return response.data;
};

export const deleteSupplier = async (id: number): Promise<{ success: boolean }> => {
  const response = await api.delete(`/suppliers.php?id=${id}`);
  return response.data;
};