import React from "react";

interface ImageGalleryProps {
  images: string[];
}

const ImageGallery: React.FC<ImageGalleryProps> = ({ images }) => {
  const sliderRef = React.useRef<HTMLDivElement | null>(null);

  const scrollSlider = (direction: "left" | "right") => {
    if (sliderRef.current) {
      const scrollAmount = 200;
      const currentScroll = sliderRef.current.scrollLeft;
      sliderRef.current.scrollLeft =
        direction === "left"
          ? currentScroll - scrollAmount
          : currentScroll + scrollAmount;
    }
  };

  return (
    <div className="relative">
      {/* Image Container (Horizontal Scrollable) */}
      <div
        ref={sliderRef}
        className="flex overflow-x-auto space-x-4 py-4 scrollbar-hidden"
        role="slider" // This is the target container for scrolling
      >
        {images.map((image, index) => (
          <div key={index} className="flex-shrink-0 w-64 h-64">
            <img
              src={image}
              alt={`House Image ${index + 1}`}
              className="w-full h-full object-cover rounded-lg shadow-lg"
            />
          </div>
        ))}
      </div>

      {/* Scroll Buttons (Left & Right) */}
      <div className="absolute inset-0 flex items-center justify-between px-4">
        <button
          className="bg-gray-900 text-white p-2 rounded-full shadow-md hover:bg-gray-700 focus:outline-none"
          onClick={() => scrollSlider("left")}
        >
          &#10094;
        </button>
        <button
          className="bg-gray-900 text-white p-2 rounded-full shadow-md hover:bg-gray-700 focus:outline-none"
          onClick={() => scrollSlider("right")}
        >
          &#10095;
        </button>
      </div>
    </div>
  );
};

export default ImageGallery;
