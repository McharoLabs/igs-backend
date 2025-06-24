import FeaturedListings from "./FeaturedListings";
import { Users, Building2, Home, Handshake } from "lucide-react";

const Banner = () => {
  return (
    <>
      {/* STATS SECTION */}
      <section className="bg-muted text-gray-800 py-12">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-2  md:grid-cols-4 gap-8 text-center">
          <div className="space-y-2">
            <Users className="mx-auto text-primary" size={28} />
            <h2 className="text-2xl font-semibold">10K+</h2>
            <p className="text-sm text-gray-600">Watumiaji Waliosajiliwa</p>
          </div>

          <div className="space-y-2">
            <Building2 className="mx-auto text-primary" size={28} />
            <h2 className="text-2xl font-semibold">5K+</h2>
            <p className="text-sm text-gray-600">Matangazo ya Nyumba</p>
          </div>

          <div className="space-y-2">
            <Home className="mx-auto text-primary" size={28} />
            <h2 className="text-2xl font-semibold">2K+</h2>
            <p className="text-sm text-gray-600">Nyumba Zilizopangishwa</p>
          </div>

          <div className="space-y-2">
            <Handshake className="mx-auto text-primary" size={28} />
            <h2 className="text-2xl font-semibold">1K+</h2>
            <p className="text-sm text-gray-600">Mawakala Waliothibitishwa</p>
          </div>
        </div>
      </section>

      {/* Featured Listings Section */}
      <FeaturedListings />
    </>
  );
};

export default Banner;
