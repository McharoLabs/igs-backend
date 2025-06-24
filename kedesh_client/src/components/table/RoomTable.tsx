import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../state/store";
import { fetchRoom } from "../../state/room/MyRoomListSlice";
import { MdDelete, MdVisibility } from "react-icons/md";
import { Room } from "../../types/RoomType";
import { formatPrice } from "../../utils/PriceFormat";

const RoomTable = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { error, rooms, loading } = useSelector(
    (state: RootState) => state.agentRoomList
  );

  React.useEffect(() => {
    if (rooms.results.length === 0) {
      dispatch(fetchRoom());
    }
  }, [dispatch, rooms.results.length]);

  const handleDelete = (id: string) => {
    console.log("Deleting room:", id);
  };

  const handleView = (id: string) => {
    console.log("Viewing room:", id);
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
              {rooms.results.map((room: Room, index: number) => (
                <tr
                  key={index}
                  className=" border-b border-accent.gray/30 hover:bg-body"
                >
                  <td className="px-6 py-4 text-center">{index + 1}</td>
                  <td className="px-6 py-4 text-center">
                    {room.location?.region ?? "Hakuna"}
                  </td>
                  <td className="px-6 py-4 text-center">
                    {room.room_category}
                  </td>
                  <td className="px-6 py-4 text-center">
                    {formatPrice(room.price)}
                  </td>
                  <td className="px-6 py-4 text-center">{room.condition}</td>
                  <td className="px-6 py-4 text-center">
                    <div className="flex items-center justify-center gap-4">
                      <button
                        onClick={() => handleView(room.property_id)}
                        className="text-primary hover:text-primary-dark"
                        title="Angalia"
                      >
                        <MdVisibility size={20} />
                      </button>
                      <button
                        onClick={() => handleDelete(room.property_id)}
                        className="text-accent-coral hover:text-red-700"
                        title="Futa"
                      >
                        <MdDelete size={20} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {rooms.results.length === 0 && (
                <tr>
                  <td
                    colSpan={6}
                    className="px-6 py-6 text-center text-accent.gray"
                  >
                    Hakuna vyumba vilivyopatikana.
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

export default RoomTable;
