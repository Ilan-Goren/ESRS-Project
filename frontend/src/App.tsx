import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Import pages
import Login from './pages/Login';
import AdminDashboard from './pages/admin/Dashboard';
import InventoryPage from './pages/admin/Inventory';
import ManagerUserPage from './pages/admin/ManagerUser';
import ReportPage from './pages/admin/Report';
import SettingPage from './pages/admin/Setting';
import ManagerDashboard from './pages/manager/Dashboard';
import InventoryManagement from './pages/manager/Inventory';
import ManageSuppliers from './pages/manager/Suppliers';
import StaffDashboard from './pages/staff/Dashboard';
import InventoryItem from './pages/staff/Inventory';
import PlaceOrder from './pages/staff/Orders';
import SupplierDashboard from './pages/supplier/Dashboard';
import SupplierOrders from './pages/supplier/Orders';
import SupplierDeliveries from './pages/supplier/Deliveries';
import NotFound from './pages/NotFound';


// Create a client
const queryClient = new QueryClient();

// Protected route component
const ProtectedRoute = ({ children, roles }: { children: JSX.Element, roles?: string[] }) => {
  const { isAuthenticated, user, loading } = useAuth();
  
  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (roles && user && !roles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }
  
  return children;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            
            <Route 
              path="/admin/*" 
              element={
                <ProtectedRoute roles={['admin']}>
                  <AdminDashboard />
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

            <Route 
              path="/admin/ManagerUser" 
              element={
                <ProtectedRoute roles={['admin']}>
                  <ManagerUserPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/admin/reports" 
              element={
                <ProtectedRoute roles={['admin']}>
                  <ReportPage />
                </ProtectedRoute>
              } 
            />

            <Route 
              path="/admin/settings" 
              element={
                <ProtectedRoute roles={['admin']}>
                  <SettingPage />
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
              path="/manager/inventory" 
              element={
                <ProtectedRoute roles={['manager']}>
                  <InventoryManagement />
                </ProtectedRoute>
              } 
            />

            <Route 
              path="/manager/suppliers" 
              element={
                <ProtectedRoute roles={['manager']}>
                  <ManageSuppliers />
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
              path="/staff/inventory" 
              element={
                <ProtectedRoute roles={['staff']}>
                  <InventoryItem />
                </ProtectedRoute>
              } 
            />

            <Route 
              path="/staff/orders" 
              element={
                <ProtectedRoute roles={['staff']}>
                  <PlaceOrder />
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
              path="/supplier/orders" 
              element={
                <ProtectedRoute roles={['supplier']}>
                  <SupplierOrders />
                </ProtectedRoute>
              } 
            />

            <Route 
              path="/supplier/deliveries" 
              element={
                <ProtectedRoute roles={['supplier']}>
                  <SupplierDeliveries />
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