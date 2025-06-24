import React from "react";

interface CardProps {
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

const Card: React.FC<CardProps> = ({
  title = "",
  children,
  footer,
  className = "",
  onClick,
}) => {
  return (
    <div
      onClick={onClick}
      className={`min-w-min bg-white p-8 rounded-lg shadow-lg ${className}`}
    >
      <h2 className="text-2xl font-bold text-center text-gray-700 mb-6">
        {title}
      </h2>
      <div className="space-y-4">{children}</div>
      {footer && <div className="mt-4">{footer}</div>}
    </div>
  );
};

export default Card;
