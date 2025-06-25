import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { LandListResponse } from "../../types/landType";
import { RootState } from "../store";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { LAND_TYPE } from "../../types/enums";

interface SearchParamsType {
  region: string | null;
  district: string | null;
  minPrice: string | null;
  maxPrice: string | null;
  ward: string | null;
  street: string | null;
  page: string | null;
  category: LAND_TYPE | null;
}
export interface LandFilterState {
  searchParams: SearchParamsType;
  filteredLands: LandListResponse | null;
  detail: string | null;
  loading: boolean;
  error: string | null;
}

const initializeSearchParams: SearchParamsType = {
  region: null,
  district: null,
  minPrice: null,
  maxPrice: null,
  ward: null,
  street: null,
  page: null,
  category: null,
};

export const fetchFilteredLands = createAsyncThunk<
  LandListResponse,
  void,
  { rejectValue: string }
>("landFilter/fetchFilteredLands", async (_, { rejectWithValue, getState }) => {
  try {
    const state = getState() as RootState;
    const data = state.landFilter.searchParams;

    const params = new URLSearchParams();
    if (data.region) params.append("region", data.region);
    if (data.district) params.append("district", data.district);
    if (data.ward) params.append("ward", data.ward);
    if (data.street) params.append("street", data.street);
    if (data.minPrice) params.append("minPrice", data.minPrice);
    if (data.maxPrice) params.append("maxPrice", data.maxPrice);
    if (data.page) params.append("page", data.page);
    if (data.category) params.append("category", data.category);

    const response = await apiClient.get(endpoints.fetchFilteredLand(), {
      params,
    });

    console.log(response.data);
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data.detail);
    } else {
      return rejectWithValue(String(error));
    }
  }
});

const landFilterSlice = createSlice({
  name: "landFilter",
  initialState: {
    searchParams: initializeSearchParams,
    filteredLands: null,
    detail: null,
    loading: false,
    error: null,
  } as LandFilterState,
  reducers: {
    setLandSearchParams: (
      state,
      action: PayloadAction<Partial<SearchParamsType>>
    ) => {
      state.searchParams = {
        ...state.searchParams,
        ...action.payload,
      };
    },
    setLandPage: (state, action: PayloadAction<string | null>) => {
      state.searchParams.page = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchFilteredLands.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchFilteredLands.fulfilled,
        (state, action: { payload: LandListResponse }) => {
          state.loading = false;
          state.filteredLands = action.payload;
        }
      )
      .addCase(fetchFilteredLands.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setLandSearchParams, setLandPage } = landFilterSlice.actions;
export default landFilterSlice.reducer;
