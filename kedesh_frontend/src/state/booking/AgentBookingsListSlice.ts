import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AxiosError } from "axios";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { RootState } from "../store";
import { BookingResponse } from "../../types/BookingType";

export interface BookingListState {
  bookingLists: BookingResponse;
  loading: boolean;
  error: string | null;
}

const initialBookingListValue = {
  count: 0,
  next: null,
  previous: null,
  results: [],
};

const initialState: BookingListState = {
  bookingLists: initialBookingListValue,
  loading: false,
  error: null,
};

export const fetchAgentBookingList = createAsyncThunk<
  BookingResponse,
  { customerName: string },
  { rejectValue: string }
>(
  "agentBookingList/fetchAgentBookingList",
  async ({ customerName }, { rejectWithValue, getState }) => {
    try {
      const token = (getState() as RootState).auth.tokens.access;
      const response = await apiClient.get(
        endpoints.agentBookingList(customerName),
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
          error.response?.data.detail || "Failed to fetch BookingList"
        );
      }
      return rejectWithValue("Failed to fetch BookingList");
    }
  }
);

const BookingListSlice = createSlice({
  name: "agentBookingList",
  initialState: initialState,
  reducers: {
    resetAgentBookingListState: (state) => {
      state.bookingLists = initialBookingListValue;
      state.error = null;
      state.loading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAgentBookingList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchAgentBookingList.fulfilled,
        (state, action: PayloadAction<BookingResponse>) => {
          state.loading = false;
          state.bookingLists = action.payload;
        }
      )
      .addCase(fetchAgentBookingList.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload ||
          action.error.message ||
          "Failed to fetch BookingList";
      });
  },
});

export const { resetAgentBookingListState } = BookingListSlice.actions;
export default BookingListSlice.reducer;
