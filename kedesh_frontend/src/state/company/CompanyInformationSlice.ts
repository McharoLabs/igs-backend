import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { SiteSettings } from "../../types/companyType";

export interface CompanyInformationState {
  companyInformations: SiteSettings | null;
  loading: boolean;
  error: string | null;
}

const initialState: CompanyInformationState = {
  companyInformations: null,
  loading: false,
  error: null,
};

export const fetchCompanyInformation = createAsyncThunk<
  SiteSettings,
  void,
  { rejectValue: string }
>(
  "CompanyInformation/fetchCompanyInformation",
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiClient.get(endpoints.companyInformation);
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        return rejectWithValue(
          error.response?.data?.detail || "Failed to fetch CompanyInformations"
        );
      }
      return rejectWithValue("Failed to fetch CompanyInformations");
    }
  }
);

const companyInformationSlice = createSlice({
  name: "companyInformation",
  initialState,
  reducers: {
    resetCompanyInformationState: (state) => {
      state.companyInformations = null;
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchCompanyInformation.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchCompanyInformation.fulfilled,
        (state, action: PayloadAction<SiteSettings>) => {
          state.loading = false;
          state.companyInformations = action.payload;
        }
      )
      .addCase(fetchCompanyInformation.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload ||
          action.error.message ||
          "Failed to fetch CompanyInformations";
      });
  },
});

export const { resetCompanyInformationState } = companyInformationSlice.actions;

export default companyInformationSlice.reducer;
