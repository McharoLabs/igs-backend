import React from "react";
import { Outlet } from "react-router-dom";
import AsideBar from "../components/specific/AsideBar";
import NavBar from "../components/specific/NavBar";

const HomeLayout: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);
  const handleSidebarToggle = () => {
    setIsSidebarOpen((prevState) => !prevState);
  };

  return (
    <>
      <NavBar onSidebarToggle={handleSidebarToggle} />
      <AsideBar isOpen={isSidebarOpen} toggleSidebar={handleSidebarToggle} />
      <div className="p-4 sm:ml-64">
        <div className="p-4 mt-14">
          <Outlet />
        </div>
      </div>
    </>
  );
};

export default HomeLayout;
