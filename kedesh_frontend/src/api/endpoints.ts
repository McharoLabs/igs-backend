export const endpoints = {
  clientRoomDetail: (propertyId: string) =>
    `/room/rooms/${propertyId}/room_detail/`,
  clientHouseDetail: (propertyId: string) =>
    `/house/houses/${propertyId}/house_detail/`,
  login: "/auth/sign-in",
  signOut: "/auth/sign-out",
  plans: "/account/plans/get_subscription/",
  account: "/account/accounts/account/",
  subscribe: "/account/plans/subscribe/",
  agentRegistration: "/user/agents/register/",
  properties: "/properties",
  avatar: "/user/users/serve_avatar/",
  regions: "/location/regions/list_regions/",
  districts: "/location/districts/list_districts/",
  addHouse: "/house/houses/add_house/",
  addRoom: "/room/rooms/add_room/",
  agentRoomDetail: (property_id: string) =>
    `/room/rooms/${property_id}/retrieve_room/`,
  roomList: "/room/rooms/room_list/",
  uploadHouseImages: "/house/images/upload_images/",
  houseList: "/house/houses/list_houses/",
  filterHouse: "/house/houses/filter_houses/",
  filterRooms: "/room/rooms/room_filter/",
  booking_order: "/booking/bookings/make_booking/",
  requestAgentPhoneNumber: "/booking/bookings/request_agent_info/",
  myHouseDetail: (propertyId: string) =>
    `/house/houses/${propertyId}/retrieve_house/`,
  districtsByRegion: (region_id: string) =>
    `/location/districts/${region_id}/retrieve_region_districts/`,
  propertyDetail: (id: string) => `/properties/${id}`,
  agentBookingList: (customerName: string) =>
    `/booking/bookings/agent_booked_properties/?customer_name=${customerName}`,
  agentBookedPropertyDetail: (bookingId: string) =>
    `/booking/bookings/${bookingId}/agent_booked_property/`,
  companyInformation: "/company_information/informations/get_information/",
  markPropertyRented: (propertyId: string) =>
    `/property/properties/${propertyId}/mark_property_rented/`,
  markPropertySold: (propertyId: string) =>
    `/property/properties/${propertyId}/mark_property_sold/`,
  markPropertyAvailable: (propertyId: string) =>
    `/property/properties/${propertyId}/mark_property_available/`,
  demoProperties: "/property/properties/demo_property/",
  deleteHouse: (propertyId: string) =>
    `/house/houses/${propertyId}/soft_delete_house/`,
  deleteRoom: (propertyId: string) =>
    `/room/rooms/${propertyId}/soft_delete_room/`,
  wardByDistrict: (districtId: string) =>
    `/location/wards/${districtId}/retrieve_district_wards/`,
  streetByWard: (wardId: string) =>
    `/location/streets/${wardId}/retrieve_ward_streets/`,
  addLand: () => "/land/lands/add_land/",
  landList: "/land/lands/land_list/",
  fetchAgentLand: (landId: string) => `/land/lands/${landId}/retrieve_land/`,
  deleteLand: (landId: string) => `/land/lands/${landId}/soft_delete_land/`,
  fetchFilteredLand: () => "/land/lands/land_filter/",
  fetchLandDetails: (landId: string) =>
    `/land/lands/${landId}/retrieve_land_details/`,
  requestAgentLandPhoneNumber: () => `/land/lands/request_agent_info/`,
};
