import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { District } from "../../types/location";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";

export interface DistrictState {
  districts: District[];
  loading: boolean;
  error: string | null;
}

const initialState: DistrictState = {
  districts: [],
  loading: false,
  error: null,
};

export const fetchRegionDistrictList = createAsyncThunk<
  District[],
  string,
  { rejectValue: string }
>(
  "district/fetchRegionDistrictList",
  async (region_id: string, { rejectWithValue }) => {
    try {
      const response = await apiClient.get(
        endpoints.districtsByRegion(region_id)
      );
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        return rejectWithValue(
          error.response?.data?.detail || "Failed to fetch districts"
        );
      }
      return rejectWithValue("Failed to fetch districts");
    }
  }
);

const districtSlice = createSlice({
  name: "district",
  initialState,
  reducers: {
    resetDistrictState: (state) => {
      state.districts = [];
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchRegionDistrictList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchRegionDistrictList.fulfilled,
        (state, action: PayloadAction<District[]>) => {
          state.loading = false;
          state.districts = action.payload;
        }
      )
      .addCase(fetchRegionDistrictList.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch districts";
      });
  },
});

export const { resetDistrictState } = districtSlice.actions;

export default districtSlice.reducer;
