import useNavigation from "../hooks/useNavigation";
import { MdChevronRight } from "react-icons/md";
import RoomTable from "../components/table/RoomTable";

const Room = () => {
  const { goToDashboard, goToAddRoom } = useNavigation();

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
          <span className="font-medium text-gray-600">Vyumba</span>
        </nav>

        {/* Page Title & Button */}
        <div className="mt-8 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-800">Orodha ya Vyumba</h1>
          <button
            className="bg-primary hover:primary-shadow text-white px-4 py-2 rounded-md shadow"
            onClick={goToAddRoom}
          >
            Ongeza Chumba
          </button>
        </div>

        {/* Table of Rooms */}
        <RoomTable />
      </div>
    </div>
  );
};

export default Room;
