import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm, SubmitHandler } from 'react-hook-form';
import { login } from '../services/authService';
import { useAuth } from '../context/AuthContext';

// Images (make sure they are in the assets folder)
import adminIcon from "../assets/restaurant.jpg";
import managerIcon from "../assets/restaurant.jpg";
import staffIcon from "../assets/restaurant.jpg";
import supplierIcon from "../assets/restaurant.jpg";

type FormValues = {
  email: string;
  password: string;
};

const Login = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedRole, setSelectedRole] = useState<string | null>(null);
  
  const { setUser } = useAuth();
  const navigate = useNavigate();

  const handleRoleClick = (role: string) => {
    setSelectedRole(role);
  };

  const onSubmit: SubmitHandler<FormValues> = async (data) => {
    if (!selectedRole) {
      setError('Please select a role to continue.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await login({
        email: data.email,
        password: data.password
      });

      // Save token and user data
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));

      // Update auth context
      setUser(response.user);

      // Redirect based on role (override selectedRole if backend role differs)
      const roleToRedirect = response.user.role || selectedRole;

      const redirectMap: Record<string, string> = {
        admin: '/admin',
        manager: '/manager',
        staff: '/staff',
        supplier: '/supplier'
      };

      navigate(redirectMap[roleToRedirect] || '/');
    } catch (err) {
      setError('Invalid email or password. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.left}>
        <div style={styles.logo}>STOCKED</div>

        <div style={styles.iconContainer}>
          <RoleIcon role="admin" label="Admin" icon={adminIcon} onClick={handleRoleClick} selected={selectedRole === 'admin'} />
          <RoleIcon role="manager" label="Manager" icon={managerIcon} onClick={handleRoleClick} selected={selectedRole === 'manager'} />
          <RoleIcon role="staff" label="Staff" icon={staffIcon} onClick={handleRoleClick} selected={selectedRole === 'staff'} />
          <RoleIcon role="supplier" label="Supplier" icon={supplierIcon} onClick={handleRoleClick} selected={selectedRole === 'supplier'} />
        </div>

        <form onSubmit={handleSubmit(onSubmit)} style={styles.loginBox}>
          {error && (
            <div style={styles.errorMessage}>
              {error}
            </div>
          )}

          <input
            type="email"
            placeholder="Email"
            {...register('email', { required: 'Email is required' })}
            style={styles.inputField}
          />
          {errors.email && <p style={styles.fieldError}>{errors.email.message}</p>}

          <input
            type="password"
            placeholder="Password"
            {...register('password', { required: 'Password is required' })}
            style={styles.inputField}
          />
          {errors.password && <p style={styles.fieldError}>{errors.password.message}</p>}

          <div style={styles.checkboxContainer}>
            <input type="checkbox" id="keep-logged" style={styles.checkbox} />
            <label htmlFor="keep-logged" style={styles.checkboxLabel}>Keep me logged in</label>
          </div>

          <button
            type="submit"
            disabled={loading}
            style={loading ? { ...styles.loginButton, ...styles.loginButtonDisabled } : styles.loginButton}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>

          <p style={styles.forgotPassword}>Forgot password?</p>
        </form>
      </div>

      <div style={styles.right}></div>
    </div>
  );
};

type RoleIconProps = {
  role: string;
  label: string;
  icon: string;
  onClick: (role: string) => void;
  selected: boolean;
};

const RoleIcon = ({ role, label, icon, onClick, selected }: RoleIconProps) => (
  <div
    onClick={() => onClick(role)}
    style={{
      ...styles.icon,
      ...(selected ? styles.selectedIcon : {})
    }}
  >
    <img src={icon} alt={label} style={styles.iconImage} />
    <span style={styles.iconText}>{label}</span>
  </div>
);

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    display: 'flex',
    height: '100vh',
    fontFamily: "'Arial', sans-serif"
  },
  left: {
    flex: 1,
    padding: '40px',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#f0f2f5',
    position: 'relative'
  },
  logo: {
    fontSize: '32px',
    fontWeight: 'bold',
    marginBottom: '40px',
    color: '#333'
  },
  iconContainer: {
    display: 'flex',
    justifyContent: 'space-around',
    marginBottom: '40px',
    flexWrap: 'wrap'
  },
  icon: {
    cursor: 'pointer',
    textAlign: 'center',
    marginBottom: '20px',
    borderWidth: '2px',
    borderStyle: 'solid',
    borderColor: 'transparent', // moved from shorthand
    borderRadius: '10px',
    padding: '10px',
    transition: 'border-color 0.3s ease'
  },
  selectedIcon: {
    borderColor: '#007bff'
  },
  iconImage: {
    width: '80px',
    height: '80px',
    borderRadius: '50%',
    objectFit: 'cover'
  },
  iconText: {
    display: 'block',
    marginTop: '10px',
    fontSize: '14px',
    color: '#555'
  },
  loginBox: {
    backgroundColor: '#fff',
    padding: '30px',
    borderRadius: '10px',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '400px'
  },
  inputField: {
    width: '100%',
    padding: '12px',
    marginBottom: '15px',
    borderRadius: '8px',
    border: '1px solid #ddd',
    boxSizing: 'border-box'
  },
  checkboxContainer: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '15px'
  },
  checkbox: {
    marginRight: '8px'
  },
  checkboxLabel: {
    fontSize: '14px',
    color: '#555'
  },
  loginButton: {
    width: '100%',
    padding: '12px',
    fontSize: '16px',
    color: '#fff',
    backgroundColor: '#007bff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.3s ease'
  },
  loginButtonDisabled: {
    backgroundColor: '#7ab5ff',
    cursor: 'not-allowed'
  },
  forgotPassword: {
    marginTop: '15px',
    fontSize: '14px',
    color: '#007bff',
    cursor: 'pointer',
    textAlign: 'center'
  },
  errorMessage: {
    backgroundColor: '#ffeeee',
    color: '#e53e3e',
    padding: '10px',
    borderRadius: '8px',
    marginBottom: '15px',
    fontSize: '14px'
  },
  fieldError: {
    color: '#e53e3e',
    fontSize: '12px',
    marginTop: '-10px',
    marginBottom: '10px'
  },
  right: {
    flex: 1,
    backgroundImage: 'url(../assets/restaurant.jpg)',
    backgroundSize: 'cover',
    backgroundPosition: 'center'
  }
};

export default Login;