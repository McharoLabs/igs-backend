import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { CATEGORY } from "../../types/enums";
import { HouseResponse } from "../../types/houseType";
import { RootState } from "../store";

interface SearchParamsType {
  category: CATEGORY | null;
  region: string | null;
  district: string | null;
  minPrice: string | null;
  street: string | null;
  ward: string | null;
  maxPrice: string | null;
  page: string | null;
}

export interface FilterHouseState {
  searchParams: SearchParamsType;
  filteredHouse: HouseResponse;
  detail: string | null;
  loading: boolean;
  error: string | null;
}

const initializeSearchParams: SearchParamsType = {
  category: null,
  district: null,
  maxPrice: null,
  minPrice: null,
  street: null,
  ward: null,
  region: null,
  page: null,
};

const initializeFilteredResponse: HouseResponse = {
  count: 0,
  next: null,
  previous: null,
  results: [],
};

const initialState: FilterHouseState = {
  searchParams: initializeSearchParams,
  filteredHouse: initializeFilteredResponse,
  detail: null,
  loading: false,
  error: null,
};

export const filterHouse = createAsyncThunk<
  HouseResponse,
  void,
  { rejectValue: string }
>("filterHouse/filterHouse", async (_, { rejectWithValue, getState }) => {
  try {
    const state = getState() as RootState;
    const data = state.houseFilter.searchParams;

    const params = new URLSearchParams();
    if (data.category) params.append("category", data.category);
    if (data.region) params.append("region", data.region);
    if (data.district) params.append("district", data.district);
    if (data.ward) params.append("ward", data.ward);
    if (data.street) params.append("street", data.street);
    if (data.minPrice) params.append("minPrice", data.minPrice);
    if (data.maxPrice) params.append("maxPrice", data.maxPrice);
    if (data.page) params.append("page", data.page.toString());

    const endpoint = `${endpoints.filterHouse}?${params.toString()}`;
    const response = await apiClient.get(endpoint);

    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data?.detail);
    }
    return rejectWithValue("Failed to fetch houses");
  }
});

const FilterHouseSlice = createSlice({
  name: "filterHouse",
  initialState,
  reducers: {
    setSearchParams: (
      state,
      action: PayloadAction<Partial<SearchParamsType>>
    ) => {
      state.searchParams = { ...state.searchParams, ...action.payload };
    },
    setHousePage: (state, action: PayloadAction<string | null>) => {
      state.searchParams.page = action.payload;
      state.filteredHouse = initializeFilteredResponse;
    },
    resetFilteredHouse: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
      state.searchParams = initializeSearchParams;
      state.filteredHouse = initializeFilteredResponse;
    },
    resetParams: (state) => {
      state.searchParams = initializeSearchParams;
      state.filteredHouse = initializeFilteredResponse;
    },
    resetHousepage: (state) => {
      state.searchParams.page = null;
      state.filteredHouse = initializeFilteredResponse;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(filterHouse.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        filterHouse.fulfilled,
        (state, action: PayloadAction<HouseResponse>) => {
          state.loading = false;
          state.filteredHouse = action.payload;
        }
      )
      .addCase(filterHouse.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch houses";
      });
  },
});

export const {
  resetFilteredHouse,
  setSearchParams,
  setHousePage,
  resetParams,
  resetHousepage,
} = FilterHouseSlice.actions;

export default FilterHouseSlice.reducer;
