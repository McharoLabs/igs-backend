import React, { useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvents,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface LocationPickerProps {
  onLocationSelect: (lat: number, lng: number) => void;
}

interface Position {
  lat: number;
  lng: number;
}

const LocationPicker: React.FC<LocationPickerProps> = ({
  onLocationSelect,
}) => {
  const defaultPosition: Position = { lat: -6.163, lng: 35.7516 };
  const [position, setPosition] = useState<Position | null>(defaultPosition);

  function ClickHandler() {
    useMapEvents({
      click(e: L.LeafletMouseEvent) {
        const latlng = e.latlng;
        setPosition(latlng);
        onLocationSelect(latlng.lat, latlng.lng);
      },
    });

    return null;
  }

  return (
    <div className="w-full h-[60vh] overflow-auto">
      <MapContainer
        center={[defaultPosition.lat, defaultPosition.lng]}
        zoom={20}
        scrollWheelZoom={true}
        dragging={true}
        style={{ width: "100%", height: "100%" }}
      >
        <TileLayer
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
          attribution="&copy; <a href='https://www.esri.com/'>Esri</a>"
        />
        <ClickHandler />
        {position && (
          <Marker position={position}>
            <Popup>
              Latitude: {position.lat}, Longitude: {position.lng}
            </Popup>
          </Marker>
        )}
      </MapContainer>
    </div>
  );
};

export default LocationPicker;
