import React, { useEffect } from "react";

interface ButtonProps {
  label: string;
  onClick: () => void;
  style?: string;
}

interface MessageModalProps {
  isOpen: boolean;
  message: string;
  type: "success" | "error" | "info";
  xClose: () => void;
  autoClose?: boolean;
  time?: number;
  title?: string;
  buttons?: ButtonProps[];
}

const Message: React.FC<MessageModalProps> = ({
  isOpen,
  message,
  type,
  xClose,
  autoClose = false,
  time = 5000,
  title = "Success",
  buttons = [],
}) => {
  useEffect(() => {
    if (autoClose && isOpen) {
      const timer = setTimeout(() => {
        xClose();
      }, time);
      return () => clearTimeout(timer);
    }
  }, [autoClose, isOpen, time, xClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50 z-50 p-4">
      <div className="bg-white rounded-lg shadow-lg max-w-sm w-full p-6">
        <div
          className={`flex items-center justify-between mb-4 ${
            type === "success"
              ? "text-green-600"
              : type === "error"
              ? "text-accent-coral"
              : "text-gray-600"
          }`}
        >
          <h3 className="text-xl font-semibold">{title}</h3>
          <button
            onClick={xClose}
            className="text-gray-500 hover:text-gray-700 text-3xl"
          >
            &times;
          </button>
        </div>
        <p>{message}</p>
        <div className="mt-4 flex justify-end space-x-2">
          {/* Render dynamic buttons */}
          {buttons.map((button, index) => (
            <button
              key={index}
              onClick={button.onClick}
              className={`px-4 py-2 rounded-md ${
                button.style || "bg-primary text-white hover:bg-primary"
              }`}
            >
              {button.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Message;
