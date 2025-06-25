import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { RootState } from "../store";
import { RoomSchemaType } from "../../schemas/RoomShema";

export interface RoomState {
  detail: string | null;
  loading: boolean;
  error: string | null;
  statusCode: number | null;
}

const initialState: RoomState = {
  detail: null,
  loading: false,
  error: null,
  statusCode: null,
};

export const addRoom = createAsyncThunk<
  { detail: string; statusCode: number },
  RoomSchemaType,
  { rejectValue: { error: string; statusCode: number } }
>("addRoom/addRoom", async (data, { rejectWithValue, getState }) => {
  try {
    const token = (getState() as RootState).auth.tokens.access;

    const formData = new FormData();
    formData.append("rental_duration", String(data.rental_duration));
    formData.append("room_category", data.room_category);
    formData.append("description", String(data.description));
    formData.append("price", String(data.price));
    formData.append("condition", String(data.condition));
    formData.append("nearby_facilities", String(data.nearby_facilities));
    formData.append("utilities", String(data.utilities));
    formData.append("security_features", String(data.security_features));
    formData.append(
      "heating_cooling_system",
      String(data.heating_cooling_system)
    );
    formData.append("furnishing_status", String(data.furnishing_status));
    formData.append("district_id", String(data.district));
    formData.append("ward", String(data.ward));
    formData.append("street", String(data.street));
    formData.append(
      "latitude",
      String(parseFloat(String(data.latitude)).toFixed(8))
    );
    formData.append(
      "longitude",
      String(parseFloat(String(data.longitude)).toFixed(8))
    );

    const images = data.images;

    if (!images || images.length === 0) {
      return rejectWithValue({ error: "No images provided", statusCode: 400 });
    }

    Array.from(data.images).forEach((image) => {
      if (image instanceof File) {
        formData.append("images", image);
      } else {
        console.error("Not a valid file:", image);
      }
    });

    const response = await apiClient.post(endpoints.addRoom, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "multipart/form-data",
      },
    });

    return { detail: response.data.detail, statusCode: response.status };
  } catch (error) {
    console.error(error);
    if (error instanceof AxiosError) {
      return rejectWithValue({
        error: error.response?.data?.detail || "Failed to add Room",
        statusCode: error.response?.status || 500,
      });
    }
    return rejectWithValue({ error: "Failed to submit Room", statusCode: 500 });
  }
});

const RoomSlice = createSlice({
  name: "addRoom",
  initialState,
  reducers: {
    resetAddRoomState: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
      state.statusCode = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(addRoom.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.statusCode = null;
      })
      .addCase(
        addRoom.fulfilled,
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
        addRoom.rejected,
        (
          state,
          action: PayloadAction<
            { error: string; statusCode: number } | undefined
          >
        ) => {
          state.loading = false;
          state.error = action.payload?.error || "Failed to add Room";
          state.statusCode = action.payload?.statusCode || 500;
        }
      );
  },
});

export const { resetAddRoomState } = RoomSlice.actions;

export default RoomSlice.reducer;
