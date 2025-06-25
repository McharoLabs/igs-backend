import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { RoomResponse } from "../../types/RoomType";
import { AxiosError } from "axios";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { RootState } from "../store";

export interface RoomState {
  rooms: RoomResponse;
  loading: boolean;
  error: string | null;
}

const initialRoomValue = {
  count: 0,
  next: null,
  previous: null,
  results: [],
};

const initialState: RoomState = {
  rooms: initialRoomValue,
  loading: false,
  error: null,
};

export const fetchRoom = createAsyncThunk<
  RoomResponse,
  void,
  { rejectValue: string }
>("MyRoom/fetchRoom", async (_, { rejectWithValue, getState }) => {
  try {
    const token = (getState() as RootState).auth.tokens.access;
    const response = await apiClient.get(endpoints.roomList, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(
        error.response?.data.detail || "Failed to fetch Room"
      );
    }
    return rejectWithValue("Failed to fetch Room");
  }
});

const MyRoomSlice = createSlice({
  name: "MyRoom",
  initialState: initialState,
  reducers: {
    resetMyRoomState: (state) => {
      state.rooms = initialRoomValue;
      state.error = null;
      state.loading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchRoom.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchRoom.fulfilled,
        (state, action: PayloadAction<RoomResponse>) => {
          state.loading = false;
          state.rooms = action.payload;
        }
      )
      .addCase(fetchRoom.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch Room";
      });
  },
});

export const { resetMyRoomState } = MyRoomSlice.actions;
export default MyRoomSlice.reducer;
