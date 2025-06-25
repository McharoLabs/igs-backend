import { Search } from "lucide-react";
import React, { useState } from "react";

type SearchInputProps = {
  onClick: (value: string) => void;
  placeholder: string;
};

const SearchInput: React.FC<SearchInputProps> = ({ onClick, placeholder }) => {
  const [searchValue, setSearchValue] = useState<string>("");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value);
  };

  const handleSearchClick = () => {
    onClick(searchValue);
  };

  return (
    <div className="flex justify-center items-center py-4">
      <div className="relative w-full max-w-lg">
        <input
          type="text"
          value={searchValue}
          onChange={handleInputChange}
          className="w-full p-3 pr-4 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          placeholder={placeholder}
        />

        <button
          onClick={handleSearchClick}
          className="absolute right-3 top-1.5 p-2 text-gray-500 hover:text-primary focus:outline-none"
        >
          <Search />
        </button>
      </div>
    </div>
  );
};

export default SearchInput;
