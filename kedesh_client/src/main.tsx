/* eslint-disable @typescript-eslint/no-explicit-any */
// Patch Array.prototype.map early to catch non-array usage
const originalMap = Array.prototype.map;
Array.prototype.map = function <U>(
  this: any[],
  callbackfn: (value: any, index: number, array: any[]) => U,
  thisArg?: any
): U[] {
  if (!Array.isArray(this)) {
    console.error("⚠️ .map called on non-array:", this);
  }
  // Type assertion to ensure the return type matches U[]
  return originalMap.apply(this, [callbackfn, thisArg]) as U[];
};

// Now normal imports
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { Provider } from "react-redux";
import { store } from "./state/store.ts";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </StrictMode>
);
