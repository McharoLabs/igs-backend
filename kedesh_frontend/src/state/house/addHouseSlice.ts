import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { HouseSchemaType } from "../../schemas/AddHouseSchema";
import { RootState } from "../store";

export interface HouseState {
  detail: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: HouseState = {
  detail: null,
  loading: false,
  error: null,
};

export const addHouse = createAsyncThunk<
  string,
  HouseSchemaType,
  { rejectValue: string }
>("addHouse/addHouse", async (data, { rejectWithValue, getState }) => {
  try {
    const token = (getState() as RootState).auth.tokens.access;

    const formData = new FormData();
    formData.append(
      "rental_duration",
      data.rental_duration === undefined ? "" : String(data.rental_duration)
    );
    formData.append("category", data.category);
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
    formData.append("total_bed_room", String(data.total_bed_room));
    formData.append("total_dining_room", String(data.total_dining_room));
    formData.append("total_bath_room", String(data.total_bath_room));
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
      return rejectWithValue("No images provided");
    }

    Array.from(data.images).forEach((image) => {
      if (image instanceof File) {
        formData.append("images", image);
      } else {
        console.error("Not a valid file:", image);
      }
    });

    const response = await apiClient.post(endpoints.addHouse, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data.detail;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data?.detail);
    }
    return rejectWithValue("Failed to submit house");
  }
});

const houseSlice = createSlice({
  name: "addHouse",
  initialState,
  reducers: {
    resetAddHouseState: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(addHouse.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addHouse.fulfilled, (state, action: PayloadAction<string>) => {
        state.loading = false;
        state.detail = action.payload;
      })
      .addCase(addHouse.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to add house";
      });
  },
});

export const { resetAddHouseState } = houseSlice.actions;

export default houseSlice.reducer;
