import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { RootState } from "../store";

export interface MarkPropertyAvailableState {
  detail: string | null;
  loading: boolean;
  error: string | null;
  statusCode: number | null;
}

const initialState: MarkPropertyAvailableState = {
  detail: null,
  loading: false,
  error: null,
  statusCode: null,
};

export const markPropertyAvailable = createAsyncThunk<
  { detail: string; statusCode: number },
  { propertyId: string },
  { rejectValue: { error: string; statusCode: number } }
>(
  "markPropertyAvailable/markPropertyAvailable",
  async ({ propertyId }, { rejectWithValue, getState }) => {
    try {
      const token = (getState() as RootState).auth.tokens.access;
      const response = await apiClient.post(
        endpoints.markPropertyAvailable(propertyId),
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
            error.response?.data?.detail || "Failed to mark property available",
          statusCode: error.response?.status || 500,
        });
      }
      return rejectWithValue({
        error: "Failed to mark property available",
        statusCode: 500,
      });
    }
  }
);

const markPropertyAvailableSlice = createSlice({
  name: "markPropertyAvailable",
  initialState,
  reducers: {
    resetMarkPropertyAvailable: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(markPropertyAvailable.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.statusCode = null;
      })
      .addCase(
        markPropertyAvailable.fulfilled,
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
        markPropertyAvailable.rejected,
        (
          state,
          action: PayloadAction<
            { error: string; statusCode: number } | undefined
          >
        ) => {
          state.loading = false;
          state.error =
            action.payload?.error || "Failed to mark property available";
          state.statusCode = action.payload?.statusCode || 500;
        }
      );
  },
});

export const { resetMarkPropertyAvailable } =
  markPropertyAvailableSlice.actions;

export default markPropertyAvailableSlice.reducer;
