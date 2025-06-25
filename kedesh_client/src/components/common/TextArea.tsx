import React from "react";
import { UseFormRegisterReturn } from "react-hook-form";

interface TextAreaProps {
  label: string;
  error?: string;
  register: UseFormRegisterReturn<string>;
  className?: string;
  placeholder?: string;
  rows?: number;
}

const TextArea: React.FC<TextAreaProps> = ({
  label,
  error,
  register,
  className = "",
  placeholder = "",
  rows = 4,
}) => {
  return (
    <div className={className}>
      <label
        htmlFor={register.name}
        className="block text-sm font-medium text-gray-700"
      >
        {label}
      </label>
      <textarea
        id={register.name}
        placeholder={placeholder}
        rows={rows}
        {...register}
        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary"
      />
      {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
    </div>
  );
};

export default TextArea;
