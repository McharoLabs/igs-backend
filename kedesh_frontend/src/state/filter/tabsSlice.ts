import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type Active = "House" | "Room" | "Land";

interface ActiveSearchState {
  activeSearchValue: Active;
}

const initialState: ActiveSearchState = {
  activeSearchValue: "House",
};

const ActiveSearchSlice = createSlice({
  name: "ActiveSearch",
  initialState: initialState,
  reducers: {
    setActiveSearchFilter: (state, action: PayloadAction<Active>) => {
      state.activeSearchValue = action.payload;
    },
  },
});

export const { setActiveSearchFilter } = ActiveSearchSlice.actions;

export default ActiveSearchSlice.reducer;
