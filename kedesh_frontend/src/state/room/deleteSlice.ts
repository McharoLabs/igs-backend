import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AxiosError } from "axios";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { RootState } from "../store";
import { fetchRoom } from "./MyRoomListSlice";

export interface DeleteRoomState {
  detail: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: DeleteRoomState = {
  detail: null,
  loading: false,
  error: null,
};

export const softDeleteRoom = createAsyncThunk<
  string,
  { propertyId: string },
  { rejectValue: string }
>(
  "DeleteRoom/softDeleteRoom",
  async ({ propertyId }, { rejectWithValue, getState, dispatch }) => {
    try {
      const token = (getState() as RootState).auth.tokens.access;
      const response = await apiClient.delete(
        endpoints.deleteRoom(propertyId),
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 200) {
        dispatch(fetchRoom());
      }

      return response.data.detail;
    } catch (error) {
      console.error(error);
      if (error instanceof AxiosError) {
        return rejectWithValue(
          error.response?.data.detail ||
            "Imeshindwa kufuta kwasababu isiyojulikana, jaribu tena badae"
        );
      }
      return rejectWithValue(
        "Imeshindwa kufuta kwasababu isiyojulikana, jaribu tena badae"
      );
    }
  }
);

const deleteRoomSlice = createSlice({
  name: "DeleteRoom",
  initialState: initialState,
  reducers: {
    resetSoftDeleteRoom: (state) => {
      state.detail = null;
      state.error = null;
      state.loading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(softDeleteRoom.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        softDeleteRoom.fulfilled,
        (state, action: PayloadAction<string>) => {
          state.loading = false;
          state.detail = action.payload;
        }
      )
      .addCase(softDeleteRoom.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload ||
          action.error.message ||
          "Imeshindwa kufuta kwasababu isiyojulikana, jaribu tena badae";
      });
  },
});

export const { resetSoftDeleteRoom } = deleteRoomSlice.actions;
export default deleteRoomSlice.reducer;
