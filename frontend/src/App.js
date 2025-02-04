import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/loginPage";
import Pendaftaran from "./pages/pagePendaftaran";
import DashboardLayout from "./pages/DashboardLayout"; // Import layout

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          {/* Halaman utama (Login) */}
          <Route path="/" element={<LoginPage />} />

          {/* Group Route untuk Dashboard */}
          <Route path="/dashboard" element={<DashboardLayout />}>
            <Route path="pendaftaran" element={<Pendaftaran />} />
          </Route>
        </Routes>
      </Router>
    </div>
  );
}
export default App