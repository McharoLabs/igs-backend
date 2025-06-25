import React, { useState } from "react";
import useNavigation from "../../hooks/useNavigation";
import { AlignRight } from "lucide-react";
import { ROUTES } from "../../routes/routes";
import { useLocation } from "react-router-dom";
import { useSelector } from "react-redux";
import { RootState } from "../../state/store";

const ClientTopBar: React.FC = () => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  const { goToClient, goToAboutUs, goToSearch, goToDashboard } =
    useNavigation();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white/80 text-black/70 fixed top-0 left-0 w-full z-50 shadow-lg backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 py-5 flex items-center justify-between">
        {/* Logo */}
        <div
          className="flex flex-row items-center cursor-pointer text-black"
          onClick={goToClient}
        >
          {/* <img src="/logo.png" className="h-8 me-1" alt="Kedesh Logo" /> */}
          <div className="bg-primary text-white h-[40px] w-[40px] flex justify-center items-center rounded-full text-3xl font-bold hover:primary-shadow duration-300">
            K
          </div>
          <h1 className="text-3xl">edesh</h1>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex space-x-2 items-center">
          <button
            onClick={goToClient}
            className={`${
              location.pathname === ROUTES.CLIENT.path
                ? "text-xl text-primary font-bold"
                : ""
            } inline-block text-lg py-1 px-4 hover:primary-shadow hover:bg-primary hover:text-white rounded transition-all duration-300 hover:scale-110`}
          >
            Nyumbani
          </button>
          <button
            onClick={goToSearch}
            className={`${
              location.pathname === ROUTES.CLIENT_SEARCH.path
                ? "text-xl text-primary font-bold"
                : ""
            } inline-block text-lg py-1 px-4 hover:primary-shadow hover:bg-primary hover:text-white rounded transition-all duration-300 hover:scale-110`}
          >
            Tafutan nyumba
          </button>

          <button
            onClick={goToAboutUs}
            className={`${
              location.pathname === ROUTES.ABOUT_US.path
                ? "text-xl text-primary font-bold"
                : ""
            } inline-block text-lg py-1 px-4 hover:primary-shadow hover:bg-primary hover:text-white rounded transition-all duration-300 hover:scale-110`}
          >
            Kuhusu sisi
          </button>

          {isAuthenticated && (
            <button
              onClick={() => {
                goToDashboard();
              }}
              className={`${
                location.pathname === ROUTES.DASHBOARD.path
                  ? "text-xl text-primary font-bold"
                  : ""
              } inline-block text-lg py-1 px-4 hover:primary-shadow hover:bg-primary hover:text-white rounded transition-all duration-300 hover:scale-110`}
            >
              Dashibodi
            </button>
          )}
        </nav>

        {/* Mobile Menu Toggle */}
        <button
          className="md:hidden flex items-center"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <AlignRight size={28} />
        </button>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <nav className="md:hidden shadow-lg px-4 py-3">
          <ul className="space-y-4">
            <li>
              <button
                onClick={() => {
                  goToClient();
                  setIsMenuOpen(false);
                }}
                className="text-xl font-medium text-black/70"
              >
                Nyumbani
              </button>
            </li>

            {isAuthenticated && (
              <li>
                <button
                  onClick={() => {
                    goToDashboard();
                    setIsMenuOpen(false);
                  }}
                  className="text-xl font-medium text-black/70"
                >
                  Dashibodi
                </button>
              </li>
            )}

            <li>
              <button
                onClick={() => {
                  goToAboutUs();
                  setIsMenuOpen(false);
                }}
                className="text-xl font-medium text-black/70"
              >
                {ROUTES.ABOUT_US.name}
              </button>
            </li>
            <li>
              <button
                onClick={() => {
                  setIsMenuOpen(false);
                  goToSearch();
                }}
                className="text-xl font-medium text-black/70"
              >
                Tafuta nyumba
              </button>
            </li>
          </ul>
        </nav>
      )}
    </header>
  );
};

export default ClientTopBar;
