import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import { filterHouse, setHousePage } from "../state/filter/houseFilterSlice";
import Loader from "../components/common/Loader";
import { filterRooms, setRoomPage } from "../state/filter/roomFilterSlice";
import Notification from "../components/common/Notification";
import { setActiveSearchFilter } from "../state/filter/tabsSlice";
import Pagination from "../components/common/Pagination";
import { scrollToElement } from "../utils/scrollUtils";
import RoomCard from "../components/specific/RoomCard";
import HouseCard from "../components/specific/HouseCard";
import SearchHeader from "../components/specific/SearchHeader";
import { fetchFilteredLands, setLandPage } from "../state/land/landSearchSlice";
import LandCard from "../components/cards/LandCard";

const Search = () => {
  const { activeSearchValue } = useSelector(
    (state: RootState) => state.activeFilterSearch
  );

  // Properties
  const { filteredHouse, loading: loadingHouse } = useSelector(
    (state: RootState) => state.houseFilter
  );

  const {
    filteredRooms,
    searchParams: roomSearchParams,
    loading: loadingRoom,
  } = useSelector((state: RootState) => state.roomFilter);

  const { filteredLands, loading: loadingLand } = useSelector(
    (state: RootState) => state.landFilter
  );

  const dispatch = useDispatch<AppDispatch>();

  // START OF PROPERTY FILTER
  React.useEffect(() => {
    if (filteredHouse.results.length === 0) {
      dispatch(filterHouse());
    }
  }, [dispatch, filteredHouse.results.length]);

  React.useEffect(() => {
    if (filteredRooms.results.length === 0) {
      dispatch(filterRooms());
    }
  }, [dispatch, filteredRooms.results.length, roomSearchParams]);
  console.log(filteredLands);
  React.useEffect(() => {
    if (!filteredLands && !loadingLand) {
      dispatch(fetchFilteredLands());
    }
  }, [dispatch, filteredLands, loadingLand, roomSearchParams]);

  // END OF PEOPERT FILTER

  // START FOR SELECTED ID

  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-6 py-16">
      <div className="flex w-full">
        <button
          className={`transition-all px-6 py-2 text-white font-semibold rounded-l-lg ${
            activeSearchValue === "House"
              ? "bg-primary w-[50%]"
              : "bg-secondary flex-1"
          }`}
          onClick={() => dispatch(setActiveSearchFilter("House"))}
        >
          Nyumba
        </button>

        <button
          className={`transition-all px-6 py-2 text-white font-semibold ${
            activeSearchValue === "Room"
              ? "bg-primary w-[50%]"
              : "bg-secondary flex-1"
          }`}
          onClick={() => dispatch(setActiveSearchFilter("Room"))}
        >
          Chumba
        </button>

        <button
          className={`transition-all px-6 py-2 text-white font-semibold rounded-r-lg ${
            activeSearchValue === "Land"
              ? "bg-primary w-[50%]"
              : "bg-secondary flex-1"
          }`}
          onClick={() => dispatch(setActiveSearchFilter("Land"))}
        >
          Ardhi
        </button>
      </div>

      <Loader loading={loadingHouse} label="Inatafuta nyumba" />
      <Loader loading={loadingRoom} label="Inatafuta vyumba" />

      <div className=".filtered-properties" />

      <SearchHeader />

      <div className="mt-6">
        <div className="text-3xl font-semibold text-secondary-dark font-poppins">
          Orodha ya Matokeo
        </div>
        <div className="mt-2 inline-flex items-center space-x-2">
          <span className="text-4xl font-bold text-primary font-poppins">
            {activeSearchValue === "House"
              ? filteredHouse.count.toString()
              : activeSearchValue === "Room"
              ? filteredRooms.count.toString()
              : activeSearchValue === "Land"
              ? filteredLands?.count.toString()
              : 0}
          </span>
          <span className="text-lg text-accent-gray font-poppins">matokeo</span>
        </div>
      </div>

      {/* House Listings */}
      {activeSearchValue === "House" && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mt-2">
          {filteredHouse.results.length === 0 && !loadingHouse && (
            <Notification
              message="Hakuna nyumba iliyo patikana"
              title="Nyumba"
              type="info"
              key={"house-search"}
            />
          )}
          {filteredHouse.results.map((house, index) => (
            <HouseCard house={house} key={index} />
          ))}
        </div>
      )}

      {activeSearchValue === "Room" && !loadingRoom && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mt-2">
          {filteredRooms.results.length === 0 && (
            <Notification
              message="Hakuna vyumba vilivyopatikana"
              title="Chumba"
              type="info"
              key={"room-search"}
            />
          )}
          {filteredRooms.results.map((room, index) => (
            <RoomCard room={room} key={index} />
          ))}
        </div>
      )}

      {activeSearchValue === "Land" && !loadingLand && filteredLands && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mt-2">
          {filteredLands.results.length === 0 && (
            <Notification
              message="Hakuna Ardhi iliyopatikana kwenye mfumo"
              title="Ardhi"
              type="info"
              key={"land-search"}
            />
          )}
          {filteredLands.results.map((land, index) => (
            <LandCard land={land} key={index} />
          ))}
        </div>
      )}

      {(filteredHouse.next || filteredHouse.previous) &&
        activeSearchValue === "House" && (
          <div className="flex items-center justify-center mt-8">
            <Pagination
              key={filteredHouse.count}
              next={filteredHouse.next}
              previous={filteredHouse.previous}
              onClick={(page: string | null) => {
                dispatch(setHousePage(page));
                dispatch(filterHouse());
                scrollToElement(".filtered-properties", "smooth");
              }}
            />
          </div>
        )}

      {(filteredRooms.next || filteredRooms.previous) &&
        activeSearchValue === "Room" && (
          <div className="flex items-center justify-center mt-8">
            <Pagination
              key={filteredHouse.count}
              next={filteredHouse.next}
              previous={filteredHouse.previous}
              onClick={(page: string | null) => {
                dispatch(setRoomPage(page));
                dispatch(filterRooms());
                scrollToElement("filtered-properties", "smooth");
              }}
            />
          </div>
        )}

      {filteredLands &&
        (filteredLands.next || filteredLands.previous) &&
        activeSearchValue === "Land" && (
          <div className="flex items-center justify-center mt-8">
            <Pagination
              key={filteredLands.count}
              next={filteredLands.next}
              previous={filteredLands.previous}
              onClick={(page: string | null) => {
                dispatch(setLandPage(page));
                dispatch(fetchFilteredLands());
                scrollToElement("filtered-properties", "smooth");
              }}
            />
          </div>
        )}

      <div className="mb-6"></div>
    </div>
  );
};

export default Search;
