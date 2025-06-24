import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AxiosError } from "axios";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { RoomDetail } from "../../types/RoomType";

export interface ClientRoomState {
  room: RoomDetail | null;
  loading: boolean;
  error: string | null;
}

const initialState: ClientRoomState = {
  room: null,
  loading: false,
  error: null,
};

export const fetchClientRoomDetail = createAsyncThunk<
  RoomDetail,
  { propertyId: string },
  { rejectValue: string }
>(
  "ClientRoomDetail/fetchClientRoomDetail",
  async ({ propertyId }, { rejectWithValue }) => {
    try {
      const response = await apiClient.get(
        endpoints.clientRoomDetail(propertyId),
      );
      return response.data;
    } catch (error) {
      console.error(error);
      if (error instanceof AxiosError) {
        return rejectWithValue(
          error.response?.data.detail || "Failed to fetch ClientRoom"
        );
      }
      return rejectWithValue("Failed to fetch ClientRoom");
    }
  }
);

const MyClientRoomSlice = createSlice({
  name: "ClientRoomDetail",
  initialState: initialState,
  reducers: {
    resetClientRoomState: (state) => {
      state.room = null;
      state.error = null;
      state.loading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchClientRoomDetail.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchClientRoomDetail.fulfilled,
        (state, action: PayloadAction<RoomDetail>) => {
          state.loading = false;
          state.room = action.payload;
        }
      )
      .addCase(fetchClientRoomDetail.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload ||
          action.error.message ||
          "Failed to fetch ClientRoom";
      });
  },
});

export const { resetClientRoomState } = MyClientRoomSlice.actions;
export default MyClientRoomSlice.reducer;
