import React from "react";
import { Route, Routes } from "react-router-dom";
import Login from "../pages/Login";
// import Home from "../pages/Home";
import ProtectedRoute from "./ProtectedRoute";
import Search from "../pages/Search";
import { ROUTES } from "./routes";
import Register from "../pages/Register";
import AddHouse from "../pages/AddHouse";
// import HomeLayout from "../layouts/HomeLayout";
import HouseList from "../pages/HouseList";
import Profile from "../pages/Profile";
import HouseInfo from "../pages/HouseInfo";
import ClientLayout from "../layouts/ClientLayout";
import Client from "../pages/Client";
import AddRoom from "../pages/AddRoom";
import RoomList from "../pages/RoomList";
import RoomDetail from "../pages/RoomDetail";
import ClientHouseDetail from "../pages/ClientHouseDetail";
import ClientRoomDetail from "../pages/ClientRoomDetail";
import AboutUs from "../pages/AboutUs";
import BookingDetail from "../pages/BookingDetail";
// import initFacebookPixel from "../utils/facebookPixel";
// import ReactPixel from "react-facebook-pixel";
import SubscriptionPlan from "../pages/SubscriptionPlan";
import Dashboard from "../pages/Dashboard";
import Room from "../pages/Room";
import House from "../pages/House";
import Land from "../pages/Land";
import AddLand from "../pages/AddLand";
import AgentLandDetail from "../pages/AgentLandDetail";
import ClientLandDetail from "../pages/ClientLandDetail";

const AppRouter: React.FC = () => {
  // const location = useLocation();

  // React.useEffect(() => {
  //   initFacebookPixel();
  // }, []);

  // React.useEffect(() => {
  //   ReactPixel.pageView();
  // }, [location.pathname]);

  return (
    <Routes>
      {/* Public Routes */}
      <Route path={ROUTES.CLIENT.path} element={<ClientLayout />}>
        <Route index element={<Client />} />
        <Route path={ROUTES.CLIENT_SEARCH.path} element={<Search />} />
        <Route path={ROUTES.LOGIN.path} element={<Login />} />
        <Route path={ROUTES.REGISTER.path} element={<Register />} />
        <Route
          path={ROUTES.CLIENT_HOUSE_DETAIL.path}
          element={<ClientHouseDetail />}
        />
        <Route
          path={ROUTES.CLIENT_ROOM_DETAIL.path}
          element={<ClientRoomDetail />}
        />
        <Route path={ROUTES.ABOUT_US.path} element={<AboutUs />} />
      </Route>

      {/* Protected Routes */}
      <Route
        path={ROUTES.DASHBOARD.path}
        element={
          <ProtectedRoute>
            <ClientLayout />
          </ProtectedRoute>
        }
      >
        {/* Nested Routes */}
        <Route index element={<Dashboard />} />
        <Route path={ROUTES.ADD_HOUSE.path} element={<AddHouse />} />
        <Route path={ROUTES.HOUSE_LIST.path} element={<HouseList />} />
        <Route path={ROUTES.PROFILE.path} element={<Profile />} />
        <Route path={ROUTES.HOUSE_INFO.path} element={<HouseInfo />} />
        <Route path={ROUTES.ADD_ROOM.path} element={<AddRoom />} />
        <Route path={ROUTES.ROOM_LIST.path} element={<RoomList />} />
        <Route path={ROUTES.ROOM_DETAIL.path} element={<RoomDetail />} />
        <Route path={ROUTES.BOOKING_DETAILS.path} element={<BookingDetail />} />
        <Route
          path={ROUTES.SUBSCRIPTION_PLAN.path}
          element={<SubscriptionPlan />}
        />
        <Route path={ROUTES.ROOM.path} element={<Room />} />
        <Route path={ROUTES.HOUSE.path} element={<House />} />
        <Route path={ROUTES.LAND.path} element={<Land />} />
        <Route path={ROUTES.ADD_LAND.path} element={<AddLand />} />
        <Route
          path={ROUTES.AGENT_LAND_DETAIL.path}
          element={<AgentLandDetail />}
        />
        <Route
          path={ROUTES.TENANT_LAND_DETAIL.path}
          element={<ClientLandDetail />}
        />
      </Route>
    </Routes>
  );
};

export default AppRouter;
