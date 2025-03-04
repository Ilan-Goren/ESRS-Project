import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { login } from '../services/authService';
import { useAuth } from '../context/AuthContext';
import restaurant from "../assets/restaurant.jpg"; // Make sure this image is in your assets folder

const Login = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const { setUser } = useAuth();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await login({
        email: data.email,
        password: data.password
      });
      
      // Save token and user
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      
      // Update auth context
      setUser(response.user);
      
      // Redirect based on role
      const redirectMap = {
        admin: '/admin',
        manager: '/manager',
        staff: '/staff',
        supplier: '/supplier'
      };
      
      navigate(redirectMap[response.user.role] || '/');
    } catch (err) {
      setError('Invalid email or password. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{...styles.container, backgroundImage: `url(${restaurant})` }}>
      <div style={styles.card}>
        <h2 style={styles.title}>Restaurant Inventory Management System</h2>
        {error && (
          <div style={styles.errorMessage}>
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit(onSubmit)} style={styles.form}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Email:</label>
            <input
              type="email"
              style={styles.input}
              placeholder="Please enter your email"
              {...register('email', { required: 'Email is required' })}
            />
            {errors.email && (
              <p style={styles.fieldError}>{errors.email.message}</p>
            )}
          </div>
          <div style={styles.formGroup}>
            <label style={styles.label}>Password:</label>
            <input
              type="password"
              style={styles.input}
              placeholder="Please enter the password"
              {...register('password', { required: 'Password is required' })}
            />
            {errors.password && (
              <p style={styles.fieldError}>{errors.password.message}</p>
            )}
          </div>
          <div style={styles.checkboxContainer}>
            <input type="checkbox" id="keep-logged" style={styles.checkbox} />
            <label htmlFor="keep-logged" style={styles.checkboxLabel}>Keep me logged in</label>
          </div>
          <button 
            type="submit" 
            style={loading ? {...styles.button, ...styles.buttonDisabled} : styles.button}
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
          <p style={styles.forgotPassword}>Forgot password?</p>
        </form>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    backgroundColor: "#f0f2f5",
    backgroundSize: "cover", 
    backgroundPosition: "center", 
    fontFamily: "'Arial', sans-serif",
  },
  card: {
    backgroundColor: "#fff",
    borderRadius: "12px",
    boxShadow: "0 4px 20px rgba(0, 0, 0, 0.1)",
    padding: "40px",
    width: "350px",
    textAlign: "center",
  },
  title: {
    fontSize: "24px",
    fontWeight: "600",
    marginBottom: "20px",
    color: "#333",
  },
  form: {
    display: "flex",
    flexDirection: "column",
  },
  formGroup: {
    marginBottom: "20px",
    textAlign: "left",
  },
  label: {
    display: "block",
    marginBottom: "8px",
    fontSize: "14px",
    color: "#555",
  },
  input: {
    width: "100%",
    padding: "12px",
    fontSize: "14px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    boxSizing: "border-box",
    outline: "none",
    transition: "border-color 0.3s ease",
  },
  checkboxContainer: {
    display: "flex",
    alignItems: "center",
    marginBottom: "15px",
    textAlign: "left",
  },
  checkbox: {
    marginRight: "8px",
  },
  checkboxLabel: {
    fontSize: "14px",
    color: "#555",
  },
  button: {
    width: "100%",
    padding: "12px",
    fontSize: "16px",
    color: "#fff",
    backgroundColor: "#007bff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "background-color 0.3s ease",
  },
  buttonDisabled: {
    backgroundColor: "#7ab5ff",
    cursor: "not-allowed",
  },
  forgotPassword: {
    marginTop: "15px",
    fontSize: "14px",
    color: "#007bff",
    cursor: "pointer",
  },
  errorMessage: {
    backgroundColor: "#ffeeee",
    color: "#e53e3e",
    padding: "10px",
    borderRadius: "8px",
    marginBottom: "15px",
    fontSize: "14px",
  },
  fieldError: {
    color: "#e53e3e",
    fontSize: "12px",
    marginTop: "5px",
  },
};

export default Login;