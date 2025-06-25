import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { RootState } from "../store";
import { SubscribeSchemaType } from "../../schemas/Subscribe";

export interface SubscribeState {
  detail: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: SubscribeState = {
  detail: null,
  loading: false,
  error: null,
};

export const subscribe = createAsyncThunk<
  string,
  SubscribeSchemaType,
  { rejectValue: string }
>(
  "subscribe/subscribe",
  async ({ plan_id, phone_number }, { rejectWithValue, getState }) => {
    try {
      const formData = new FormData();
      formData.append("plan_id", plan_id);
      formData.append("phone_number", phone_number);
      const token = (getState() as RootState).auth.tokens.access;
      const response = await apiClient.post(endpoints.subscribe, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data.detail;
    } catch (error) {
      if (error instanceof AxiosError) {
        return rejectWithValue(
          error.response?.data?.detail || "Failed to Subscribe"
        );
      }
      return rejectWithValue("Failed to Subscribe");
    }
  }
);

const SubscribeSlice = createSlice({
  name: "Subscribe",
  initialState,
  reducers: {
    resetSubscribe: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(subscribe.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(subscribe.fulfilled, (state, action: PayloadAction<string>) => {
        state.loading = false;
        state.detail = action.payload;
      })
      .addCase(subscribe.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to Subscribe";
      });
  },
});

export const { resetSubscribe } = SubscribeSlice.actions;

export default SubscribeSlice.reducer;
