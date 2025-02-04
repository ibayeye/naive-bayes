import { Outlet } from "react-router-dom";
import Sidebar from "./sidebar";

const DashboardLayout = () => {
  return (
    <div className="flex">
      <Sidebar />
      <div className="p-4 flex-1">
        <Outlet /> {/* Ini akan menampilkan halaman dalam dashboard */}
      </div>
    </div>
  );
};

export default DashboardLayout;
