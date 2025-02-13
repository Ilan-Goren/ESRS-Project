import { useState } from "react";
import restaurant from "./assets/restaurant.jpg";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        alert(`login information：\nusername: ${username}\npassword: ${password}`);
    };

    return (
        <div style={{...styles.container, backgroundImage: `url(${restaurant})` }}>
            <div style={styles.card}>
                <h2 style={styles.title}>Restaurant Warehouse Management System</h2>
                <form onSubmit={handleSubmit} style={styles.form}>
                    <div style={styles.formGroup}>
                        <label style={styles.label}>username:</label>
                        <input
                            type="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            style={styles.input}
                            placeholder="Please enter your username"
                        />
                    </div>
                    <div style={styles.formGroup}>
                        <label style={styles.label}>password:</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            style={styles.input}
                            placeholder="Please enter the password"
                        />
                    </div>
                    <button type="submit" style={styles.button}>login</button>
                </form>
            </div>
        </div>
    );
}

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
    inputFocus: {
        borderColor: "#007bff",
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
    buttonHover: {
        backgroundColor: "#0056b3",
    },
    link: {
        color: "#007bff",
        textDecoration: "none",
        fontWeight: "500",
    },
};

export default Login;