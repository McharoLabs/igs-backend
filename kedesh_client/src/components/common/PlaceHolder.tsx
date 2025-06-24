import React from "react";

type PlaceHolderProps = {
  onClick?: () => void;
};

export const ImagePlaceholder: React.FC<PlaceHolderProps> = ({ onClick }) => (
  <div
    className="w-full h-72 bg-gray-200 flex justify-center items-center text-xl text-gray-600 border-dashed border-2 border-gray-300"
    onClick={(e) => {
      e.preventDefault();
      if (onClick) onClick();
    }}
  >
    Add Image
  </div>
);

export const RoomPlaceholder: React.FC<PlaceHolderProps> = ({ onClick }) => (
  <div
    className="w-full h-40 bg-gray-200 flex justify-center items-center text-xl text-gray-600 border-dashed border-2 border-gray-300"
    onClick={(e) => {
      e.preventDefault();
      if (onClick) onClick();
    }}
  >
    Add Room
  </div>
);
