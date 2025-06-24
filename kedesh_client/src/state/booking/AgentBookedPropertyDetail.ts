import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AxiosError } from "axios";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { RootState } from "../store";
import { Booking } from "../../types/BookingType";

export interface BookedPropertyDetailState {
  bookedProperty: Booking | null;
  loading: boolean;
  error: string | null;
}

const initialState: BookedPropertyDetailState = {
  bookedProperty: null,
  loading: false,
  error: null,
};

export const fetchAgentBookedPropertyDetails = createAsyncThunk<
  Booking,
  { bookingId: string },
  { rejectValue: string }
>(
  "agentBookedPropertyDetails/fetchAgentBookedPropertyDetails",
  async ({ bookingId }, { rejectWithValue, getState }) => {
    try {
      const token = (getState() as RootState).auth.tokens.access;
      const response = await apiClient.get(
        endpoints.agentBookedPropertyDetail(bookingId),
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        return rejectWithValue(
          error.response?.data.detail || "Failed to fetch Booking"
        );
      }
      return rejectWithValue("Failed to fetch Booking");
    }
  }
);

const bookedPropertyDetailsSlice = createSlice({
  name: "agentBookedPropertyDetails",
  initialState: initialState,
  reducers: {
    resetAgentBookedPropertyDetailState: (state) => {
      state.bookedProperty = null;
      state.error = null;
      state.loading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAgentBookedPropertyDetails.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchAgentBookedPropertyDetails.fulfilled,
        (state, action: PayloadAction<Booking>) => {
          state.loading = false;
          state.bookedProperty = action.payload;
        }
      )
      .addCase(fetchAgentBookedPropertyDetails.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch Booking";
      });
  },
});

export const { resetAgentBookedPropertyDetailState } =
  bookedPropertyDetailsSlice.actions;
export default bookedPropertyDetailsSlice.reducer;
