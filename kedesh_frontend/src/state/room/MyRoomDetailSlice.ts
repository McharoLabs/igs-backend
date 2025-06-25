import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AxiosError } from "axios";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { RootState } from "../store";
import { RoomDetail } from "../../types/RoomType";

export interface RoomState {
  myRoomDetail: RoomDetail | null;
  loading: boolean;
  error: string | null;
}

const initialState: RoomState = {
  myRoomDetail: null,
  loading: false,
  error: null,
};

export const fetchRoomDetail = createAsyncThunk<
  RoomDetail,
  { propertyId: string },
  { rejectValue: string }
>(
  "MyRoomDetail/fetchRoomDetail",
  async ({ propertyId }, { rejectWithValue, getState }) => {
    try {
      const token = (getState() as RootState).auth.tokens.access;
      const response = await apiClient.get(
        endpoints.agentRoomDetail(propertyId),
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
          error.response?.data.detail || "Failed to fetch Room"
        );
      }
      return rejectWithValue("Failed to fetch Room");
    }
  }
);

const MyRoomSlice = createSlice({
  name: "MyRoomDetail",
  initialState: initialState,
  reducers: {
    resetMyRoomDetailState: (state) => {
      state.myRoomDetail = null;
      state.error = null;
      state.loading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchRoomDetail.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchRoomDetail.fulfilled,
        (state, action: PayloadAction<RoomDetail>) => {
          state.loading = false;
          state.myRoomDetail = action.payload;
        }
      )
      .addCase(fetchRoomDetail.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch Room";
      });
  },
});

export const { resetMyRoomDetailState } = MyRoomSlice.actions;
export default MyRoomSlice.reducer;
