import React from "react";

interface ImageProps {
  src: string;
  alt?: string;
  className?: string;
  loading?: "lazy" | "eager";
}

const Image: React.FC<ImageProps> = ({
  src,
  alt = "Image",
  className = "",
  loading = "lazy",
}) => {
  return (
    <img
      src={src}
      alt={alt}
      className={`object-cover ${className}`}
      loading={loading}
      srcSet={`${src}?w=400 400w, ${src}?w=800 800w, ${src}?w=1200 1200w`}
    />
  );
};

export default Image;
