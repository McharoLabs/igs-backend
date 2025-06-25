import { Check, CircleX, Info } from "lucide-react";
import React from "react";

interface NotificationCardProps {
  message: string;
  type: "success" | "error" | "info";
  title: string;
}

const Notification: React.FC<NotificationCardProps> = ({
  message,
  type,
  title = "Notification",
}) => {
  const cardStyles = {
    success: "bg-green-100 text-green-700",
    error: "bg-red-100 text-red-700",
    info: "bg-blue-100 text-primary",
  }[type];

  const borderColor = {
    success: "border-green-500",
    error: "border-red-500",
    info: "border-primary",
  }[type];

  return (
    <div
      className={`w-full max-w-md mx-auto p-4 mb-4 rounded-lg shadow-lg ${cardStyles} border-l-4 ${borderColor}`}
    >
      <div className="flex items-center">
        <div className="flex-shrink-0">
          {type === "success" ? (
            <Check />
          ) : type === "error" ? (
            <CircleX />
          ) : (
            <Info />
          )}
        </div>
        <div className="ml-3 flex-1">
          <p className="font-medium">{title}</p>
          <p className="text-sm">{message}</p>
        </div>
      </div>
    </div>
  );
};

export default Notification;
