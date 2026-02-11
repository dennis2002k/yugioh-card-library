import React from "react";

export default function Navbar({ onLogout }) {
  return (
    <nav style={styles.navbar}>
      <div style={styles.spacer}></div>

      <button style={styles.logoutBtn} onClick={onLogout}>
        Log Out
      </button>
    </nav>
  );
}

const styles = {
  navbar: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height: "60px",
    backgroundColor: "#1e1e1e",
    display: "flex",
    alignItems: "center",
    padding: "0 20px",
    boxSizing: "border-box",
    zIndex: 1000,
  },
  spacer: {
    flex: 1, // pushes button to the right
  },
  logoutBtn: {
    backgroundColor: "#ff4d4d",
    border: "none",
    color: "white",
    padding: "10px 16px",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "14px",
  },
};
