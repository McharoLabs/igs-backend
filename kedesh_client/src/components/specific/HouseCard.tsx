import React from "react";
import { House } from "../../types/houseType";
import { Bed, Home, MapPin, Droplet } from "lucide-react";
import useNavigation from "../../hooks/useNavigation";
import { formatPrice } from "../../utils/PriceFormat";
import { CATEGORY } from "../../types/enums";

type HouseCardProps = {
  house: House;
};

const HouseCard: React.FC<HouseCardProps> = ({ house }) => {
  const nav = useNavigation();

  const getCategoryBadgeStyle = () => {
    return house.category === CATEGORY.RENTAL
      ? "bg-accent-coral text-white"
      : "bg-accent-yellow text-secondary";
  };

  return (
    <div className="bg-white flex flex-col justify-between shadow-lg rounded-lg overflow-hidden transition-all hover:scale-105 hover:shadow-2xl">
      {/* House Image */}
      <img
        src={house.images[0] || "default-image.jpg"}
        alt={house.price.toString()}
        className="w-full h-44 sm:h-52 object-cover rounded-t-lg"
      />

      {/* House Details */}
      <div className="p-6 text-left space-y-2">
        {/* Location */}
        <div className="flex items-center text-sm text-accent-gray space-x-2">
          <MapPin className="text-accent-yellow w-5 h-5" />
          <p className="font-semibold text-secondary">
            {house.location.region}, {house.location.district}
          </p>
        </div>

        {/* Kata (Ward) */}
        <div className="flex items-center text-xs text-accent-gray">
          <span className="font-semibold text-secondary mr-1">Kata:</span>
          <span>{house.location.ward}</span>
        </div>

        {/* Mtaa (Street) */}
        <div className="flex items-center text-xs text-accent-gray">
          <span className="font-semibold text-secondary mr-1">Mtaa:</span>
          <span>{house.location.street}</span>
        </div>

        {/* Rental Duration */}
        {house.category === CATEGORY.RENTAL && house.rental_duration && (
          <div className="flex items-center text-xs text-accent-gray">
            <Droplet className="w-4 h-4 text-accent-yellow mr-1" />
            <span>
              Muda wa pango:{" "}
              <span className="font-medium text-secondary">
                {house.rental_duration}
              </span>
            </span>
          </div>
        )}

        {/* Price */}
        <p className="text-xl font-semibold text-accent-coral pt-2">
          Bei: {formatPrice(house.price, "TZS")}
        </p>

        {/* House Features */}
        <div className="grid grid-cols-3 gap-2 text-xs text-accent-gray pt-1">
          <div className="flex items-center">
            <Bed className="w-4 h-4 text-accent-yellow mr-1" />
            <span>{house.total_bed_room} Chumba</span>
          </div>
          <div className="flex items-center">
            <Droplet className="w-4 h-4 text-accent-yellow mr-1" />
            <span>{house.total_bath_room} Bafu</span>
          </div>
          <div className="flex items-center">
            <Home className="w-4 h-4 text-accent-yellow mr-1" />
            <span>{house.total_dining_room} Sebule</span>
          </div>
        </div>
      </div>

      {/* Bottom Action */}
      <div className="flex justify-between items-center p-4 bg-secondary-light">
        {/* Category Badge */}
        <span
          className={`hover:primary-shadow inline-block text-xs font-semibold px-3 py-1 rounded-full ${getCategoryBadgeStyle()}`}
        >
          {house.category === CATEGORY.RENTAL ? "Kupangisha" : "Kuuzwa"}
        </span>

        {/* View Details Button */}
        <button
          onClick={() => nav.goToClientHouseDetail(house.property_id)}
          className="bg-secondary hover:white-shadow text-white text-sm font-semibold py-2 px-4 rounded-full transition duration-300 hover:bg-secondary-dark focus:outline-none"
        >
          Tazama zaidi
        </button>
      </div>
    </div>
  );
};

export default HouseCard;
