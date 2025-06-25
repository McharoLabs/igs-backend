import React from "react";
import { UseFormRegisterReturn } from "react-hook-form";

interface FileInputProps {
  label: string;
  error?: string;
  register: UseFormRegisterReturn<string>;
  className?: string;
  multiple?: boolean;
  accept?: string;
}

const FileInput: React.FC<FileInputProps> = ({
  label,
  error,
  register,
  className = "",
  multiple = false,
  accept = "image/*",
}) => {
  return (
    <div className={className}>
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <input
        type="file"
        accept={accept}
        multiple={multiple}
        {...register}
        className="mt-1 block w-full text-sm text-gray-500"
      />
      {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
    </div>
  );
};

export default FileInput;
