import React from "react";

interface PropertyCardProps {
  title: string;
  price: number;
  image: string;
}

const PropertyCard: React.FC<PropertyCardProps> = ({ title, price, image }) => {
  return (
    <div className="border rounded shadow-lg">
      <img src={image} alt={title} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h3 className="text-xl font-bold">{title}</h3>
        <p className="text-gray-600">${price}</p>
      </div>
    </div>
  );
};

export default PropertyCard;
