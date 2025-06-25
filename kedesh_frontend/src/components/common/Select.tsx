import React from "react";
import { UseFormRegisterReturn } from "react-hook-form";

interface SelectProps {
  label: string;
  options: { value: string; label: string }[];
  error?: string;
  register: UseFormRegisterReturn<string>;
  className?: string;
}

const Select: React.FC<SelectProps> = ({
  label,
  options,
  error,
  register,
  className = "",
}) => {
  return (
    <div className={className}>
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <select
        {...register}
        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary"
      >
        <option value="">Select {label}</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <p className="text-accent-coral text-xs mt-1">{error}</p>}
    </div>
  );
};

export default Select;
