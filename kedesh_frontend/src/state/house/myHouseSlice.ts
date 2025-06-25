import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { HouseResponse } from "../../types/houseType";
import { AxiosError } from "axios";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { RootState } from "../store";

export interface HouseState {
  houses: HouseResponse;
  loading: boolean;
  error: string | null;
}

const initialHouseValue = {
  count: 0,
  next: null,
  previous: null,
  results: [],
};

const initialState: HouseState = {
  houses: initialHouseValue,
  loading: false,
  error: null,
};

export const fetchHouse = createAsyncThunk<
  HouseResponse,
  void,
  { rejectValue: string }
>("MyHouse/fetchHouse", async (_, { rejectWithValue, getState }) => {
  try {
    const token = (getState() as RootState).auth.tokens.access;
    const response = await apiClient.get(endpoints.houseList, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(
        error.response?.data.detail || "Failed to fetch house"
      );
    }
    return rejectWithValue("Failed to fetch house");
  }
});

const MyHouseSlice = createSlice({
  name: "MyHouse",
  initialState: initialState,
  reducers: {
    resetMyHouseState: (state) => {
      state.houses = initialHouseValue;
      state.error = null;
      state.loading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchHouse.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchHouse.fulfilled,
        (state, action: PayloadAction<HouseResponse>) => {
          state.loading = false;
          state.houses = action.payload;
        }
      )
      .addCase(fetchHouse.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch house";
      });
  },
});

export const { resetMyHouseState } = MyHouseSlice.actions;
export default MyHouseSlice.reducer;
