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
    console.log(`${import.meta.env.VITE_API_URL}`)
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/register`, {
        method: "POST",
        // headers: { "Content-Type": "application/json" },
        body: formData,
      });


      if (response.ok) {
        navigate("/login");
      } else if (response.status === 409) {
        setError("That username is already taken."); // Use the same state setter!
      } else {
        setError("Something went wrong.");
      }
    } catch (err) {
      // This only runs if the API is offline/unreachable
      setError("Could not register user due to a network error.");
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
            {error && <p style={styles.error}>{error}</p>}
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

const styles = {
  title: {
    marginBottom: "20px",
    textAlign: "center",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  input: {
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    fontSize: "14px",
  },
  button: {
    padding: "10px",
    borderRadius: "6px",
    border: "none",
    background: "#4f46e5",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
  },
  error: {
    marginTop: "10px",
    color: "red",
    textAlign: "center",
  },
};
export default Register;
