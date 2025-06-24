import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { RootState } from "../store";

export interface MarkPropertySoldState {
  detail: string | null;
  loading: boolean;
  error: string | null;
  statusCode: number | null;
}

const initialState: MarkPropertySoldState = {
  detail: null,
  loading: false,
  error: null,
  statusCode: null,
};

export const markPropertySold = createAsyncThunk<
  { detail: string; statusCode: number },
  { propertyId: string },
  { rejectValue: { error: string; statusCode: number } }
>(
  "markPropertySold/markPropertySold",
  async ({ propertyId }, { rejectWithValue, getState }) => {
    try {
      const token = (getState() as RootState).auth.tokens.access;
      const response = await apiClient.post(
        endpoints.markPropertySold(propertyId),
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
          error: error.response?.data?.detail || "Failed to mark property Sold",
          statusCode: error.response?.status || 500,
        });
      }
      return rejectWithValue({
        error: "Failed to mark property Sold",
        statusCode: 500,
      });
    }
  }
);

const markPropertySoldSlice = createSlice({
  name: "markPropertySold",
  initialState,
  reducers: {
    resetMarkPropertySold: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
      state.statusCode = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(markPropertySold.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.statusCode = null;
      })
      .addCase(
        markPropertySold.fulfilled,
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
        markPropertySold.rejected,
        (
          state,
          action: PayloadAction<
            { error: string; statusCode: number } | undefined
          >
        ) => {
          state.loading = false;
          state.error = action.payload?.error || "Failed to mark property Sold";
          state.statusCode = action.payload?.statusCode || 500;
        }
      );
  },
});

export const { resetMarkPropertySold } = markPropertySoldSlice.actions;

export default markPropertySoldSlice.reducer;
