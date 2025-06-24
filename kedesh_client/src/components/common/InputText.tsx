import React from "react";
import { UseFormRegisterReturn } from "react-hook-form";

interface TextInputProps {
  label: string;
  type?: "email" | "number" | "password" | "tel" | "text" | "url";
  error?: string;
  register: UseFormRegisterReturn<string>;
  className?: string;
  placeholder?: string;
  disabled?: boolean;
}

const TextInput: React.FC<TextInputProps> = ({
  label,
  type = "text",
  error,
  register,
  className = "",
  placeholder = "",
  disabled = false,
}) => {
  return (
    <div className={className}>
      <label
        htmlFor={register.name}
        className="block text-sm font-medium text-gray-600"
      >
        {label}
      </label>
      <input
        id={register.name}
        disabled={disabled}
        type={type}
        placeholder={placeholder}
        autoComplete="new-password"
        {...register}
        className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary 
          ${
            disabled
              ? "bg-secondary-light text-secondary-dark border-secondary cursor-not-allowed"
              : "border-gray-300"
          } 
          ${error ? "border-accent-coral" : ""}`}
      />
      {error && <p className="text-accent-coral text-xs mt-1">{error}</p>}
    </div>
  );
};

export default TextInput;
