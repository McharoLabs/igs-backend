import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { RootState } from "../store";
import { UploadImagesSchemaType } from "../../schemas/UplaodImagesSchema";
import { fetchHouse } from "./myHouseSlice";

export interface UploadHouseImageState {
  detail: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: UploadHouseImageState = {
  detail: null,
  loading: false,
  error: null,
};

export const uploadHouseImages = createAsyncThunk<
  string,
  UploadImagesSchemaType,
  { rejectValue: string }
>(
  "uplaodImages/uploadHouseImages",
  async (data, { rejectWithValue, getState, dispatch }) => {
    try {
      const token = (getState() as RootState).auth.tokens.access;

      const formData = new FormData();
      formData.append("property_id", data.property_id);

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

      const response = await apiClient.post(
        endpoints.uploadHouseImages,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (response.status === 200) {
        dispatch(fetchHouse());
      }

      return response.data.detail;
    } catch (error) {
      if (error instanceof AxiosError) {
        return rejectWithValue(error.response?.data?.detail);
      }
      return rejectWithValue("Failed to submit images");
    }
  }
);

const UploadHouseImageSlice = createSlice({
  name: "uplaodImages",
  initialState,
  reducers: {
    resetUploadImagesState: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(uploadHouseImages.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        uploadHouseImages.fulfilled,
        (state, action: PayloadAction<string>) => {
          state.loading = false;
          state.detail = action.payload;
        }
      )
      .addCase(uploadHouseImages.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to upload images";
      });
  },
});

export const { resetUploadImagesState } = UploadHouseImageSlice.actions;

export default UploadHouseImageSlice.reducer;
