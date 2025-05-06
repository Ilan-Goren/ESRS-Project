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
  sku?: string;
  unit_price?: number;
}

export interface InventorySearchFilters {
  searchTerm?: string;
  category?: string;
  supplier?: string | number;
  minStock?: string | number;
  maxStock?: string | number;
  lowStock?: boolean;
}

// Get all inventory items with optional filtering
export const getInventory = async (filters?: InventorySearchFilters): Promise<InventoryItem[]> => {
  try {
    // Build query params if filters provided
    let queryString = '';
    if (filters) {
      const queryParams = new URLSearchParams();
      
      if (filters.searchTerm) queryParams.append('search', filters.searchTerm);
      if (filters.category) queryParams.append('category', filters.category.toString());
      if (filters.supplier) queryParams.append('supplier', filters.supplier.toString());
      if (filters.minStock !== undefined && filters.minStock !== '') 
        queryParams.append('min_stock', filters.minStock.toString());
      if (filters.maxStock !== undefined && filters.maxStock !== '') 
        queryParams.append('max_stock', filters.maxStock.toString());
      if (filters.lowStock) queryParams.append('low_stock', 'true');
      
      queryString = queryParams.toString();
      if (queryString) queryString = `?${queryString}`;
    }
    
    // Log the request for debugging
    console.log('Fetching inventory with params:', queryString);
    console.log('Auth status:', {
      token: !!localStorage.getItem('access_token'),
      tokenStart: localStorage.getItem('access_token')?.substring(0, 10) + '...'
    });
    
    // Make the API request
    const response = await api.get(`/inventory/${queryString}`);
    console.log('Inventory response:', response.status);
    return response.data;
  } catch (error) {
    console.error('Error fetching inventory:', error);
    throw error;
  }
};

export const getInventoryItem = async (id: number): Promise<InventoryItem> => {
  try {
    const response = await api.get(`/inventory/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching inventory item ${id}:`, error);
    throw error;
  }
};

export const createInventoryItem = async (item: Omit<InventoryItem, 'id' | 'last_updated'>): Promise<{ id: number }> => {
  try {
    const response = await api.post('/inventory/', item);
    return response.data;
  } catch (error) {
    console.error('Error creating inventory item:', error);
    throw error;
  }
};

export const updateInventoryItem = async (id: number, item: Partial<InventoryItem>): Promise<{ success: boolean }> => {
  try {
    const response = await api.put(`/inventory/${id}/`, item);
    return response.data;
  } catch (error) {
    console.error(`Error updating inventory item ${id}:`, error);
    throw error;
  }
};

export const deleteInventoryItem = async (id: number): Promise<{ success: boolean }> => {
  try {
    const response = await api.delete(`/inventory/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting inventory item ${id}:`, error);
    throw error;
  }
};

export default {
  getInventory,
  getInventoryItem,
  createInventoryItem,
  updateInventoryItem,
  deleteInventoryItem
};