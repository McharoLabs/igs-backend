import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { Ward } from "../../types/location";

export interface WardState {
  wards: Ward[];
  loading: boolean;
  error: string | null;
}

const initialState: WardState = {
  wards: [],
  loading: false,
  error: null,
};

export const fetchDistrictWardList = createAsyncThunk<
  Ward[],
  string,
  { rejectValue: string }
>(
  "ward/fetchDistrictWardList",
  async (district_id: string, { rejectWithValue }) => {
    try {
      const response = await apiClient.get(
        endpoints.wardByDistrict(district_id)
      );
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        return rejectWithValue(
          error.response?.data?.detail || "Failed to fetch Wards"
        );
      }
      return rejectWithValue("Failed to fetch Wards");
    }
  }
);

const wardSlice = createSlice({
  name: "ward",
  initialState,
  reducers: {
    resetWardState: (state) => {
      state.wards = [];
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDistrictWardList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchDistrictWardList.fulfilled,
        (state, action: PayloadAction<Ward[]>) => {
          state.loading = false;
          state.wards = action.payload;
        }
      )
      .addCase(fetchDistrictWardList.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch Wards";
      });
  },
});

export const { resetWardState } = wardSlice.actions;

export default wardSlice.reducer;
