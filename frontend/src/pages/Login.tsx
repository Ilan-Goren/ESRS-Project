import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { login } from '../services/authService';
import { useAuth } from '../context/AuthContext';

// Import images
import adminIcon from "../assets/admin.png";
import managerIcon from "../assets/manager.png";
import staffIcon from "../assets/staff.png";
import supplierIcon from "../assets/supplier.png";
import restaurantBg from "../assets/restaurant.jpg";

interface LoginFormData {
  email: string;
  password: string;
}

const MergedLogin = () => {
  const { register, handleSubmit, formState: { errors }, reset } = useForm<LoginFormData>();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedRole, setSelectedRole] = useState<string | null>(null);
  const { setUser } = useAuth();
  const navigate = useNavigate();

  const handleIconClick = (role: string) => {
    setSelectedRole(role);
    
    // Reset form fields when changing roles
    reset();
    
    // Clear any existing error
    setError(null);
  };

  const onSubmit = async (data: LoginFormData) => {
    if (!selectedRole) {
      setError("Please select a role first");
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      // Pass both email/password AND the selected role to the login function
      const loginData = {
        email: data.email,
        password: data.password,
        role: selectedRole // Include the selected role
      };
      
      console.log(`Attempting login with email: ${data.email}, role: ${selectedRole}`);
      
      // Call the login function
      const user = await login(loginData);
      
      console.log("Login response:", user);
      
      // Get the role from localStorage after login
      const userRole = localStorage.getItem('role');
      
      if (!userRole) {
        setError('Login successful but role information is missing');
        setLoading(false);
        return;
      }
      
      console.log(`User role from backend: ${userRole}, selected role: ${selectedRole}`);
      
      // Use case-insensitive comparison for roles
      if (userRole.toLowerCase() !== selectedRole.toLowerCase()) {
        // Allow admin to access any role
        if (userRole.toLowerCase() === 'admin') {
          console.log('Admin accessing another role - allowed');
        }
        // For non-admins, enforce role matching
        else {
          setError(`You don't have ${selectedRole} privileges. Please select your actual role: ${userRole}`);
          setLoading(false);
          return;
        }
      }
      
      // Update auth context
      setUser(user);
      
      // Determine which dashboard to redirect to
      const effectiveRole = userRole.toLowerCase() === 'admin' && selectedRole.toLowerCase() !== 'admin'
        ? selectedRole.toLowerCase()  // Admin acting as another role
        : userRole.toLowerCase();     // Normal user with their own role
      
      const redirectMap: Record<string, string> = {
        admin: '/admin',
        manager: '/manager',
        staff: '/staff',
        supplier: '/supplier'
      };
      
      navigate(redirectMap[effectiveRole] || '/');
    } catch (err) {
      setError('Invalid email or password. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* Left - Login form */}
      <div style={styles.leftContainer}>
        {/* Logo */}
        <div style={styles.logo}>STOCKED</div>

        {/* Icons */}
        <div style={styles.iconContainer}>
          <div 
            style={selectedRole === "admin" ? {...styles.icon, ...styles.selectedIcon} : styles.icon} 
            onClick={() => handleIconClick("admin")}
          >
            <img src={adminIcon} alt="Admin" style={styles.iconImage} />
            <span style={styles.iconText}>Admin</span>
          </div>
          <div 
            style={selectedRole === "manager" ? {...styles.icon, ...styles.selectedIcon} : styles.icon} 
            onClick={() => handleIconClick("manager")}
          >
            <img src={managerIcon} alt="Manager" style={styles.iconImage} />
            <span style={styles.iconText}>Manager</span>
          </div>
          <div 
            style={selectedRole === "staff" ? {...styles.icon, ...styles.selectedIcon} : styles.icon} 
            onClick={() => handleIconClick("staff")}
          >
            <img src={staffIcon} alt="Staff" style={styles.iconImage} />
            <span style={styles.iconText}>Staff</span>
          </div>
          <div 
            style={selectedRole === "supplier" ? {...styles.icon, ...styles.selectedIcon} : styles.icon} 
            onClick={() => handleIconClick("supplier")}
          >
            <img src={supplierIcon} alt="Supplier" style={styles.iconImage} />
            <span style={styles.iconText}>Supplier</span>
          </div>
        </div>

        {/* Login form */}
        <div style={styles.loginBox}>
          {error && (
            <div style={styles.errorMessage}>
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit(onSubmit)}>
            <div style={styles.inputWrapper}>
              <input
                type="email"
                style={styles.inputField}
                placeholder="Email"
                {...register('email', { 
                  required: 'Email is required'
                })}
              />
            </div>
            {errors.email && (
              <p style={styles.fieldError}>{errors.email.message}</p>
            )}
            
            <div style={styles.inputWrapper}>
              <input
                type="password"
                style={styles.inputField}
                placeholder="Password"
                {...register('password', { required: 'Password is required' })}
              />
            </div>
            {errors.password && (
              <p style={styles.fieldError}>{errors.password.message}</p>
            )}

            {/* Checkbox */}
            <div style={styles.checkboxContainer}>
              <input type="checkbox" id="keep-logged" style={styles.checkbox} />
              <label htmlFor="keep-logged" style={styles.checkboxLabel}>Keep me logged in</label>
            </div>

            {/* Login button */}
            <button 
              type="submit" 
              style={{
                ...styles.loginBtn,
                ...(loading ? styles.buttonDisabled : {}),
                ...(selectedRole ? {} : styles.buttonDisabled)
              }}
              disabled={loading || !selectedRole}
            >
              {loading ? 'Logging in...' : selectedRole ? `Login as ${selectedRole}` : 'Select a role'}
            </button>

            {/* Forgotten password*/}
            <p style={styles.forgotPassword}>Forgot password?</p>
          </form>
        </div>
      </div>

      {/* Right - Background Image */}
      <div style={styles.rightContainer}></div>
    </div>
  );
};

// Styles - unchanged
const styles = {
  // ... (styles remain the same)
  inputWrapper: {
    position: "relative" as const,
    width: "100%",
  },
  container: {
    display: "flex",
    width: "100%",
    height: "100vh",
    fontFamily: "'Arial', sans-serif",
  },
  leftContainer: {
    flex: "0 0 50%",
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center",
    justifyContent: "center",
    padding: "40px",
    backgroundColor: "#fff",
  },
  rightContainer: {
    flex: "0 0 50%",
    backgroundImage: `url(${restaurantBg})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
  },
  logo: {
    fontSize: "28px",
    fontWeight: "700" as const,
    marginBottom: "30px",
    color: "#000",
    padding: "10px 20px",
    backgroundColor: "#000",
    color: "#fff",
    borderRadius: "4px",
  },
  iconContainer: {
    display: "flex",
    justifyContent: "space-between",
    gap: "15px",
    marginBottom: "40px",
    width: "100%",
    maxWidth: "400px",
  },
  icon: {
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center",
    cursor: "pointer",
    padding: "5px",
    transition: "all 0.3s ease",
  },
  selectedIcon: {
    borderBottom: "2px solid #000",
  },
  iconImage: {
    width: "50px",
    height: "50px",
    marginBottom: "5px",
  },
  iconText: {
    fontSize: "14px",
    color: "#333",
  },
  loginBox: {
    width: "100%",
    maxWidth: "400px",
  },
  inputField: {
    width: "100%",
    padding: "10px 0",
    margin: "10px 0",
    fontSize: "14px",
    border: "none",
    borderBottom: "1px solid #ddd",
    boxSizing: "border-box" as const,
    outline: "none",
    transition: "border-color 0.3s ease",
  },
  checkboxContainer: {
    display: "flex",
    alignItems: "center",
    marginTop: "15px",
    marginBottom: "20px",
  },
  checkbox: {
    marginRight: "8px",
  },
  checkboxLabel: {
    fontSize: "14px",
    color: "#555",
  },
  loginBtn: {
    width: "100%",
    padding: "12px",
    fontSize: "16px",
    color: "#fff",
    backgroundColor: "#000",
    border: "none",
    cursor: "pointer",
    transition: "background-color 0.3s ease",
  },
  buttonDisabled: {
    backgroundColor: "#999",
    cursor: "not-allowed",
  },
  forgotPassword: {
    marginTop: "15px",
    fontSize: "14px",
    color: "#555",
    cursor: "pointer",
    textAlign: "center" as const,
  },
  errorMessage: {
    color: "#e53e3e",
    backgroundColor: "#fee",
    padding: "10px",
    borderRadius: "4px",
    marginBottom: "15px",
    fontSize: "14px",
    textAlign: "center" as const,
  },
  fieldError: {
    color: "#e53e3e",
    fontSize: "12px",
    marginTop: "5px",
    marginBottom: "10px",
  },
};

export default MergedLogin;