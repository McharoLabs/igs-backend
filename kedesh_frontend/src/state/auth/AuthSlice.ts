import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";
import { jwtDecode } from "jwt-decode";
import { RootState } from "../store";

interface AuthState {
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  tokens: {
    access: string | null;
    refresh: string | null;
  };
  user: {
    full_name: string | null;
    email: string | null;
    is_superuser: boolean;
  };
  errorCode: number | null;
}

interface DecodedToken {
  full_name: string;
  email: string;
  is_superuser: boolean;
  exp: number;
}

interface RejectedPayload {
  status: number;
  detail: string;
}

// Load tokens and user data from localStorage
const loadTokensFromLocalStorage = () => {
  const access = localStorage.getItem("access_token");
  const refresh = localStorage.getItem("refresh_token");
  return { access, refresh };
};

const restoreUserDataFromToken = (accessToken: string | null) => {
  if (accessToken) {
    try {
      const decoded: DecodedToken = jwtDecode(accessToken);
      return {
        full_name: decoded.full_name,
        email: decoded.email,
        is_superuser: decoded.is_superuser,
      };
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      return { full_name: null, email: null, is_superuser: true };
    }
  }
  return { full_name: null, email: null, is_superuser: true };
};

const { access, refresh } = loadTokensFromLocalStorage();

const userData = restoreUserDataFromToken(access);

const initialStateWithTokens: AuthState = {
  loading: false,
  error: null,
  isAuthenticated: !!access && !userData.is_superuser,
  tokens: { access, refresh },
  user: userData,
  errorCode: null,
};

// Store tokens in localStorage
const storeTokensToLocalStorage = (tokens: {
  access: string | null;
  refresh: string | null;
}) => {
  if (tokens.access) {
    localStorage.setItem("access_token", tokens.access);
  }
  if (tokens.refresh) {
    localStorage.setItem("refresh_token", tokens.refresh);
  }
};

export const deleteTokenFromLocal = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};

// Async thunk to send sign-out request
export const signOutRequest = createAsyncThunk<
  string,
  void,
  { rejectValue: string }
>("auth/signOutRequest", async (_, { getState, rejectWithValue }) => {
  const { refresh, access } = (getState() as RootState).auth.tokens;
  if (!refresh) {
    return rejectWithValue("No refresh token found");
  }

  const formData = new FormData();
  formData.append("refresh", refresh);

  try {
    const response = await apiClient.post(endpoints.signOut, formData, {
      headers: {
        Authorization: `Bearer ${access}`,
      },
    });
    console.log(response.data);
    return response.data.detail;
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
  } catch (error) {
    return rejectWithValue("Failed to sign out");
  }
});

export const signIn = createAsyncThunk(
  "auth/signIn",
  async (
    credentials: { username: string; password: string },
    { rejectWithValue }
  ) => {
    try {
      const response = await apiClient.post(endpoints.login, credentials);
      return response.data;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
      const status = error.response?.status;
      let detail =
        error.response?.data?.detail || "An unexpected error occurred";

      if (error.response?.status === 400) {
        detail =
          error.response?.data?.non_field_errors[0] || "Invalid credentials";
      } else if (error.response?.status === 500) {
        detail = "Something went wrong on the server";
      } else {
        detail = "Invalid credentials";
      }

      return rejectWithValue({ status, detail });
    }
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState: initialStateWithTokens,
  reducers: {
    signOut: (state) => {
      state.tokens = { access: null, refresh: null };
      state.user = { full_name: null, email: null, is_superuser: false };
      state.loading = false;
      state.error = null;
      state.errorCode = null;

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(signIn.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.errorCode = null;
      })
      .addCase(signIn.fulfilled, (state, action: PayloadAction<AuthState>) => {
        state.loading = false;
        state.tokens = action.payload.tokens;
        storeTokensToLocalStorage(action.payload.tokens);

        if (action.payload.tokens.access) {
          try {
            const decoded: DecodedToken = jwtDecode(
              action.payload.tokens.access
            );
            state.user.full_name = decoded.full_name;
            state.user.email = decoded.email;
            state.isAuthenticated = !decoded.is_superuser;

            if (Date.now() >= decoded.exp * 1000) {
              state.error = "Session expired. Please sign in again.";
            }
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
          } catch (error) {
            state.error = "Failed to decode token.";
          }
        }
      })
      .addCase(signIn.rejected, (state, action) => {
        state.loading = false;

        if (action.payload && typeof action.payload === "object") {
          const { status, detail } = action.payload as RejectedPayload;
          state.errorCode = status;
          state.error = detail;
        } else {
          state.error = "An unexpected error occurred.";
        }
      })
      // Handle the sign-out request
      .addCase(signOutRequest.pending, (state) => {
        state.loading = true;
      })
      .addCase(signOutRequest.fulfilled, (state) => {
        state.loading = false;
        state.tokens = { access: null, refresh: null };
        state.user = { full_name: null, email: null, is_superuser: false };
        state.isAuthenticated = false;
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      })
      .addCase(signOutRequest.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Failed to sign out";
      });
  },
});

export const { signOut } = authSlice.actions;
export default authSlice.reducer;
