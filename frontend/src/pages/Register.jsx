import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Register.css";
import "./Login.css";

function Register() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");

  const [error, setError] = useState("");

  async function handleRegister(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("password", password);

    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        // headers: { "Content-Type": "application/json" },
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Register failed");
      }

      // After successful register → login
      navigate("/login");
    } catch (err) {
      setError("Could not register user");
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div
        style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh", // full viewport height
            backgroundColor: "#121212", // dark background
        }}
        >
          <div
            style={{
            backgroundColor: "#1e1e1e",
            padding: "40px",
            borderRadius: "10px",
            boxShadow: "0 0 10px rgba(0,0,0,0.5)",
            minWidth: "300px",
            color: "white",
            }}
          >
            <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
            Register
            </h2>

            <form onSubmit={handleRegister}>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={inputStyle}
            />
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={inputStyle}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={inputStyle}
            />
            <button type="submit" style={buttonStyle}>
                Register
            </button>
            </form>
          </div>
        </div>
      </div>
    </div>

  );
}

const inputStyle = {
    display: "block",
    width: "100%",
    padding: "10px",
    marginBottom: "15px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    backgroundColor: "#2c2c2c",
    color: "white",
  };
  
  const buttonStyle = {
    display: "block",        // ensures it behaves like the inputs
    width: "107%",           // same as inputs
    padding: "12px",         // slightly more for a bigger look
    backgroundColor: "#4caf50",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",        // makes it more prominent
    marginTop: "10px",       // spacing from last input
  };
export default Register;
