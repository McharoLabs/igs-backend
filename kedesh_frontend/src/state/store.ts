import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./counter/counterSlice";
import authReducer from "./auth/AuthSlice";
import registrationReducer from "./registration/registrationSlice";
import regionReducer from "./region/regionSlice";
import districtReducer from "./district/districtSlice";
import addHouseReducer from "./house/addHouseSlice";
import planReducer from "./account/planSlice";
import accountReducer from "./account/accountSlice";
import subscribeReducer from "./account/subscribeSlice";
import myHouseReducer from "./house/myHouseSlice";
import myHouseDetailReducer from "./house/myHouseInfoSlice";
import uploadHouseImages from "./house/uplaodImagesSlice";
import houseFilterReducer from "./filter/houseFilterSlice";
import roomFilterReducer from "./filter/roomFilterSlice";
import addRoomReducer from "./room/AddRoomSlice";
import agentRoomDetail from "./room/MyRoomDetailSlice";
import agentRoomList from "./room/MyRoomListSlice";
import clientHouseDetailReducer from "./filter/houseDetailSlice";
import clientRoomDetailReducer from "./filter/roomDetailSlice";
import bookingOrderReducer from "./booking/BookingSlice";
import agentBookingListReducer from "./booking/AgentBookingsListSlice";
import agentBookedPropertyDetailReducer from "./booking/AgentBookedPropertyDetail";
import activeFilterSearchReducer from "./filter/tabsSlice";
import companyInformationReducer from "./company/CompanyInformationSlice";
import markPropertyAvailableReducer from "./property/MarkPropertyAvailableSlice";
import markPropertySoldReducer from "./property/MarkPropertySoldSlice";
import markPropertyRentedReducer from "./property/MarkPropertyRentedSlice";
import demoPropertiesReducer from "./property/DemoPropertySlice";
import deleteHouseReducer from "./house/deleteSlice";
import deleteRoomReducer from "./room/deleteSlice";
import streetReducer from "./location/streetSlice";
import wardReducer from "./location/wardSlice";
import landReducer from "./land/landSlice";
import landSearchFilterReducer from "./land/landSearchSlice";

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    landFilter: landSearchFilterReducer,
    auth: authReducer,
    registration: registrationReducer,
    region: regionReducer,
    district: districtReducer,
    addHouse: addHouseReducer,
    plan: planReducer,
    account: accountReducer,
    subscribe: subscribeReducer,
    myHouse: myHouseReducer,
    myHouseDetail: myHouseDetailReducer,
    uploadHouseImages: uploadHouseImages,
    houseFilter: houseFilterReducer,
    roomFilter: roomFilterReducer,
    addRoom: addRoomReducer,
    agentRoomDetail: agentRoomDetail,
    agentRoomList: agentRoomList,
    clientRoomDetail: clientRoomDetailReducer,
    clientHouseDetail: clientHouseDetailReducer,
    bookingOrder: bookingOrderReducer,
    agentBookingList: agentBookingListReducer,
    agentBookedPropertyDetal: agentBookedPropertyDetailReducer,
    activeFilterSearch: activeFilterSearchReducer,
    companyInformation: companyInformationReducer,
    markPropertyRented: markPropertyRentedReducer,
    markPropertyAvailable: markPropertyAvailableReducer,
    markPropertySold: markPropertySoldReducer,
    demoProperties: demoPropertiesReducer,
    deleteHouse: deleteHouseReducer,
    deleteRoom: deleteRoomReducer,
    ward: wardReducer,
    street: streetReducer,
    land: landReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
