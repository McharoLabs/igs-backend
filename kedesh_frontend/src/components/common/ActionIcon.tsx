import React from "react";
import { FaTrash, FaEdit, FaEye } from "react-icons/fa";

type ActionIconProps = {
  type: "edit" | "delete" | "view";
  size?: number;
  onClick?: () => void;
  className?: string;
};

const ActionIcon: React.FC<ActionIconProps> = ({
  type,
  size = 20,
  onClick,
  className = "",
}) => {
  let IconComponent;

  switch (type) {
    case "edit":
      IconComponent = FaEdit;
      break;
    case "delete":
      IconComponent = FaTrash;
      break;
    case "view":
      IconComponent = FaEye;
      break;
    default:
      IconComponent = FaEdit;
  }

  return (
    <button
      onClick={onClick}
      className={`p-2 rounded-full hover:scale-110 transition-all transform ${className}`}
    >
      <IconComponent size={size} color="white" />
    </button>
  );
};

export default ActionIcon;
