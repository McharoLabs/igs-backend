interface Route {
  path: string;
  name: string;
}

interface DynamicRoute {
  (id: string): Route;
}

interface Routes {
  SUBSCRIPTION_PLAN: Route;
  HOME_SEARCH: Route;
  LOGIN: Route;
  REGISTER: Route;
  ADD_HOUSE: Route;
  HOUSE_LIST: Route;
  HOUSE_INFO: Route;
  PROPERTY_LISTINGS: Route;
  PROFILE: Route;
  PROPERTY_DETAIL: DynamicRoute;
  ADD_ROOM: Route;
  ROOM_LIST: Route;
  CLIENT: Route;
  CLIENT_ROOM_DETAIL: Route;
  CLIENT_HOUSE_DETAIL: Route;
  CLIENT_SEARCH: Route;
  ROOM_DETAIL: Route;
  ABOUT_US: Route;
  BOOKING_DETAILS: Route;
  DASHBOARD: Route;
  ROOM: Route;
  HOUSE: Route;
  LAND: Route;
  ADD_LAND: Route;
  AGENT_LAND_DETAIL: Route;
  TENANT_LAND_DETAIL: Route;
}

export const ROUTES: Routes = {
  ABOUT_US: { path: "/about-us", name: "About Us" },
  CLIENT: { path: "/", name: "client" },
  CLIENT_SEARCH: { path: "/search", name: "Search" },
  CLIENT_HOUSE_DETAIL: {
    path: "/house-detail/:propertyId",
    name: "House Detail",
  },
  SUBSCRIPTION_PLAN: {
    path: "/panel/plan/subscribe",
    name: "Subscription Plan",
  },
  CLIENT_ROOM_DETAIL: { path: "/room-detail/:propertyId", name: "Room Detail" },
  ADD_ROOM: { path: "/panel/add-room", name: "Add Room" },
  ROOM_LIST: { path: "/panel/room-list", name: "Room List" },
  HOME_SEARCH: { path: "/", name: "Home Search" },
  LOGIN: { path: "/auth", name: "Login" },
  REGISTER: { path: "/register", name: "Register" },
  PROFILE: { path: "/panel/profile", name: "Profile" },
  ADD_HOUSE: { path: "/panel/add-house", name: "Add New House" },
  HOUSE_LIST: { path: "/panel/house-list", name: "House List" },
  HOUSE_INFO: { path: "/panel/house-info/:propertyId", name: "House Info" },
  ROOM_DETAIL: { path: "/panel/room-info/:propertyId", name: "Room Detail" },
  BOOKING_DETAILS: {
    path: "/panel/booking-details/:bookingId",
    name: "Booking Details",
  },
  PROPERTY_LISTINGS: { path: "/listings", name: "Property Listings" },
  PROPERTY_DETAIL: (id: string) => ({
    path: `/properties/${id}`,
    name: `Property Detail: ${id}`,
  }),

  DASHBOARD: {
    path: "/panel",
    name: "Dashboard",
  },
  ROOM: {
    path: "/panel/room",
    name: "Room",
  },
  HOUSE: {
    path: "/panel/house",
    name: "House",
  },
  LAND: {
    path: "/panel/land",
    name: "Land",
  },
  ADD_LAND: {
    path: "/panel/land/add-land",
    name: "Add Land",
  },
  AGENT_LAND_DETAIL: {
    path: "/panel/land/detail/:id",
    name: "Land Detail",
  },
  TENANT_LAND_DETAIL: {
    path: "/panel/land/tenant/detail/:id",
    name: "Land Details",
  },
};
