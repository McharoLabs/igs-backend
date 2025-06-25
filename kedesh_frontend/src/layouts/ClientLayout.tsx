import { Outlet } from "react-router-dom";
import ClientTopBar from "../components/specific/ClientTopBar";
import Footer from "../components/specific/Footer";
import React from "react";

const ClientLayout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <ClientTopBar />
      <main className="flex-grow pt-10 ">{<Outlet />}</main>
      <Footer />
    </div>
  );
};

export default ClientLayout;
