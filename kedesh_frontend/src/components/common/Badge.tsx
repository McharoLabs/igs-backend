import React from "react";

type BadgeProps = {
  color:
    | "gray"
    | "info"
    | "failure"
    | "success"
    | "warning"
    | "indigo"
    | "purple"
    | "pink";
  children: React.ReactNode;
  className?: string;
};

const Badge: React.FC<BadgeProps> = ({ color, children, className }) => {
  const BadgeClasses = {
    gray: "bg-gray-500 text-white",
    info: "bg-primary text-white",
    failure: "bg-red-500 text-white",
    success: "bg-green-500 text-white",
    warning: "bg-yellow-500 text-white",
    indigo: "bg-indigo-500 text-white",
    purple: "bg-purple-500 text-white",
    pink: "bg-pink-500 text-white",
  };

  return (
    <span
      className={`px-3 py-1 text-sm font-medium rounded-full text-center justify-center items-center flex max-w-14 ${BadgeClasses[color]} ${className}`}
    >
      {children}
    </span>
  );
};

export default Badge;
