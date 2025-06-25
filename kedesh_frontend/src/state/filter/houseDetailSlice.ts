import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AxiosError } from "axios";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { HouseDetail } from "../../types/houseType";

export interface ClientHouseState {
  house: HouseDetail | null;
  loading: boolean;
  error: string | null;
}

const initialState: ClientHouseState = {
  house: null,
  loading: false,
  error: null,
};

export const fetchClientHouseDetail = createAsyncThunk<
  HouseDetail,
  { propertyId: string },
  { rejectValue: string }
>(
  "ClientHouseDetail/fetchClientHouseDetail",
  async ({ propertyId }, { rejectWithValue }) => {
    try {
      const response = await apiClient.get(
        endpoints.clientHouseDetail(propertyId),
      );
      return response.data;
    } catch (error) {
      console.error(error);
      if (error instanceof AxiosError) {
        return rejectWithValue(
          error.response?.data.detail || "Failed to fetch ClientHouse"
        );
      }
      return rejectWithValue("Failed to fetch ClientHouse");
    }
  }
);

const MyClientHouseSlice = createSlice({
  name: "ClientHouseDetail",
  initialState: initialState,
  reducers: {
    resetClientHouseState: (state) => {
      state.house = null;
      state.error = null;
      state.loading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchClientHouseDetail.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchClientHouseDetail.fulfilled,
        (state, action: PayloadAction<HouseDetail>) => {
          state.loading = false;
          state.house = action.payload;
        }
      )
      .addCase(fetchClientHouseDetail.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload ||
          action.error.message ||
          "Failed to fetch ClientHouse";
      });
  },
});

export const { resetClientHouseState } = MyClientHouseSlice.actions;
export default MyClientHouseSlice.reducer;
