import React, { ChangeEvent } from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../state/store";
import {
  filterHouse,
  resetHousepage,
  setSearchParams,
} from "../../state/filter/houseFilterSlice";
import {
  filterRooms,
  setRoomSearchParams,
} from "../../state/filter/roomFilterSlice";
import {
  CATEGORY,
  LAND_TYPE,
  LAND_TYPE_CHOICES,
  ROOM_CATEGORY,
  ROOM_CATEGORY_CHOICES,
} from "../../types/enums";
import {
  fetchRegionDistrictList,
  resetDistrictState,
} from "../../state/district/districtSlice";
import {
  fetchRegionList,
  resetRegionState,
} from "../../state/region/regionSlice";
import Loader from "../common/Loader";
import Message from "../common/Message";
import {
  fetchFilteredLands,
  setLandSearchParams,
} from "../../state/land/landSearchSlice";

const SearchHeader = () => {
  const dispatch = useDispatch<AppDispatch>();

  const { searchParams } = useSelector((state: RootState) => state.houseFilter);

  const { searchParams: roomSearchParams } = useSelector(
    (state: RootState) => state.roomFilter
  );

  const { searchParams: landSearchParams } = useSelector(
    (state: RootState) => state.landFilter
  );

  // Regions
  const {
    regions,
    loading: loadingRegions,
    error: regionError,
  } = useSelector((state: RootState) => state.region);

  // Districts
  const {
    districts,
    loading: loadingDistricts,
    error: districtError,
  } = useSelector((state: RootState) => state.district);

  const { activeSearchValue } = useSelector(
    (state: RootState) => state.activeFilterSearch
  );

  const [selectedRegionId, setSelectedRegionId] = React.useState<string>("");
  const [selectedRegionIdForRoom, setSelectedRegionIdForRoom] =
    React.useState<string>("");
  const [selectedRegionIdForLand, setSelectedRegionIdForLand] =
    React.useState<string>("");

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (activeSearchValue === "House") {
      dispatch(setSearchParams({ [name]: value }));
      return;
    }

    if (activeSearchValue === "Room") {
      dispatch(setRoomSearchParams({ [name]: value }));
    }
  };

  const handleCategoryChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const { value } = e.target;
    dispatch(setSearchParams({ category: value as CATEGORY }));
  };

  const handleRoomCategoryChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const { value } = e.target;
    dispatch(setRoomSearchParams({ roomCategory: value as ROOM_CATEGORY }));
  };

  const handleLandCategoryChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const { value } = e.target;
    dispatch(setLandSearchParams({ category: value as LAND_TYPE }));
  };

  const handleRegionChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const { value } = e.target;

    if (activeSearchValue === "House") {
      if (value) {
        const selectedRegion = regions.find((r) => r.name === value);
        if (selectedRegion) {
          setSelectedRegionId(selectedRegion.region_id);
          dispatch(setSearchParams({ region: selectedRegion.name }));
        }
      } else {
        setSelectedRegionId("");
        dispatch(
          setSearchParams({
            region: null,
            district: null,
            ward: null,
            street: null,
          })
        );

        dispatch(resetDistrictState());
      }

      return;
    }

    if (activeSearchValue === "Room") {
      if (value) {
        const selectedRegion = regions.find((r) => r.name === value);
        if (selectedRegion) {
          setSelectedRegionIdForRoom(selectedRegion.region_id);
          dispatch(setRoomSearchParams({ region: selectedRegion.name }));
        }
      } else {
        setSelectedRegionIdForRoom("");
        dispatch(
          setRoomSearchParams({
            region: null,
            district: null,
            ward: null,
            street: null,
          })
        );

        dispatch(resetDistrictState());
      }
      return;
    }

    if (activeSearchValue === "Land") {
      if (value) {
        const selectedRegion = regions.find((r) => r.name === value);
        if (selectedRegion) {
          setSelectedRegionIdForLand(selectedRegion.region_id);
          dispatch(setLandSearchParams({ region: selectedRegion.name }));
        }
      } else {
        setSelectedRegionIdForLand("");
        dispatch(
          setLandSearchParams({
            region: null,
            district: null,
            ward: null,
            street: null,
          })
        );

        dispatch(resetDistrictState());
      }
      return;
    }
  };

  const handleDistrictChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const { value } = e.target;

    if (activeSearchValue === "House") {
      if (value) {
        const selectedDistrict = districts.find((d) => d.name === value);
        if (selectedDistrict) {
          dispatch(setSearchParams({ district: selectedDistrict.name }));
        }
      } else {
        dispatch(setSearchParams({ district: null, ward: null, street: null }));
      }

      return;
    }

    if (activeSearchValue === "Room") {
      if (value) {
        const selectedDistrict = districts.find((d) => d.name === value);
        if (selectedDistrict) {
          dispatch(setRoomSearchParams({ district: selectedDistrict.name }));
        }
      } else {
        dispatch(
          setRoomSearchParams({ district: null, ward: null, street: null })
        );
      }
      return;
    }

    if (activeSearchValue === "Land") {
      if (value) {
        const selectedDistrict = districts.find((d) => d.name === value);
        if (selectedDistrict) {
          dispatch(setLandSearchParams({ district: selectedDistrict.name }));
        }
      } else {
        dispatch(
          setLandSearchParams({ district: null, ward: null, street: null })
        );
      }
      return;
    }
  };

  const handleSearch = () => {
    if (activeSearchValue === "House") {
      dispatch(resetHousepage());
      dispatch(filterHouse());
      return;
    }

    if (activeSearchValue === "Room") {
      dispatch(filterRooms());
      return;
    }

    if (activeSearchValue === "Land") {
      dispatch(fetchFilteredLands());
      return;
    }
  };

  React.useEffect(() => {
    if (selectedRegionId) {
      dispatch(fetchRegionDistrictList(selectedRegionId));
    }
  }, [dispatch, selectedRegionId]);

  React.useEffect(() => {
    if (selectedRegionIdForRoom) {
      dispatch(fetchRegionDistrictList(selectedRegionIdForRoom));
    } else if (selectedRegionIdForLand) {
      dispatch(fetchRegionDistrictList(selectedRegionIdForLand));
    }
  }, [dispatch, selectedRegionIdForLand, selectedRegionIdForRoom]);

  // Fetch Location
  React.useEffect(() => {
    if (regions.length === 0) {
      dispatch(fetchRegionList());
    }
  }, [dispatch, regions.length]);

  return (
    <>
      <Loader loading={loadingRegions} label="Inapakia mikoa" />
      <Loader loading={loadingDistricts} label="Inapakia wilaya" />
      <Message
        type="error"
        isOpen={!!regionError}
        message={regionError || ""}
        xClose={() => dispatch(resetRegionState())}
      />

      <Message
        type="error"
        isOpen={!!districtError}
        message={districtError || ""}
        xClose={() => dispatch(resetDistrictState())}
      />
      <div className="bg-white mt-6 shadow-xl rounded-lg p-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {activeSearchValue === "Room" && (
            <select
              name="roomCategory"
              value={roomSearchParams.roomCategory || ""}
              onChange={handleRoomCategoryChange}
              className="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Chagua aina ya chumba</option>
              {ROOM_CATEGORY_CHOICES.map((category, index) => (
                <option key={index} value={category.value}>
                  {category.label}
                </option>
              ))}
            </select>
          )}

          {activeSearchValue === "House" && (
            <select
              name="category"
              value={searchParams.category || ""}
              onChange={handleCategoryChange}
              className="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Chagua aina</option>
              <option value={CATEGORY.SALE}>Kwa Uuzaji</option>
              <option value={CATEGORY.RENTAL}>Kwa Pango</option>
            </select>
          )}

          {activeSearchValue === "Land" && (
            <select
              name="category"
              value={landSearchParams.category || ""}
              onChange={handleLandCategoryChange}
              className="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Chagua aina</option>
              {LAND_TYPE_CHOICES.map((choice) => (
                <option key={choice.value} value={choice.value}>
                  {choice.label}
                </option>
              ))}
            </select>
          )}

          <select
            name="region"
            value={
              activeSearchValue === "House"
                ? searchParams.region || ""
                : activeSearchValue === "Land"
                ? landSearchParams.region || ""
                : roomSearchParams.region || ""
            }
            onChange={handleRegionChange}
            className="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="">Chagua mkoa</option>
            {regions.map((r, index) => (
              <option value={r.name} key={index}>
                {r.name}
              </option>
            ))}
          </select>

          <select
            name="district"
            value={
              activeSearchValue === "House"
                ? searchParams.district || ""
                : activeSearchValue === "Land"
                ? landSearchParams.district || ""
                : roomSearchParams.district || ""
            }
            onChange={handleDistrictChange}
            className="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="">Chagua wilaya</option>
            {districts.map((d, index) => (
              <option value={d.name} key={index}>
                {d.name}
              </option>
            ))}
          </select>

          {/* Min Price */}
          <input
            type="number"
            name="minPrice"
            value={
              activeSearchValue === "House"
                ? searchParams.minPrice || ""
                : activeSearchValue === "Land"
                ? landSearchParams.minPrice || ""
                : roomSearchParams.minPrice || ""
            }
            onChange={handleChange}
            className="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="Bei ya chini"
          />

          {/* Max Price */}
          <input
            type="number"
            name="maxPrice"
            value={
              activeSearchValue === "House"
                ? searchParams.maxPrice || ""
                : activeSearchValue === "Land"
                ? landSearchParams.maxPrice || ""
                : roomSearchParams.maxPrice || ""
            }
            onChange={handleChange}
            className="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="Bei ya juu"
          />

          {/* Search Button */}
          <button
            onClick={() => handleSearch()}
            className="bg-primary text-white px-6 py-3 rounded-lg font-semibold shadow-md hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
          >
            Tafuta
          </button>
        </div>
      </div>
    </>
  );
};

export default SearchHeader;
