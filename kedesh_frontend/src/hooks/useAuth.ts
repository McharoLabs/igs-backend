import { useSelector } from "react-redux";
import { RootState } from "../state/store";

export const useAuth = () => {
  const isAuthenticated = useSelector(
    (state: RootState) => state.auth.isAuthenticated
  );
  return isAuthenticated;
};
