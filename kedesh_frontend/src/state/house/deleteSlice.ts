import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AxiosError } from "axios";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { RootState } from "../store";
import { fetchHouse } from "./myHouseSlice";

export interface DeleteHouseState {
  detail: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: DeleteHouseState = {
  detail: null,
  loading: false,
  error: null,
};

export const softDeleteHouse = createAsyncThunk<
  string,
  { propertyId: string },
  { rejectValue: string }
>(
  "DeleteHouse/softDeleteHouse",
  async ({ propertyId }, { rejectWithValue, getState, dispatch }) => {
    try {
      const token = (getState() as RootState).auth.tokens.access;
      const response = await apiClient.delete(
        endpoints.deleteHouse(propertyId),
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 200) {
        dispatch(fetchHouse());
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

const deleteHouseSlice = createSlice({
  name: "DeleteHouse",
  initialState: initialState,
  reducers: {
    resetSoftDeleteHouse: (state) => {
      state.detail = null;
      state.error = null;
      state.loading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(softDeleteHouse.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        softDeleteHouse.fulfilled,
        (state, action: PayloadAction<string>) => {
          state.loading = false;
          state.detail = action.payload;
        }
      )
      .addCase(softDeleteHouse.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload ||
          action.error.message ||
          "Imeshindwa kufuta kwasababu isiyojulikana, jaribu tena badae";
      });
  },
});

export const { resetSoftDeleteHouse } = deleteHouseSlice.actions;
export default deleteHouseSlice.reducer;
