import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { AxiosError } from "axios";
import { AccountType } from "../../types/accountType";
import { RootState } from "../store";

export interface AccountState {
  account: AccountType | null;
  showMessage: boolean;
  loading: boolean;
  error: string | null;
}

const initialState: AccountState = {
  account: null,
  loading: false,
  error: null,
  showMessage: false,
};

export const fetchAccount = createAsyncThunk<
  AccountType,
  void,
  { rejectValue: string }
>("account/fetchAccount", async (_, { rejectWithValue, getState }) => {
  try {
    const token = (getState() as RootState).auth.tokens.access;
    const response = await apiClient.get(endpoints.account, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(
        error.response?.data?.detail || "Failed to fetch Account"
      );
    }
    return rejectWithValue("Failed to fetch Account");
  }
});

const AccountSlice = createSlice({
  name: "Account",
  initialState,
  reducers: {
    resetAccount: (state) => {
      state.account = null;
      state.loading = false;
      state.error = null;
    },
    hideAccountMessage: (state) => {
      state.showMessage = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAccount.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchAccount.fulfilled,
        (state, action: PayloadAction<AccountType>) => {
          state.loading = false;
          state.account = action.payload;

          if (Number(action.payload.plan.price) === 0) {
            state.showMessage = true;
          }
        }
      )
      .addCase(fetchAccount.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload || action.error.message || "Failed to fetch Account";
      });
  },
});

export const { resetAccount, hideAccountMessage } = AccountSlice.actions;

export default AccountSlice.reducer;
