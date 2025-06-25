// useNavigation.ts (hook)
import { useNavigate } from "react-router-dom";
import { ROUTES } from "../routes/routes";
import { useDispatch } from "react-redux";
import { AppDispatch } from "../state/store";
import { signOutRequest } from "../state/auth/AuthSlice";

const useNavigation = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();

  const goToDashboard = () => navigate(ROUTES.DASHBOARD.path);
  const goToLogin = () => navigate(ROUTES.LOGIN.path);
  const goToAddHouse = () => navigate(ROUTES.ADD_HOUSE.path);
  const goToHouseList = () => navigate(ROUTES.HOUSE_LIST.path);
  const goToAddRoom = () => navigate(ROUTES.ADD_ROOM.path);
  const goToRoomList = () => navigate(ROUTES.ROOM_LIST.path);
  const goToProfile = () => navigate(ROUTES.PROFILE.path);
  const goToPage = (page: string) => navigate(page);
  const goToHouseDetail = (propertyId: string) =>
    navigate(`/home/house-info/${propertyId}`);
  const goToRoomDetail = (propertyId: string) =>
    navigate(`/home/room-info/${propertyId}`);
  const goToPrevPage = () => navigate(-1);
  const goToClient = () => navigate(ROUTES.CLIENT.path);
  const goToSearch = () => navigate(ROUTES.CLIENT_SEARCH.path);
  const goToRegistration = () => navigate(ROUTES.REGISTER.path);
  const goToClientHouseDetail = (propertyId: string) =>
    navigate(`/house-detail/${propertyId}`);
  const goToClientRoomDetail = (propertyId: string) =>
    navigate(`/room-detail/${propertyId}`);

  const goToAboutUs = () => navigate(ROUTES.ABOUT_US.path);
  const goToBookingDetails = (bookingId: string) =>
    navigate(`/home/booking-details/${bookingId}`);

  const goToSubscriptionPlan = () => navigate(ROUTES.SUBSCRIPTION_PLAN.path);

  const logout = () => {
    dispatch(signOutRequest());
    navigate(ROUTES.CLIENT.path);
  };

  const navigateToRoom = () => navigate(ROUTES.ROOM.path);
  const navigateToHouse = () => navigate(ROUTES.HOUSE.path);
  const navigateToLand = () => navigate(ROUTES.LAND.path);
  const navigateToAddLand = () => navigate(ROUTES.ADD_LAND.path);
  const navigateToAgentLandDetail = (id: string) =>
    navigate(`/panel/land/detail/${id}`);
  const navigateToTenantLandDetail = (id: string) =>
    navigate(`/panel/land/tenant/detail/${id}`);

  return {
    navigateToTenantLandDetail,
    navigateToAgentLandDetail,
    navigateToAddLand,
    navigateToLand,
    navigateToHouse,
    navigateToRoom,
    goToSubscriptionPlan,
    goToBookingDetails,
    goToAboutUs,
    goToClientHouseDetail,
    goToClientRoomDetail,
    goToRoomDetail,
    goToAddRoom,
    goToRoomList,
    goToRegistration,
    goToClient,
    goToSearch,
    goToPrevPage,
    goToHouseDetail,
    goToProfile,
    goToAddHouse,
    goToHouseList,
    goToDashboard,
    goToLogin,
    goToPage,
    logout,
  };
};

export default useNavigation;
