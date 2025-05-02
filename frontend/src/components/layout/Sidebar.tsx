import { useLocation, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

interface NavItem {
  path: string;
  label: string;
  roles: string[];
}

const Sidebar = () => {
  const { user } = useAuth();
  const location = useLocation();
  
  const navItems: NavItem[] = [
    // Admin routes
    { path: '/admin', label: 'Dashboard', roles: ['admin'] },
    { path: '/admin/inventory', label: 'Inventory', roles: ['admin'] },
    { path: '/admin/ManagerUser', label: 'Manage Users', roles: ['admin'] },
    { path: '/admin/reports', label: 'Reports & Analytics', roles: ['admin'] },
    { path: '/admin/settings', label: 'System Settings', roles: ['admin'] },
    
    // Manager routes
    { path: '/manager', label: 'Dashboard', roles: ['manager'] },
    { path: '/manager/inventory', label: 'Inventory Management', roles: ['manager'] },
    { path: '/manager/suppliers', label: 'Manage Suppliers', roles: ['manager'] },
    
    // Staff routes
    { path: '/staff', label: 'Dashboard', roles: ['staff'] },
    { path: '/staff/Inventory', label: 'View Stock Levels', roles: ['staff'] },
    { path: '/staff/orders', label: 'Place New Order', roles: ['staff'] },
    
    // Supplier routes
    { path: '/supplier', label: 'Dashboard', roles: ['supplier'] },
    { path: '/supplier/orders', label: 'View Orders', roles: ['supplier'] },
    { path: '/supplier/deliveries', label: 'Update Deliveries', roles: ['supplier'] }
  ];

  const filteredNavItems = navItems.filter(item => 
    item.roles.includes(user?.role || '')
  );

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <div className="hidden md:flex md:flex-shrink-0">
      <div className="flex flex-col w-64">
        <div className="flex flex-col h-0 flex-1 bg-gray-800">
          <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <nav className="mt-5 px-2 space-y-1">
              {filteredNavItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                    isActive(item.path)
                      ? 'bg-gray-900 text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;