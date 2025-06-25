import React from "react";

type CardProps = {
  imgSrc?: string;
  imgAlt?: string;
  className?: string;
  renderImage?: () => JSX.Element;
  children: React.ReactNode;
};

export const Card = ({
  imgSrc,
  imgAlt,
  className,
  renderImage,
  children,
}: CardProps) => {
  return (
    <div
      className={`bg-white rounded-lg shadow-lg overflow-hidden ${className}`}
    >
      {imgSrc && (
        <img src={imgSrc} alt={imgAlt} className="w-full h-48 object-cover" />
      )}
      {renderImage && <div className="w-full h-48">{renderImage()}</div>}

      <div className="p-4">{children}</div>
    </div>
  );
};
