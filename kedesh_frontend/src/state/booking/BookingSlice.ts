import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { BookingType } from "../../schemas/BookingSchema";

export interface BookingState {
  detail: string | null;
  loading: boolean;
  error: string | null;
  statusCode: number | null;
}

const initialState: BookingState = {
  detail: null,
  loading: false,
  error: null,
  statusCode: null,
};

export const bookingOrder = createAsyncThunk<
  { detail: string; statusCode: number },
  BookingType,
  { rejectValue: { error: string; statusCode: number } }
>("bookingOrder/bookingOrder", async (data, { rejectWithValue }) => {
  try {
    const formData = new FormData();
    formData.append("property_id", data.property_id);
    formData.append("customer_name", data.customer_name);
    formData.append("customer_email", data.customer_email);
    formData.append("phone_number", data.customer_phone);

    const response = await apiClient.post(
      endpoints.requestAgentPhoneNumber,
      formData
    );
    return { detail: response.data.detail, statusCode: response.status };
  } catch (error) {
    console.error(error);
    if (error instanceof AxiosError) {
      return rejectWithValue({
        error: error.response?.data?.detail || "Failed to add Booking",
        statusCode: error.response?.status || 500,
      });
    }
    return rejectWithValue({
      error: "Failed to submit Booking",
      statusCode: 500,
    });
  }
});

const BookingSlice = createSlice({
  name: "bookingOrder",
  initialState,
  reducers: {
    resetbookingOrderState: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
      state.statusCode = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(bookingOrder.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.statusCode = null;
      })
      .addCase(
        bookingOrder.fulfilled,
        (
          state,
          action: PayloadAction<{ detail: string; statusCode: number }>
        ) => {
          state.loading = false;
          state.detail = action.payload.detail;
          state.statusCode = action.payload.statusCode;
        }
      )
      .addCase(
        bookingOrder.rejected,
        (
          state,
          action: PayloadAction<
            { error: string; statusCode: number } | undefined
          >
        ) => {
          state.loading = false;
          state.error = action.payload?.error || "Failed to add Booking";
          state.statusCode = action.payload?.statusCode || 500;
        }
      );
  },
});

export const { resetbookingOrderState } = BookingSlice.actions;

export default BookingSlice.reducer;
