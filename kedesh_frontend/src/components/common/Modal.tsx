import React from "react";
import Button from "./Button";

interface ModalProps {
  isOpen: boolean;
  onClose?: () => void;
  onSubmit?: () => void;
  xButton?: () => void;
  title?: string;
  children: React.ReactNode;
  cancelButtonLabel?: string;
  submitButtonLabel?: string;
  size?: "small" | "medium" | "large" | "full-screen";
  className?: string;
}

const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  xButton,
  title,
  children,
  cancelButtonLabel = "Cancel",
  submitButtonLabel = "Submit",
  className = "bg-white",
  size = "medium",
}) => {
  if (!isOpen) return null;

  // Define size-specific classes
  const sizeClasses = {
    small: "max-w-sm w-full p-4",
    medium: "max-w-md w-full p-6 sm:m-6 sm:px-8",
    large: "max-w-2xl w-full p-8",
    "full-screen": "w-full h-full p-0 m-0 rounded-none",
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      {/* Modal Content */}
      <div
        className={`rounded-lg shadow-lg mx-3 ${className} ${
          sizeClasses[size]
        } ${size === "full-screen" ? "h-screen" : ""}`}
      >
        {/* Modal Header */}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">{title}</h2>
          {xButton && (
            <button
              onClick={xButton}
              className="text-gray-500 hover:text-gray-800 text-3xl font-bold"
            >
              &times;
            </button>
          )}
        </div>

        {/* Modal Body */}
        <div className="mb-4">{children}</div>

        {/* Modal Footer */}
        <div className="flex gap-4 justify-end">
          {onClose && (
            <Button
              type={"button"}
              onClick={onClose}
              className="bg-red-500 hover:bg-red-400"
            >
              {cancelButtonLabel}
            </Button>
          )}
          {onSubmit && (
            <Button
              type={"button"}
              onClick={onSubmit}
              className="bg-green-500 hover:bg-green-400"
            >
              {submitButtonLabel}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Modal;
