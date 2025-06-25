import { useDispatch, useSelector } from "react-redux";
import useNavigation from "../../hooks/useNavigation";
import { AppDispatch, RootState } from "../../state/store";
import { fetchCompanyInformation } from "../../state/company/CompanyInformationSlice";
import React from "react";

const Footer = () => {
  const nav = useNavigation();
  const { companyInformations } = useSelector(
    (state: RootState) => state.companyInformation
  );
  const dispatch = useDispatch<AppDispatch>();

  React.useEffect(() => {
    if (!companyInformations) {
      dispatch(fetchCompanyInformation());
    }
  }, [dispatch, companyInformations]);

  return (
    <footer className="bg-black text-white mt-auto w-full py-12 font-poppins backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-12">
          {/* Help Section */}
          <div className=" sm:text-left">
            <h2 className="text-2xl font-semibold mb-4">Unahitaji Msaada?</h2>
            <p className="text-sm ">
              Piga simu:{" "}
              <a
                href={`tel:${
                  companyInformations?.support_phone || "0617805831"
                }`}
                className="text-primary hover:underline"
              >
                {companyInformations?.support_phone || "0617805831"}
              </a>
            </p>
            <p className="text-sm  mt-2">
              Barua pepe:{" "}
              <a
                href={`mailto:${
                  companyInformations?.support_email || "support@company.com"
                }`}
                className="text-primary hover:underline"
              >
                {companyInformations?.support_email || "support@company.com"}
              </a>
            </p>
            <p className="text-sm  mt-2">
              Makao makuu: {companyInformations?.headquarters || "N/A"}
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-xl font-semibold mb-4">Viungo vya Haraka</h3>
            <ul className="space-y-2">
              <li>
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    nav.goToClient();
                  }}
                  className="text-sm  hover:text-primary"
                >
                  Nyumbani
                </a>
              </li>
              <li>
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    nav.goToSearch();
                  }}
                  className="text-sm  hover:text-primary"
                >
                  Mali
                </a>
              </li>
              <li>
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    nav.goToAboutUs();
                  }}
                  className="text-sm  hover:text-primary"
                >
                  Kuhusu Sisi
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="text-xl font-semibold mb-4">Kisheria</h3>
            <ul className="space-y-2">
              <li>
                <a
                  href="/privacy-policy"
                  className="text-sm  hover:text-primary"
                >
                  Sera ya Faragha
                </a>
              </li>
              <li>
                <a
                  href="/terms-of-service"
                  className="text-sm  hover:text-primary"
                >
                  Masharti ya Huduma
                </a>
              </li>
            </ul>
          </div>

          {/* Social Media */}
          <div>
            <h3 className="text-xl font-semibold mb-4">Tufuatilie</h3>
            <div className="flex space-x-5 text-lg">
              <a href="https://facebook.com" className="hover:text-primary">
                <i className="fab fa-facebook-f" />
              </a>
              <a href="https://twitter.com" className="hover:text-primary">
                <i className="fab fa-twitter" />
              </a>
              <a href="https://instagram.com" className="hover:text-primary">
                <i className="fab fa-instagram" />
              </a>
              <a href="https://linkedin.com" className="hover:text-primary">
                <i className="fab fa-linkedin-in" />
              </a>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-12 text-center text-sm ">
          &copy; {new Date().getFullYear()} Kedesh Rental & Sell House Portal.
          Haki Zote Zimehifadhiwa.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
