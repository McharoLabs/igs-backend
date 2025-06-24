import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import { fetchHouse, resetMyHouseState } from "../state/house/myHouseSlice";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";
import useNavigation from "../hooks/useNavigation";
import HouseTable from "../components/specific/HouseTable";

const HouseList = () => {
  const { goToHouseDetail } = useNavigation();
  const { error, houses, loading } = useSelector(
    (state: RootState) => state.myHouse
  );

  const houseDispatch = useDispatch<AppDispatch>();

  React.useEffect(() => {
    if (houses.results.length === 0) {
      houseDispatch(fetchHouse());
    }
  }, [houseDispatch, houses.results.length]);

  return (
    <div>
      <h1 className="text-3xl font-semibold mb-6">Kedesh House List</h1>

      {/* Loader */}
      <Loader loading={loading} label="Loading Houses..." />

      {/* Error Message */}
      <Message
        autoClose={true}
        title="Error"
        type="error"
        xClose={() => houseDispatch(resetMyHouseState())}
        isOpen={!!error}
        message={error || ""}
      />

      <HouseTable houses={houses.results} onView={goToHouseDetail} />
    </div>
  );
};

export default HouseList;
