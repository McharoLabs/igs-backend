import React from "react";
import { LandItem } from "../../types/landType";
import { MapPin, Droplet } from "lucide-react";
import { formatPrice } from "../../utils/PriceFormat";
import { LAND_TYPE } from "../../types/enums";
import useNavigation from "../../hooks/useNavigation";

type LandCardProps = {
  land: LandItem;
};

const LandCard: React.FC<LandCardProps> = ({ land }) => {
  const { navigateToTenantLandDetail } = useNavigation();

  const getCategoryBadgeStyle = () => {
    switch (land.category) {
      case LAND_TYPE.RESIDENTIAL:
        return "bg-accent-coral text-white";
      case LAND_TYPE.COMMERCIAL:
        return "bg-accent-yellow text-secondary";
      case LAND_TYPE.AGRICULTURAL:
        return "bg-green-200 text-green-900";
      case LAND_TYPE.VACANT:
        return "bg-gray-200 text-gray-800";
      default:
        return "bg-secondary text-white";
    }
  };

  return (
    <div className="bg-white shadow-lg rounded-lg overflow-hidden transition-all hover:scale-105 hover:shadow-2xl">
      {/* Land Image */}
      <img
        src={land.images[0] || "default-land.jpg"}
        alt={land.category}
        className="w-full h-44 sm:h-52 object-cover rounded-t-lg"
      />

      {/* Land Details */}
      <div className="p-6 text-left space-y-2">
        {/* Location */}
        <div className="flex items-center text-sm text-accent-gray space-x-2">
          <MapPin className="text-accent-yellow w-5 h-5" />
          <p className="font-semibold text-secondary">
            {land.location.region}, {land.location.district}
          </p>
        </div>

        {/* Kata (Ward) */}
        <div className="flex items-center text-xs text-accent-gray">
          <span className="font-semibold text-secondary mr-1">Kata:</span>
          <span>{land.location.ward}</span>
        </div>

        {/* Mtaa (Street) */}
        <div className="flex items-center text-xs text-accent-gray">
          <span className="font-semibold text-secondary mr-1">Mtaa:</span>
          <span>{land.location.street}</span>
        </div>

        {/* Land Size */}
        <div className="flex items-center text-xs text-accent-gray">
          <Droplet className="w-4 h-4 text-accent-yellow mr-1" />
          <span>
            Ukubwa:{" "}
            <span className="font-medium text-secondary">
              {land.land_size} {land.land_size_unit}
            </span>
          </span>
        </div>

        {/* Price */}
        <p className="text-xl font-semibold text-accent-coral pt-2">
          Bei: {formatPrice(land.price, "TZS")}
        </p>
      </div>

      {/* Bottom Action */}
      <div className="flex justify-between items-center p-4 bg-secondary-light">
        {/* Category Badge */}
        <span
          className={`inline-block text-xs font-semibold px-3 py-1 rounded-full hover:primary-shadow ${getCategoryBadgeStyle()}`}
        >
          {LAND_TYPE[land.category as keyof typeof LAND_TYPE]}
        </span>

        {/* View Details Button */}
        <button
          onClick={() => navigateToTenantLandDetail(land.land_id)}
          className="bg-secondary text-white text-sm font-semibold py-2 px-4 rounded-full transition duration-300 hover:bg-secondary-dark focus:outline-none hover:white-shadow"
        >
          Tazama zaidi
        </button>
      </div>
    </div>
  );
};

export default LandCard;
