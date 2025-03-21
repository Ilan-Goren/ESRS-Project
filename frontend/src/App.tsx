import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Import pages
import Login from './pages/Login';
import AdminDashboard from './pages/admin/Dashboard';
import ManagerDashboard from './pages/manager/Dashboard';
import StaffDashboard from './pages/staff/Dashboard';
import SupplierDashboard from './pages/supplier/Dashboard';
import NotFound from './pages/NotFound';
import InventoryPage from './pages/admin/Inventory';
import ProtectedRoute from './components/common/ProtectedRoute'

// Create a client
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} /> {/* Updated formatting */}
            
            <Route 
              path="/admin/*" 
              element={
                <ProtectedRoute roles={['admin']}>
                  <AdminDashboard />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/manager/*" 
              element={
                <ProtectedRoute roles={['manager']}>
                  <ManagerDashboard />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/staff/*" 
              element={
                <ProtectedRoute roles={['staff']}>
                  <StaffDashboard />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/supplier/*" 
              element={
                <ProtectedRoute roles={['supplier']}>
                  <SupplierDashboard />
                </ProtectedRoute>
              } 
            />

            <Route 
              path="/admin/inventory" 
              element={
                <ProtectedRoute roles={['admin']}>
                  <InventoryPage />
                </ProtectedRoute>
              } 
            />
            
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;