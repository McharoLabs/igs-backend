import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { PropertyResponse } from "../../types/PropertyType";

export interface DemoPropertyState {
  demoProperties: PropertyResponse;
  detail: string | null;
  loading: boolean;
  error: string | null;
}

const initializeFilteredResponse: PropertyResponse = {
  count: 0,
  next: null,
  previous: null,
  results: [],
};

const initialState: DemoPropertyState = {
  demoProperties: initializeFilteredResponse,
  detail: null,
  loading: false,
  error: null,
};

export const fetchDemoroperties = createAsyncThunk<
  PropertyResponse,
  void,
  { rejectValue: string }
>("demoProperties/fetchDemoroperties", async (_, { rejectWithValue }) => {
  try {
    const response = await apiClient.get(endpoints.demoProperties);

    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data?.detail);
    }
    return rejectWithValue("Failed to fetch demo properties");
  }
});

const demoPropertySlice = createSlice({
  name: "demoProperties",
  initialState,
  reducers: {
    resetDemoProperties: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDemoroperties.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchDemoroperties.fulfilled,
        (state, action: PayloadAction<PropertyResponse>) => {
          state.loading = false;
          state.demoProperties = action.payload;
        }
      )
      .addCase(fetchDemoroperties.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch Propertys";
      });
  },
});

export const { resetDemoProperties } = demoPropertySlice.actions;

export default demoPropertySlice.reducer;
