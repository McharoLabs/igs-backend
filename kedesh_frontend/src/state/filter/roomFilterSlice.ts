import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { ROOM_CATEGORY } from "../../types/enums";
import { RoomResponse } from "../../types/RoomType";
import { RootState } from "../store";

interface SearchParamsType {
  roomCategory: ROOM_CATEGORY | null;
  region: string | null;
  district: string | null;
  minPrice: string | null;
  maxPrice: string | null;
  ward: string | null;
  street: string | null;
  page: string | null;
}

export interface FilterHouseState {
  searchParams: SearchParamsType;
  filteredRooms: RoomResponse;
  detail: string | null;
  loading: boolean;
  error: string | null;
}

const initializeSearchParams: SearchParamsType = {
  roomCategory: null,
  district: null,
  maxPrice: null,
  minPrice: null,
  street: null,
  ward: null,
  region: null,
  page: null,
};

const initializeFilteredResponse: RoomResponse = {
  count: 0,
  next: null,
  previous: null,
  results: [],
};

const initialState: FilterHouseState = {
  searchParams: initializeSearchParams,
  filteredRooms: initializeFilteredResponse,
  detail: null,
  loading: false,
  error: null,
};

export const filterRooms = createAsyncThunk<
  RoomResponse,
  void,
  { rejectValue: string }
>("filterRooms/filterRooms", async (_, { rejectWithValue, getState }) => {
  try {
    const state = getState() as RootState;
    const data = state.roomFilter.searchParams;

    const params = new URLSearchParams();
    if (data.roomCategory) params.append("roomCategory", data.roomCategory);
    if (data.region) params.append("region", data.region);
    if (data.district) params.append("district", data.district);
    if (data.ward) params.append("ward", data.ward);
    if (data.street) params.append("street", data.street);
    if (data.minPrice) params.append("minPrice", data.minPrice);
    if (data.maxPrice) params.append("maxPrice", data.maxPrice);
    if (data.page) params.append("page", data.page.toString());

    const endpoint = `${endpoints.filterRooms}?${params.toString()}`;
    const response = await apiClient.get(endpoint);

    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data?.detail);
    }
    return rejectWithValue("Failed to fetch rooms");
  }
});

const FilterHouseSlice = createSlice({
  name: "filterRooms",
  initialState,
  reducers: {
    setRoomSearchParams: (
      state,
      action: PayloadAction<Partial<SearchParamsType>>
    ) => {
      state.searchParams = { ...state.searchParams, ...action.payload };
    },
    setRoomPage: (state, action: PayloadAction<string | null>) => {
      state.searchParams.page = action.payload;
    },
    resetfilteredRooms: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
      state.searchParams = initializeSearchParams;
      state.filteredRooms = initializeFilteredResponse;
    },
    resetParams: (state) => {
      state.searchParams = initializeSearchParams;
      state.filteredRooms = initializeFilteredResponse;
    },
    resetRoomPage: (state) => {
      state.searchParams.page = null;
      state.filteredRooms = initializeFilteredResponse;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(filterRooms.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        filterRooms.fulfilled,
        (state, action: PayloadAction<RoomResponse>) => {
          state.loading = false;
          state.filteredRooms = action.payload;
        }
      )
      .addCase(filterRooms.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch rooms";
      });
  },
});

export const {
  resetfilteredRooms,
  setRoomSearchParams,
  setRoomPage,
  resetParams,
  resetRoomPage,
} = FilterHouseSlice.actions;

export default FilterHouseSlice.reducer;
