import React from "react";
import { UseFormRegisterReturn } from "react-hook-form";

interface CheckboxProps {
  label: string;
  error?: string;
  register: UseFormRegisterReturn<string>;
  className?: string;
}

const Check: React.FC<CheckboxProps> = ({
  label,
  error,
  register,
  className = "",
}) => {
  return (
    <div className={className}>
      <div className="flex items-center">
        <input
          type="checkbox"
          {...register}
          className="h-4 w-4 text-primary border-gray-300 rounded focus:ring-primary"
        />
        <label className="ml-2 text-sm text-gray-700">{label}</label>
      </div>
      {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
    </div>
  );
};

export default Check;
