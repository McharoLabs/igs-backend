import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import {
  LandFormSchemaType,
  RequestAgentContactSchemaType,
} from "../../schemas/LandSchema";
import { RootState } from "../store";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { LandListResponse, LandResponse } from "../../types/landType";

interface LandState {
  detail: string | null;
  loading: boolean;
  error: string | null;
  landList: LandListResponse | null;
  land: LandResponse | null;
  landDetails: LandResponse | null;
}

const initialState: LandState = {
  detail: null,
  loading: false,
  error: null,
  landList: null,
  land: null,
  landDetails: null,
};

export const addLand = createAsyncThunk<
  string,
  LandFormSchemaType,
  { rejectValue: string }
>("land/addLand", async (data, { rejectWithValue, getState }) => {
  try {
    const token = (getState() as RootState).auth.tokens.access;

    const formData = new FormData();
    formData.append("description", String(data.description));
    formData.append("price", String(data.price));
    formData.append("land_size_unit", data.land_size_unit);
    formData.append("category", data.category);
    formData.append("land_size", String(data.land_size));
    formData.append("access_road_type", data.access_road_type);
    formData.append("zoning_type", data.zoning_type);
    formData.append("utilities", String(data.utilities));
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

    const response = await apiClient.post(endpoints.addLand(), formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data.detail;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data.detail);
    } else {
      return rejectWithValue("An unknown error occurred");
    }
  }
});

export const fetchLandList = createAsyncThunk<
  LandListResponse,
  void,
  { rejectValue: string }
>("land/fetchLandList", async (_, { rejectWithValue, getState }) => {
  try {
    const token = (getState() as RootState).auth.tokens.access;

    const response = await apiClient.get(endpoints.landList, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data.detail);
    } else {
      return rejectWithValue("An unknown error occurred");
    }
  }
});

export const fetchAgentLand = createAsyncThunk<
  LandResponse,
  { landId: string },
  { rejectValue: string }
>("land/fetchAgentLand", async ({ landId }, { rejectWithValue, getState }) => {
  try {
    const token = (getState() as RootState).auth.tokens.access;

    const response = await apiClient.get(endpoints.fetchAgentLand(landId), {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data.detail);
    } else {
      return rejectWithValue("An unknown error occurred");
    }
  }
});

export const fetchLandDetails = createAsyncThunk<
  LandResponse,
  { landId: string },
  { rejectValue: string }
>("land/fetchLandDetails", async ({ landId }, { rejectWithValue }) => {
  try {
    const response = await apiClient.get(endpoints.fetchLandDetails(landId));
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data.detail);
    } else {
      return rejectWithValue("An unknown error occurred");
    }
  }
});

export const requestAgentLandPhoneNumber = createAsyncThunk<
  string,
  RequestAgentContactSchemaType,
  { rejectValue: string }
>("land/requestAgentLandPhoneNumber", async (data, { rejectWithValue }) => {
  try {
    const response = await apiClient.post(
      endpoints.requestAgentLandPhoneNumber(),
      {
        customer_name: data.customer_name,
        customer_email: data.customer_email,
        land_id: data.land_id,
        phone_number: data.customer_phone,
      }
    );
    return response.data.detail;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data.detail);
    } else {
      return rejectWithValue("An unknown error occurred");
    }
  }
});

export const deleteLand = createAsyncThunk<
  string,
  { landId: string },
  { rejectValue: string }
>("land/deleteLand", async ({ landId }, { rejectWithValue, getState }) => {
  try {
    const token = (getState() as RootState).auth.tokens.access;
    const response = await apiClient.delete(endpoints.deleteLand(landId), {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data.detail;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data.detail);
    } else {
      return rejectWithValue("An unknown error occurred");
    }
  }
});

const landSlice = createSlice({
  name: "land",
  initialState,
  reducers: {
    resetLandState: (state) => {
      state.detail = null;
      state.loading = false;
      state.error = null;
      state.land = null;
      state.landDetails = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(addLand.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addLand.fulfilled, (state, action: PayloadAction<string>) => {
        state.loading = false;
        state.detail = action.payload;
      })
      .addCase(addLand.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Failed to add land";
      })
      .addCase(fetchLandList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchLandList.fulfilled,
        (state, action: PayloadAction<LandListResponse>) => {
          state.loading = false;
          state.landList = action.payload;
        }
      )
      .addCase(fetchLandList.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Failed to fetch land list";
      })
      .addCase(fetchAgentLand.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchAgentLand.fulfilled,
        (state, action: PayloadAction<LandResponse>) => {
          state.loading = false;
          state.land = action.payload;
        }
      )
      .addCase(fetchAgentLand.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Failed to fetch land";
      })
      .addCase(deleteLand.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteLand.fulfilled, (state, action: PayloadAction<string>) => {
        state.loading = false;
        state.detail = action.payload;
      })
      .addCase(deleteLand.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Failed to delete land";
      })
      .addCase(fetchLandDetails.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchLandDetails.fulfilled,
        (state, action: PayloadAction<LandResponse>) => {
          state.loading = false;
          state.landDetails = action.payload;
        }
      )
      .addCase(fetchLandDetails.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Failed to delete land";
      })
      .addCase(requestAgentLandPhoneNumber.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.detail = null;
      })
      .addCase(
        requestAgentLandPhoneNumber.fulfilled,
        (state, action: PayloadAction<string>) => {
          state.loading = false;
          state.detail = action.payload;
        }
      )
      .addCase(requestAgentLandPhoneNumber.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Failed get agent phone number";
      });
  },
});

export const { resetLandState } = landSlice.actions;
export default landSlice.reducer;
