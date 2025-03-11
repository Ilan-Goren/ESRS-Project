import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { FiSearch, FiFilter, FiX } from 'react-icons/fi';

interface SearchFormData {
  searchTerm: string;
  category: string;
  supplier: string;
  minStock: number | '';
  maxStock: number | '';
}

interface AdvancedSearchProps {
  categories: { id: string; name: string }[];
  suppliers: { id: number; name: string }[];
  onSearch: (filters: Partial<SearchFormData>) => void;
}

const AdvancedSearch: React.FC<AdvancedSearchProps> = ({ 
  categories = [], 
  suppliers = [],
  onSearch 
}) => {
  const [isAdvancedOpen, setIsAdvancedOpen] = useState(false);
  const { register, handleSubmit, reset, watch } = useForm<SearchFormData>({
    defaultValues: {
      searchTerm: '',
      category: '',
      supplier: '',
      minStock: '',
      maxStock: ''
    }
  });

  const searchTerm = watch('searchTerm');

  const toggleAdvanced = () => {
    setIsAdvancedOpen(!isAdvancedOpen);
  };

  const resetFilters = () => {
    reset();
    onSearch({});
  };

  const onSubmit = (data: SearchFormData) => {
    console.log('Advanced filters applied:', data);
    const filters: Partial<SearchFormData> = {};
    
    if (data.searchTerm) filters.searchTerm = data.searchTerm;
    if (data.category) filters.category = data.category;
    if (data.supplier) filters.supplier = data.supplier;
    if (data.minStock !== '') filters.minStock = data.minStock;
    if (data.maxStock !== '') filters.maxStock = data.maxStock;
    
    onSearch(filters);
  };

  const handleQuickSearch = () => {
    if (searchTerm) {
        console.log('Quick search triggered');
        onSearch({ searchTerm });
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Quick Search Bar */}
        <div className="flex gap-2 mb-3">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Search by name or SKU..."
              className="form-input pl-10 pr-4 py-2"
              {...register('searchTerm')}
            />
            <FiSearch className="absolute left-3 top-3 text-gray-400" />
          </div>
          <button
            type="button"
            onClick={handleQuickSearch}
            className="bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700"
          >
            Search
          </button>
          <button
            type="button"
            onClick={toggleAdvanced}
            className={`flex items-center justify-center gap-1 px-4 py-2 rounded ${
              isAdvancedOpen 
                ? 'bg-gray-700 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            <FiFilter />
            {isAdvancedOpen ? 'Hide Filters' : 'Filters'}
          </button>
        </div>

        {/* Advanced Filters */}
        {isAdvancedOpen && (
          <div className="border-t pt-3 mt-2 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="form-label">Category</label>
              <select {...register('category')} className="form-input">
                <option value="">All Categories</option>
                {categories.map(category => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="form-label">Supplier</label>
              <select {...register('supplier')} className="form-input">
                <option value="">All Suppliers</option>
                {suppliers.map(supplier => (
                  <option key={supplier.id} value={supplier.id}>
                    {supplier.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="form-label">Min Stock</label>
                <input
                  type="number"
                  className="form-input"
                  min="0"
                  {...register('minStock', { 
                    setValueAs: value => value === '' ? '' : parseInt(value) 
                  })}
                />
              </div>
              <div>
                <label className="form-label">Max Stock</label>
                <input
                  type="number"
                  className="form-input"
                  min="0"
                  {...register('maxStock', { 
                    setValueAs: value => value === '' ? '' : parseInt(value) 
                  })}
                />
              </div>
            </div>

            <div className="md:col-span-3 flex justify-end gap-2 mt-2">
              <button
                type="button"
                onClick={resetFilters}
                className="flex items-center px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-100"
              >
                <FiX className="mr-1" /> Clear
              </button>
              <button
                type="submit"
                className="flex items-center px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
              >
                <FiSearch className="mr-1" /> Apply Filters
              </button>
            </div>
          </div>
        )}
      </form>
    </div>
  );
};

export default AdvancedSearch;