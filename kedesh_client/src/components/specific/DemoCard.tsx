import React from "react";
import { Property } from "../../types/PropertyType";
import { CATEGORY, PROPERTY_TYPE } from "../../types/enums";
import { MdLocationOn } from "react-icons/md";
import { formatPrice } from "../../utils/PriceFormat";
import useNavigation from "../../hooks/useNavigation";

type DemoCardProps = {
  property: Property;
};

const DemoCard: React.FC<DemoCardProps> = ({ property }) => {
  const navigate = useNavigation();

  const getCategoryBadgeStyle = () => {
    return property.category === CATEGORY.RENTAL
      ? "bg-accent-coral text-white"
      : "bg-accent-yellow text-secondary";
  };

  return (
    <div className="bg-white shadow-lg rounded-lg overflow-hidden transition-all hover:scale-105 hover:shadow-2xl">
      <img
        src={property.images[0] || "default-image.jpg"}
        alt={property.category}
        className="w-full h-44 sm:h-52 object-cover rounded-t-lg"
      />

      <div className="p-6 text-left">
        {/* Location */}
        <div className="flex items-center text-sm text-accent-gray space-x-2">
          <MdLocationOn className="text-accent-yellow" />
          <p className="font-semibold text-secondary">
            {property.location.region}, {property.location.district}
          </p>
        </div>

        {/* Ward */}
        <div className="flex items-center text-xs text-accent-gray mt-1">
          <span className="font-semibold text-secondary mr-1">Kata:</span>
          <span>{property.location.ward}</span>
        </div>

        {/* Street */}
        <div className="flex items-center text-xs text-accent-gray">
          <span className="font-semibold text-secondary mr-1">Mtaa:</span>
          <span>{property.location.street}</span>
        </div>

        {/* Price */}
        <p className="text-xl font-semibold text-accent-coral mt-4">
          Bei: {formatPrice(property?.price, "TZS")}
        </p>
      </div>

      {/* Bottom action */}
      <div className="flex justify-between items-center p-4 bg-secondary-light">
        {/* Category Badge */}
        <span
          className={`inline-block text-xs font-semibold px-3 py-1 rounded-full ${getCategoryBadgeStyle()}`}
        >
          {property.category === CATEGORY.RENTAL ? "Kupangisha" : "Kuuzwa"}
        </span>

        {/* Button */}
        <button
          onClick={() =>
            property.property_type === PROPERTY_TYPE.ROOM
              ? navigate.goToClientRoomDetail(property.property_id)
              : navigate.goToClientHouseDetail(property.property_id)
          }
          className="bg-secondary text-white text-sm font-semibold py-2 px-4 rounded-full transition duration-300 hover:bg-secondary-dark focus:outline-none"
        >
          Tazama zaidi
        </button>
      </div>
    </div>
  );
};

export default DemoCard;
