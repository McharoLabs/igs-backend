import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { RootState } from "../store";

export interface MarkPropertyRentedState {
  detail: string | null;
  loading: boolean;
  error: string | null;
  statusCode: number | null;
}

const initialState: MarkPropertyRentedState = {
  detail: null,
  loading: false,
  error: null,
  statusCode: null,
};

export const markPropertyRented = createAsyncThunk<
  { detail: string; statusCode: number },
  { propertyId: string },
  { rejectValue: { error: string; statusCode: number } }
>(
  "markPropertyRented/markPropertyRented",
  async ({ propertyId }, { rejectWithValue, getState }) => {
    try {
      const token = (getState() as RootState).auth.tokens.access;
      const response = await apiClient.post(
        endpoints.markPropertyRented(propertyId),
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      return { detail: response.data.detail, statusCode: response.status };
    } catch (error) {
      if (error instanceof AxiosError) {
        return rejectWithValue({
          error:
            error.response?.data?.detail || "Failed to mark property Rented",
          statusCode: error.response?.status || 500,
        });
      }
      return rejectWithValue({
        error: "Failed to mark property Rented",
        statusCode: 500,
      });
    }
  }
);

const markPropertyRentedSlice = createSlice({
  name: "markPropertyRented",
  initialState,
  reducers: {
    resetMarkPropertyRented: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
      state.statusCode = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(markPropertyRented.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.statusCode = null;
      })
      .addCase(
        markPropertyRented.fulfilled,
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
        markPropertyRented.rejected,
        (
          state,
          action: PayloadAction<
            { error: string; statusCode: number } | undefined
          >
        ) => {
          state.loading = false;
          state.error =
            action.payload?.error || "Failed to mark property Rented";
          state.statusCode = action.payload?.statusCode || 500;
        }
      );
  },
});

export const { resetMarkPropertyRented } = markPropertyRentedSlice.actions;

export default markPropertyRentedSlice.reducer;
