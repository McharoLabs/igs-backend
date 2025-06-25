import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { RegistrationFormData } from "../../schemas/registrationSchema";
import { AxiosError } from "axios";

interface RegistrationState {
  loading: boolean;
  error: string | null;
  success: boolean;
  detail: string | null;
}

const agentRegistrationEndpoint = endpoints.agentRegistration;

export const registerAgent = createAsyncThunk<
  string,
  RegistrationFormData,
  { rejectValue: string }
>("auth/registerAgent", async (formData, { rejectWithValue }) => {
  try {
    const data = new FormData();

    data.append("first_name", formData.first_name);
    data.append("middle_name", formData.middle_name || "");
    data.append("last_name", formData.last_name);
    data.append("gender", formData.gender);
    data.append("phone_number", formData.phone_number);
    data.append("email", formData.email);
    data.append("password", formData.password);

    if (formData.avatar && formData.avatar[0]) {
      data.append("avatar", formData.avatar[0]);
    }

    const response = await apiClient.post(agentRegistrationEndpoint, data, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data.detail;
  } catch (error) {
    if (error instanceof AxiosError) {
      return rejectWithValue(error.response?.data?.detail);
    }
    return rejectWithValue(
      "Registration failed, please try again later or contact support team"
    );
  }
});

const initialState: RegistrationState = {
  loading: false,
  error: null,
  success: false,
  detail: null,
};

const registrationSlice = createSlice({
  name: "registration",
  initialState,
  reducers: {
    resetRegistrationState: (state) => {
      state.loading = false;
      state.error = null;
      state.success = false;
      state.detail = null;
    },
  },
  extraReducers: (builder) => {
    // Handle registration for Agent
    builder
      .addCase(registerAgent.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.success = false;
      })
      .addCase(
        registerAgent.fulfilled,
        (state, action: PayloadAction<string>) => {
          state.loading = false;
          state.success = true;
          state.detail = action.payload;
        }
      )
      .addCase(registerAgent.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.payload ||
          action.error.message ||
          "Registration failed please try again later";
      });
  },
});

export const { resetRegistrationState } = registrationSlice.actions;
export default registrationSlice.reducer;
