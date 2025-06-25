import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";
import useNavigation from "../hooks/useNavigation";
import { fetchRoom, resetMyRoomState } from "../state/room/MyRoomListSlice";
import RoomTable from "../components/specific/RoomTable";

const RoomList = () => {
  const { goToRoomDetail } = useNavigation();
  const { error, rooms, loading } = useSelector(
    (state: RootState) => state.agentRoomList
  );

  const roomDispatch = useDispatch<AppDispatch>();

  React.useEffect(() => {
    if (rooms.results.length === 0) {
      roomDispatch(fetchRoom());
    }
  }, [roomDispatch, rooms.results.length]);

  return (
    <div>
      <h1 className="text-3xl font-semibold mb-6">Kedesh Room List</h1>

      {/* Loader */}
      <Loader loading={loading} label="Loading Houses..." />

      {/* Error Message */}
      <Message
        autoClose={true}
        title="Error"
        type="error"
        xClose={() => roomDispatch(resetMyRoomState())}
        isOpen={!!error}
        message={error || ""}
      />

      <RoomTable rooms={rooms.results} onView={goToRoomDetail} />
    </div>
  );
};

export default RoomList;
