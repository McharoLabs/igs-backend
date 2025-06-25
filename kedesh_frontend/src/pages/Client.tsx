import React from "react";
import Hero from "../components/sections/Hero";
import Banner from "../components/sections/Banner";
import ServiceSection from "../components/sections/Service";

const Client: React.FC = () => {
  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="min-h-screen">
      <Hero />

      <Banner />

      <ServiceSection />
    </div>
  );
};

export default Client;
