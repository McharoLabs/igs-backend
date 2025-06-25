import React from "react";

interface LoaderProps {
  label?: string;
  loading?: boolean;
}

const Loader: React.FC<LoaderProps> = ({ label = "", loading = false }) => {
  return (
    <>
      {loading && (
        <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-gray-800 bg-opacity-50 z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-60">
            <div className="flex items-center justify-center">
              <div className="w-16 h-16 border-t-4 border-primary border-solid rounded-full animate-spin"></div>
            </div>
            <div className="mt-4 text-center">{label}</div>
          </div>
        </div>
      )}
    </>
  );
};

export default Loader;
