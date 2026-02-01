import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";




function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    

    try {
      const response = await fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username,
          password,
        }),
      });

      if (!response.ok) throw new Error();

      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      navigate("/library");

      // alert("Login successful!");
    } catch {
      setError("Invalid username or password");
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h2 style={styles.title}>Login</h2>

        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            style={styles.input}
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            style={styles.input}
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button style={styles.button} type="submit">
            Sign In
          </button>
        </form>
        <button
          className="link-button"
          onClick={() => navigate("/register")}
          >
          Create an account
        </button>
        {error && <p style={styles.error}>{error}</p>}
      </div>
    </div>
  );
}

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

export default Login;

