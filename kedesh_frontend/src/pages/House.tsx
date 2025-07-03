import useNavigation from "../hooks/useNavigation";
import { MdChevronRight } from "react-icons/md";
import HouseTable from "../components/table/HouseTable";

const House = () => {
  const { goToDashboard, goToAddHouse } = useNavigation();
  return (
    <div className="flex flex-col items-center justify-center">
      <div className="max-w-7xl w-full px-5 py-14">
        {/* Breadcrumb Navigation */}
        <nav className="text-sm text-primary flex items-center space-x-1">
          <button
            onClick={goToDashboard}
            className="hover:underline hover:text-blue-600 transition-colors"
          >
            Dashibodi
          </button>
          <MdChevronRight className="text-lg" />
          <span className="font-medium text-gray-600">Nyumba</span>
        </nav>

        {/* Page Title & Button */}
        <div className="mt-8 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-800">Orodha ya Nyumba</h1>
          <button
            className="bg-primary hover:primary-shadow text-white px-4 py-2 rounded-md shadow"
            onClick={goToAddHouse}
          >
            Ongeza nyumba
          </button>
        </div>

        {/* Table of Rooms */}
        <HouseTable />
      </div>
    </div>
  );
};

export default House;
