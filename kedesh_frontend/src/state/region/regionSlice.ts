import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Region } from "../../types/location";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";

export interface RegionState {
  regions: Region[];
  loading: boolean;
  error: string | null;
}

const initialState: RegionState = {
  regions: [],
  loading: false,
  error: null,
};

export const fetchRegionList = createAsyncThunk<
  Region[],
  void,
  { rejectValue: string }
>("region/fetchRegionList", async (_, { rejectWithValue }) => {
  try {
    const response = await apiClient.get(endpoints.regions);
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(
        error.response?.data?.detail || "Failed to fetch regions"
      );
    }
    return rejectWithValue("Failed to fetch regions");
  }
});

const regionSlice = createSlice({
  name: "region",
  initialState,
  reducers: {
    resetRegionState: (state) => {
      state.regions = [];
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchRegionList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchRegionList.fulfilled,
        (state, action: PayloadAction<Region[]>) => {
          state.loading = false;
          state.regions = action.payload;
        }
      )
      .addCase(fetchRegionList.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch regions";
      });
  },
});

export const { resetRegionState } = regionSlice.actions;

export default regionSlice.reducer;
