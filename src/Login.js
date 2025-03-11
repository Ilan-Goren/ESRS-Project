import React from "react";
import "./styles.css"; 
import adminIcon from "./assets/admin.png"; 
import managerIcon from "./assets/manager.png"; 
import staffIcon from "./assets/staff.png"; 
import supplierIcon from "./assets/supplier.png"; 

const LoginPage = () => {
    const handleIconClick = (role) => {
        let url = "";
        switch (role) {
          case "admin":
            url = "/admin-login"; 
            break;
          case "manager":
            url = "/manager-login"; 
            break;
          case "staff":
            url = "/staff-login"; 
            break;
          case "supplier":
            url = "/supplier-login"; 
            break;
          default:
            break;
        }
        window.location.href = url; 
    };

    return (
        <div className="container">
          {/* left - login form */}
          <div className="left">
            {/* logo */}
            <div className="logo">STOCKED</div>
    
            {/* icon */}
            <div className="icon-container">
              <div className="icon" onClick={() => handleIconClick("admin")}>
                <img src={adminIcon} className="icon-image" />
                <span className="icon-text">Admin</span>
              </div>
              <div className="icon" onClick={() => handleIconClick("manager")}>
                <img src={managerIcon} className="icon-image" />
                <span className="icon-text">Manager</span>
              </div>
              <div className="icon" onClick={() => handleIconClick("staff")}>
                <img src={staffIcon} className="icon-image" />
                <span className="icon-text">Staff</span>
              </div>
              <div className="icon" onClick={() => handleIconClick("supplier")}>
                <img src={supplierIcon} className="icon-image" />
                <span className="icon-text">Supplier</span>
              </div>
            </div>

            {/* login form */}
            <div className="login-box">
              <input type="email" placeholder="Email" required className="input-field" />
              <input type="password" placeholder="Password" required className="input-field" />
    
              {/* checkbox */}
              <div className="checkbox-container">
                <input type="checkbox" id="keep-logged" />
                <label>Keep me logged in</label>
              </div>
    
              {/* login button */}
              <button className="login-btn">Login</button>
    
              {/* forgotten password*/}
              <p className="forgot-password">Forgot password?</p>
            </div>
          </div>
    
          {/* Right - Background Image */}
          <div className="right"></div>
        </div>
      );
    };

export default LoginPage;
