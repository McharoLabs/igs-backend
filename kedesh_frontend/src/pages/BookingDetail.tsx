import React from "react";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";
import { fetchAgentBookedPropertyDetails } from "../state/booking/AgentBookedPropertyDetail";
import { AppDispatch, RootState } from "../state/store";
import Image from "../components/common/Image";
import { resetAgentBookedPropertyDetailState } from "../state/booking/AgentBookedPropertyDetail";
import MySwiper from "../components/common/Swiper";
import { ImagePlaceholder } from "../components/common/PlaceHolder";
import Button from "../components/common/Button";
import { PROPERTY_AVAILABILITY_STATUS } from "../types/enums";
import {
  markPropertyAvailable,
  resetMarkPropertyAvailable,
} from "../state/property/MarkPropertyAvailableSlice";
import {
  fetchAgentBookingList,
  resetAgentBookingListState,
} from "../state/booking/AgentBookingsListSlice";
import useNavigation from "../hooks/useNavigation";
import {
  markPropertyRented,
  resetMarkPropertyRented,
} from "../state/property/MarkPropertyRentedSlice";

const BookedProperty = () => {
  const { goToDashboard } = useNavigation();
  const { bookingId } = useParams<{ bookingId: string }>();
  const { error, loading, bookedProperty } = useSelector(
    (state: RootState) => state.agentBookedPropertyDetal
  );
  const {
    detail: markPropertyAvailableDetail,
    error: markPropertyAvailableError,
    loading: markPropertyAvailableLoading,
    statusCode: markPropertyAvailableStatusCode,
  } = useSelector((state: RootState) => state.markPropertyAvailable);

  const {
    detail: markPropertyRentedDetail,
    error: markPropertyRentedError,
    loading: markPropertyRentedLoading,
    statusCode: markPropertyRentedStatusCode,
  } = useSelector((state: RootState) => state.markPropertyRented);

  const dispatch = useDispatch<AppDispatch>();

  React.useEffect(() => {
    if (bookingId) {
      dispatch(fetchAgentBookedPropertyDetails({ bookingId }));
    }

    return () => {
      dispatch(resetAgentBookedPropertyDetailState());
    };
  }, [bookingId, dispatch]);

  if (loading) {
    return (
      <Loader
        key="booking-detail"
        label="Loading booking details..."
        loading={loading}
      />
    );
  }

  if (error) {
    return (
      <Message
        isOpen={true}
        message={error || "Error loading booking details"}
        type="error"
        xClose={() => dispatch(resetAgentBookedPropertyDetailState())}
        title="Error"
      />
    );
  }

  if (markPropertyAvailableStatusCode === 200) {
    if (bookingId) {
      dispatch(fetchAgentBookingList({ customerName: "" }));
      dispatch(resetAgentBookingListState());
    }
  }

  if (markPropertyRentedStatusCode === 200) {
    if (bookingId) {
      dispatch(fetchAgentBookingList({ customerName: "" }));
      dispatch(resetAgentBookingListState());
    }
  }

  const slides =
    bookedProperty?.property.images.map((image, index) => (
      <Image
        key={index}
        src={image}
        alt={`House Image ${index + 1}`}
        className="rounded-lg w-full h-full"
      />
    )) || [];

  return (
    <div className="max-w-screen-xl mx-auto p-6">
      <Message
        isOpen={!!markPropertyAvailableDetail}
        message={markPropertyAvailableDetail || ""}
        type="success"
        xClose={() => {
          dispatch(resetMarkPropertyAvailable());
          goToDashboard();
        }}
      />
      <Message
        isOpen={!!markPropertyAvailableError}
        message={markPropertyAvailableError || ""}
        type="error"
        xClose={() => dispatch(resetMarkPropertyAvailable())}
      />
      <Loader
        label="Marking property available"
        loading={markPropertyAvailableLoading}
      />

      <Message
        isOpen={!!markPropertyRentedDetail}
        message={markPropertyRentedDetail || ""}
        type="success"
        xClose={() => {
          dispatch(resetMarkPropertyRented());
          goToDashboard();
        }}
      />
      <Message
        isOpen={!!markPropertyRentedError}
        message={markPropertyRentedError || ""}
        type="error"
        xClose={() => dispatch(resetMarkPropertyRented())}
      />
      <Loader
        label="Marking property Rented"
        loading={markPropertyRentedLoading}
      />

      {/* Title Section */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Booked Property</h1>
        <button
          onClick={() => window.history.back()}
          className="px-4 py-2 bg-primary text-white rounded-lg shadow-md hover:bg-primary focus:outline-none"
        >
          Go Back
        </button>
      </div>

      {/* Property Images Section */}
      <div className=" mb-8">
        {bookedProperty?.property.images &&
        bookedProperty.property.images.length > 0 ? (
          <MySwiper slides={slides} />
        ) : (
          <ImagePlaceholder />
        )}
      </div>

      {/* Booking Details Section */}
      <div className="bg-gray-100 p-6 rounded-lg shadow-md ">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          Booking Details
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <strong className="block text-gray-700">Customer Name:</strong>
            <p className="text-gray-600">{bookedProperty?.customer_name}</p>
          </div>
          <div>
            <strong className="block text-gray-700">Customer Email:</strong>
            <p className="text-gray-600">{bookedProperty?.customer_email}</p>
          </div>
          <div>
            <strong className="block text-gray-700">Customer Phone:</strong>
            <p className="text-gray-600">
              {bookedProperty?.customer_phone_number}
            </p>
          </div>
          <div>
            <strong className="block text-gray-700">Listing Date:</strong>
            <p className="text-gray-600">{bookedProperty?.listing_date}</p>
          </div>
        </div>
      </div>

      {/* House Description */}
      <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold text-gray-800">Description</h2>
        <p className="text-gray-700 mt-4">
          {bookedProperty?.property?.description || "No description available"}
        </p>
      </div>

      {/* House Features */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
        <div className="bg-gray-100 p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Price:</strong>
          <p className="text-gray-600">
            {bookedProperty?.property?.price || "Not available"}
          </p>
        </div>
        <div className="bg-gray-100 p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Condition:</strong>
          <p className="text-gray-600">
            {bookedProperty?.property?.condition || "Not available"}
          </p>
        </div>

        <div className="bg-gray-100 p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Security Features:</strong>
          <p className="text-gray-600">
            {bookedProperty?.property?.security_features || "Not available"}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
        <div className="bg-white p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Heating/Cooling:</strong>
          <p className="text-gray-600">
            {bookedProperty?.property?.heating_cooling_system ||
              "Not available"}
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Furnishing:</strong>
          <p className="text-gray-600">
            {bookedProperty?.property?.furnishing_status || "Not available"}
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Availability status:</strong>
          <p className="text-gray-600">
            {bookedProperty?.property?.status || "Not available"}
          </p>
        </div>
      </div>

      <div className="mt-8 bg-gray-100 p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold text-gray-800">
          Near by facilities
        </h2>
        <p className="text-gray-700 mt-4">
          {bookedProperty?.property?.nearby_facilities ||
            "No description available"}
        </p>
      </div>

      <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold text-gray-800">Utilities</h2>
        <p className="text-gray-700 mt-4">
          {bookedProperty?.property?.utilities || "No description available"}
        </p>
      </div>

      {/* Location Details Section */}
      <div className="bg-gray-100 p-6 rounded-lg shadow-md mt-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Location</h2>
        <div>
          <p className="text-gray-600">
            <strong>Region:</strong> {bookedProperty?.property.location.region}
          </p>
          <p className="text-gray-600">
            <strong>District:</strong>{" "}
            {bookedProperty?.property.location.district}
          </p>
          <p className="text-gray-600">
            <strong>Ward:</strong> {bookedProperty?.property.location.ward}
          </p>
        </div>
      </div>

      {bookedProperty?.property.status ===
        PROPERTY_AVAILABILITY_STATUS.BOOKED && (
        <div className=" p-6 mt-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Actions</h2>
          <div className="flex flex-row gap-6">
            <Button
              type="button"
              className="bg-green-500 hover:bg-green-600"
              onClick={() =>
                dispatch(
                  markPropertyRented({
                    propertyId: bookedProperty.property.property_id,
                  })
                )
              }
            >
              Mark Rented
            </Button>
            <Button
              type="button"
              onClick={() =>
                dispatch(
                  markPropertyAvailable({
                    propertyId: bookedProperty.property.property_id,
                  })
                )
              }
            >
              Mark Available
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default BookedProperty;
