import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AxiosError } from "axios";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { RootState } from "../store";
import { HouseDetail } from "../../types/houseType";

export interface HouseState {
  myHouseDetail: HouseDetail | null;
  loading: boolean;
  error: string | null;
}

const initialState: HouseState = {
  myHouseDetail: null,
  loading: false,
  error: null,
};

export const fetchHouseDetail = createAsyncThunk<
  HouseDetail,
  { propertyId: string },
  { rejectValue: string }
>(
  "MyHouseDetail/fetchHouseDetail",
  async ({ propertyId }, { rejectWithValue, getState }) => {
    try {
      const token = (getState() as RootState).auth.tokens.access;
      const response = await apiClient.get(
        endpoints.myHouseDetail(propertyId),
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error(error);
      if (error instanceof AxiosError) {
        return rejectWithValue(
          error.response?.data.detail || "Failed to fetch house"
        );
      }
      return rejectWithValue("Failed to fetch house");
    }
  }
);

const MyHouseSlice = createSlice({
  name: "MyHouseDetail",
  initialState: initialState,
  reducers: {
    resetMyHouseDetailState: (state) => {
      state.myHouseDetail = null;
      state.error = null;
      state.loading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchHouseDetail.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchHouseDetail.fulfilled,
        (state, action: PayloadAction<HouseDetail>) => {
          state.loading = false;
          state.myHouseDetail = action.payload;
        }
      )
      .addCase(fetchHouseDetail.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch house";
      });
  },
});

export const { resetMyHouseDetailState } = MyHouseSlice.actions;
export default MyHouseSlice.reducer;
