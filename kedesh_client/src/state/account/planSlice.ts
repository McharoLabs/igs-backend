import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { PlanType } from "../../types/accountType";

export interface PlanState {
  plans: PlanType[];
  loading: boolean;
  error: string | null;
}

const initialState: PlanState = {
  plans: [],
  loading: false,
  error: null,
};

export const fetchPlanList = createAsyncThunk<
  PlanType[],
  void,
  { rejectValue: string }
>("plan/fetchPlanList", async (_, { rejectWithValue }) => {
  try {
    const response = await apiClient.get(endpoints.plans);
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(
        error.response?.data?.detail || "Failed to fetch Plans"
      );
    }
    return rejectWithValue("Failed to fetch Plans");
  }
});

const PlanSlice = createSlice({
  name: "Plan",
  initialState,
  reducers: {
    resetPlanState: (state) => {
      state.plans = [];
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchPlanList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchPlanList.fulfilled,
        (state, action: PayloadAction<PlanType[]>) => {
          state.loading = false;
          state.plans = action.payload;
        }
      )
      .addCase(fetchPlanList.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch Plans";
      });
  },
});

export const { resetPlanState } = PlanSlice.actions;

export default PlanSlice.reducer;
