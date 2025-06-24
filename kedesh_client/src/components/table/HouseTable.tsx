import React from "react";
import { AppDispatch, RootState } from "../../state/store";
import { useDispatch, useSelector } from "react-redux";
import { fetchHouse } from "../../state/house/myHouseSlice";
import { House } from "../../types/houseType";
import { formatPrice } from "../../utils/PriceFormat";
import { MdDelete, MdVisibility } from "react-icons/md";

const HouseTable = () => {
  const { error, houses, loading } = useSelector(
    (state: RootState) => state.myHouse
  );

  const dispatch = useDispatch<AppDispatch>();

  React.useEffect(() => {
    if (houses.results.length === 0) {
      dispatch(fetchHouse());
    }
  }, [dispatch, houses.results.length]);

  const handleDelete = (id: string) => {
    console.log("Deleting house:", id);
  };

  const handleView = (id: string) => {
    console.log("Viewing house:", id);
  };

  return (
    <div className="mt-8 font-poppins">
      {loading ? (
        <div className="text-center text-secondary text-lg font-medium py-4">
          Inapakia vyumba...
        </div>
      ) : error ? (
        <div className="text-center text-red-600 font-medium py-4">
          Imeshindikana kupakia vyumba: {error}
        </div>
      ) : (
        <div className="overflow-x-auto shadow rounded-md ">
          <table className="min-w-full text-sm text-left text-secondary bg-white rounded-md">
            <thead className="text-xs uppercase bg-primary text-white">
              <tr>
                {["#", "Eneo", "Aina", "Bei", "Hali", "Hatua"].map(
                  (header, i) => (
                    <th
                      key={i}
                      className="px-6 py-4 w-1/6 text-center font-semibold tracking-wider"
                    >
                      {header}
                    </th>
                  )
                )}
              </tr>
            </thead>
            <tbody>
              {houses.results.map((house: House, index: number) => (
                <tr
                  key={index}
                  className=" border-b border-accent.gray/30 hover:bg-body"
                >
                  <td className="px-6 py-4 text-center">{index + 1}</td>
                  <td className="px-6 py-4 text-center">
                    {house.location?.region ?? "Hakuna"}
                  </td>
                  <td className="px-6 py-4 text-center">{house.category}</td>
                  <td className="px-6 py-4 text-center">
                    {formatPrice(house.price)}
                  </td>
                  <td className="px-6 py-4 text-center">{house.condition}</td>
                  <td className="px-6 py-4 text-center">
                    <div className="flex items-center justify-center gap-4">
                      <button
                        onClick={() => handleView(house.property_id)}
                        className="text-primary hover:text-primary-dark"
                        title="Angalia"
                      >
                        <MdVisibility size={20} />
                      </button>
                      <button
                        onClick={() => handleDelete(house.property_id)}
                        className="text-accent-coral hover:text-red-700"
                        title="Futa"
                      >
                        <MdDelete size={20} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {houses.results.length === 0 && (
                <tr>
                  <td
                    colSpan={6}
                    className="px-6 py-6 text-center text-accent.gray"
                  >
                    Hakuna Nyumba iliyopatikana.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default HouseTable;
