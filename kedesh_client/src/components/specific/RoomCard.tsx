import React from "react";
import { Room } from "../../types/RoomType";
import { MapPin, Droplet } from "lucide-react";
import useNavigation from "../../hooks/useNavigation";
import { formatPrice } from "../../utils/PriceFormat";

type RoomCardProps = {
  room: Room;
};

const RoomCard: React.FC<RoomCardProps> = ({ room }) => {
  const nav = useNavigation();

  const getCategoryBadgeStyle = () => {
    return room.room_category === "Rental"
      ? "bg-accent-coral text-white"
      : "bg-accent-yellow text-secondary";
  };

  return (
    <div className="bg-white shadow-lg rounded-lg overflow-hidden transition-all hover:scale-105 hover:shadow-2xl">
      {/* Room Image */}
      <img
        src={room.images[0] || "default-image.jpg"}
        alt={room.room_category}
        className="w-full h-44 sm:h-52 object-cover rounded-t-lg"
      />

      {/* Room Details */}
      <div className="p-6 text-left space-y-2">
        {/* Location */}
        <div className="flex items-center text-sm text-accent-gray space-x-2">
          <MapPin className="text-accent-yellow w-5 h-5" />
          <p className="font-semibold text-secondary">
            {room.location.region}, {room.location.district}
          </p>
        </div>

        {/* Kata (Ward) */}
        <div className="flex items-center text-xs text-accent-gray">
          <span className="font-semibold text-secondary mr-1">Kata:</span>
          <span>{room.location.ward}</span>
        </div>

        {/* Mtaa (Street) */}
        <div className="flex items-center text-xs text-accent-gray">
          <span className="font-semibold text-secondary mr-1">Mtaa:</span>
          <span>{room.location.street}</span>
        </div>

        {/* Rental Duration (if available) */}
        {room.rental_duration && (
          <div className="flex items-center text-xs text-accent-gray">
            <Droplet className="w-4 h-4 text-accent-yellow mr-1" />
            <span>
              Muda pango:{" "}
              <span className="font-medium text-secondary">
                {room.rental_duration}
              </span>
            </span>
          </div>
        )}

        {/* Price */}
        <p className="text-xl font-semibold text-accent-coral pt-2">
          Bei: {formatPrice(room.price, "TZS")}
        </p>
      </div>

      {/* Bottom Action */}
      <div className="flex justify-between items-center p-4 bg-secondary-light">
        {/* Category Badge */}
        <span
          className={`inline-block text-xs font-semibold px-3 py-1 rounded-full hover:primary-shadow ${getCategoryBadgeStyle()}`}
        >
          {room.room_category === "Rental" ? "Kupangisha" : "Kuuzwa"}
        </span>

        {/* View Details Button */}
        <button
          onClick={() => nav.goToClientRoomDetail(room.property_id)}
          className="bg-secondary text-white text-sm font-semibold py-2 px-4 rounded-full transition duration-300 hover:bg-secondary-dark focus:outline-none hover:white-shadow"
        >
          Tazama zaidi
        </button>
      </div>
    </div>
  );
};

export default RoomCard;
