import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Library from "./pages/Library";
import Register from "./pages/Register";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/library" element={<Library />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}

export default App;

