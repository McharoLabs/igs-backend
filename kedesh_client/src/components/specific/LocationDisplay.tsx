import React from "react";

interface LocationProps {
  lat: number;
  lng: number;
}

const LocationDisplay: React.FC<LocationProps> = ({ lat, lng }) => {
  const googleMapsUrl = `https://maps.google.com/maps?q=${lat},${lng}&z=20&t=k&output=embed`;

  return (
    <div className="w-full h-full flex flex-col gap-4">
      <div className="w-full h-full">
        <iframe
          className="w-full h-full border-0"
          src={googleMapsUrl}
          allowFullScreen
          loading="lazy"
        ></iframe>
      </div>
    </div>
  );
};

export default LocationDisplay;
