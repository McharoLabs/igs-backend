import React from "react";
import {
  FaPhoneAlt,
  FaEnvelope,
  FaMapMarkerAlt,
  FaFacebook,
  FaTwitter,
  FaLinkedin,
  FaCheckCircle,
} from "react-icons/fa";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import {
  fetchCompanyInformation,
  resetCompanyInformationState,
} from "../state/company/CompanyInformationSlice";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";
import mission from "../assets/images/mission-removebg-preview.png";
import ourStory from "../assets/images/our_story-removebg-preview.png";

const AboutUs: React.FC = () => {
  const { companyInformations, error, loading } = useSelector(
    (state: RootState) => state.companyInformation
  );
  const dispatch = useDispatch<AppDispatch>();

  React.useEffect(() => {
    if (!companyInformations) {
      dispatch(fetchCompanyInformation());
    }
  }, [dispatch, companyInformations]);

  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 font-poppins">
      <Message
        isOpen={!!error}
        message={error || ""}
        type="error"
        xClose={() => dispatch(resetCompanyInformationState())}
        title="Hitilafu"
      />
      {loading && (
        <Loader label="Inapakia taarifa za kampuni" loading={loading} />
      )}

      {!loading && (
        <div className="space-y-20">
          {/* Hero Section */}
          <div className="bg-primary-light rounded-xl py-12 px-6 text-center shadow-md">
            <h1 className="text-5xl font-extrabold text-secondary mb-4">
              Kuhusu Sisi
            </h1>
            <p className="text-lg text-secondary-dark max-w-2xl mx-auto">
              Jifunze zaidi kuhusu kampuni yetu, maadili yetu, na timu
              inayosimamia huduma zetu.
            </p>
          </div>

          {/* Our Story */}
          <div className="grid md:grid-cols-2 gap-10 items-center">
            <div>
              <h2 className="text-3xl font-bold text-primary mb-4">
                Hadithi Yetu
              </h2>
              <p className="text-gray-700 leading-relaxed">
                Sisi ni kampuni inayojitolea kutoa huduma bora za mali
                isiyohamishika sokoni. Lengo letu ni kufanya upangishaji na
                uuzaji wa mali kuwa rahisi na bila shida.
              </p>
            </div>
            <img src={ourStory} alt="Our Story" className="w-full " />
          </div>

          {/* Mission and Values */}
          <div className="grid md:grid-cols-2 gap-10 items-center">
            <img
              src={mission}
              alt="Mission"
              className="w-64 h-64 order-last md:order-first"
            />
            <div>
              <h2 className="text-3xl font-bold text-primary mb-4">
                Dhamira Yetu
              </h2>
              <p className="text-gray-700 leading-relaxed">
                Dhamira yetu ni kuwapa watu uwezo wa kufanya maamuzi sahihi
                kuhusu mali, kwa kuwapatia huduma za kuaminika na bora katika
                kila hatua.
              </p>
            </div>
          </div>

          {/* Values */}
          <div>
            <h2 className="text-3xl font-bold text-primary mb-6 text-center">
              Maadili Yetu
            </h2>
            <div className="grid sm:grid-cols-2 gap-6">
              {[
                "Uaminifu na Uwazi",
                "Mpangilio wa Mteja Kwanza",
                "Ubora katika Utoaji Huduma",
                "Ujitolea kwa Ubunifu",
              ].map((value, idx) => (
                <div
                  key={idx}
                  className="flex items-start space-x-3 p-4 border-l-4 border-primary bg-white shadow-sm rounded-lg"
                >
                  <FaCheckCircle className="text-primary text-2xl mt-1" />
                  <span className="text-gray-800 text-lg">{value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Contact Info */}
          <div>
            <h2 className="text-3xl font-bold text-primary mb-6 text-center">
              Wasiliana Nasi
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* Phone */}
              <ContactCard
                icon={<FaPhoneAlt className="text-3xl text-accent-yellow" />}
                title="Simu"
                text={companyInformations?.support_phone}
              />
              {/* Email */}
              <ContactCard
                icon={<FaEnvelope className="text-3xl text-accent-yellow" />}
                title="Barua pepe"
                text={
                  <a
                    href={`mailto:${companyInformations?.support_email}`}
                    className="hover:underline text-primary"
                  >
                    {companyInformations?.support_email}
                  </a>
                }
              />
              {/* Address */}
              <ContactCard
                icon={
                  <FaMapMarkerAlt className="text-3xl text-accent-yellow" />
                }
                title="Anwani"
                text={companyInformations?.headquarters}
              />
            </div>
          </div>

          {/* Social Media */}
          <div className="text-center">
            <h2 className="text-3xl font-bold text-primary mb-4">Tufuate</h2>
            <p className="text-gray-600 mb-6">
              Endelea kupata taarifa na kuungana nasi kupitia mitandao yetu ya
              kijamii:
            </p>
            <div className="flex justify-center space-x-6 text-accent-coral">
              <SocialIcon href="https://www.facebook.com/kedeshlimited">
                <FaFacebook />
              </SocialIcon>
              <SocialIcon href="https://twitter.com/kedeshlimited">
                <FaTwitter />
              </SocialIcon>
              <SocialIcon href="https://www.linkedin.com/company/kedeshlimited">
                <FaLinkedin />
              </SocialIcon>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AboutUs;

// Contact Card Component
const ContactCard = ({
  icon,
  title,
  text,
}: {
  icon: React.ReactNode;
  title: string;
  text: React.ReactNode;
}) => (
  <div className="bg-white shadow-md rounded-xl p-6 flex items-start space-x-4 border-l-4 border-primary hover:shadow-xl transition-shadow duration-300">
    <div>{icon}</div>
    <div>
      <h3 className="text-xl font-semibold text-secondary mb-1">{title}</h3>
      <p className="text-gray-700">{text}</p>
    </div>
  </div>
);

// Social Icon Component
const SocialIcon = ({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) => (
  <a
    href={href}
    target="_blank"
    rel="noopener noreferrer"
    className="text-4xl hover:text-primary transition-colors"
  >
    {children}
  </a>
);
