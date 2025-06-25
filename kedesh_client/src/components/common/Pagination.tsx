import React from "react";
import { getPageNumber } from "../../utils/extractPageNumber";

interface PaginationProps {
  next: string | null;
  previous: string | null;
  onClick: (page: string | null) => void;
}

const Pagination: React.FC<PaginationProps> = ({ next, onClick, previous }) => {
  return (
    <div className="flex justify-center items-center space-x-4 mt-8">
      <button
        type="button"
        disabled={!previous}
        className="flex items-center justify-center px-6 h-12 text-base font-medium text-white bg-primary border border-transparent rounded-lg disabled:opacity-50 hover:bg-primary-dark focus:outline-none transition-all duration-300 ease-in-out"
        onClick={() => {
          if (previous) {
            onClick(getPageNumber(previous));
          }
        }}
      >
        <svg
          className="w-4 h-4 me-2 rtl:rotate-180"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 14 10"
        >
          <path
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M13 5H1m0 0 4 4M1 5l4-4"
          />
        </svg>
        Previous
      </button>

      <button
        type="button"
        disabled={!next}
        className="flex items-center justify-center px-6 h-12 text-base font-medium text-white bg-primary border border-transparent rounded-lg disabled:opacity-50 hover:bg-primary-dark focus:outline-none transition-all duration-300 ease-in-out"
        onClick={() => {
          if (next) {
            onClick(getPageNumber(next));
          }
        }}
      >
        Next
        <svg
          className="w-4 h-4 ms-2 rtl:rotate-180"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 14 10"
        >
          <path
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M1 5h12m0 0L9 1m4 4L9 9"
          />
        </svg>
      </button>
    </div>
  );
};

export default Pagination;
