import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { Street } from "../../types/location";

export interface StreetState {
  streets: Street[];
  loading: boolean;
  error: string | null;
}

const initialState: StreetState = {
  streets: [],
  loading: false,
  error: null,
};

export const fetchWardStreetList = createAsyncThunk<
  Street[],
  string,
  { rejectValue: string }
>(
  "street/fetchWardStreetList",
  async (ward_id: string, { rejectWithValue }) => {
    try {
      const response = await apiClient.get(endpoints.streetByWard(ward_id));
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        return rejectWithValue(
          error.response?.data?.detail || "Failed to fetch Streets"
        );
      }
      return rejectWithValue("Failed to fetch Streets");
    }
  }
);

const streetSlice = createSlice({
  name: "street",
  initialState,
  reducers: {
    resetStreetState: (state) => {
      state.streets = [];
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchWardStreetList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchWardStreetList.fulfilled,
        (state, action: PayloadAction<Street[]>) => {
          state.loading = false;
          state.streets = action.payload;
        }
      )
      .addCase(fetchWardStreetList.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch Streets";
      });
  },
});

export const { resetStreetState } = streetSlice.actions;

export default streetSlice.reducer;
