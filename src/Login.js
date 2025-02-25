import React from "react";
import "./styles.css"; // 引入 CSS 文件

const LoginPage = () => {
  return (
    <div className="container">
      {/* 左侧 - 登录表单 */}
      <div className="left">
        {/* Logo */}
        <div className="logo">STOCKED</div>

        {/* 登录表单 */}
        <div className="login-box">
          <h2>Login</h2>
          <input type="email" placeholder="Email" required className="input-field" />
          <input type="password" placeholder="Password" required className="input-field" />

          {/* 选项 */}
          <div className="checkbox-container">
            <input type="checkbox" id="keep-logged" />
            <label htmlFor="keep-logged">Keep me logged in</label>
          </div>

          {/* 登录按钮 */}
          <button className="login-btn">Login</button>

          {/* 忘记密码 */}
          <p className="forgot-password">Forgot password?</p>
        </div>
      </div>

      {/* 右侧 - 背景图片 */}
      <div className="right"></div>
    </div>
  );
};

export default LoginPage;
