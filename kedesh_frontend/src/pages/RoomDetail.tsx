import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { AppDispatch, RootState } from "../state/store";
import Loader from "../components/common/Loader";
import { ImagePlaceholder } from "../components/common/PlaceHolder";
import MySwiper from "../components/common/Swiper";
import Image from "../components/common/Image";
import Message from "../components/common/Message";
import { resetUploadImagesState } from "../state/house/uplaodImagesSlice";
import useNavigation from "../hooks/useNavigation";
import { fetchRoomDetail } from "../state/room/MyRoomDetailSlice";

const RoomDetail = () => {
  const { goToPrevPage } = useNavigation();
  const { propertyId } = useParams<{ propertyId: string }>();
  const { error, loading, myRoomDetail } = useSelector(
    (state: RootState) => state.agentRoomDetail
  );

  const roomDispatch = useDispatch<AppDispatch>();
  const uploadDispatch = useDispatch<AppDispatch>();

  React.useEffect(() => {
    if (propertyId) {
      roomDispatch(fetchRoomDetail({ propertyId }));
    }
  }, [propertyId, roomDispatch]);

  if (loading) {
    return (
      <Loader key="house-detail" label="Loading details..." loading={loading} />
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-500 text-xl mt-8">
        There was an error loading the room details.
      </div>
    );
  }

  const slides =
    myRoomDetail?.images?.map((image, index) => (
      <Image
        key={index}
        src={image}
        alt={`House Image ${index + 1}`}
        className="rounded-lg w-full h-full"
      />
    )) || [];

  return (
    <div className="max-w-screen-xl mx-auto ">
      <div className="mb-4">
        <button
          onClick={() => goToPrevPage()}
          className="px-4 py-2 bg-primary text-white rounded-lg shadow-md hover:bg-primary focus:outline-none"
        >
          Back
        </button>
      </div>

      <Message
        isOpen={!!error}
        message={error ?? ""}
        xClose={() => uploadDispatch(resetUploadImagesState())}
        type="error"
      />

      <Loader label="Loading information" loading={loading} />

      {/* House Image Gallery */}
      <div className="mt-8">
        {myRoomDetail?.images && myRoomDetail?.images.length > 0 ? (
          <MySwiper slides={slides} />
        ) : (
          <ImagePlaceholder />
        )}
      </div>

      {/* House Description */}
      <div className="mt-8 bg-gray-100 p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold text-gray-800">Description</h2>
        <p className="text-gray-700 mt-4">
          {myRoomDetail?.description || "No description available"}
        </p>
      </div>

      {/* House Features */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
        <div className="bg-white p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Price:</strong>
          <p className="text-gray-600">
            {myRoomDetail?.price || "Not available"}
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Condition:</strong>
          <p className="text-gray-600">
            {myRoomDetail?.condition || "Not available"}
          </p>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Security Features:</strong>
          <p className="text-gray-600">
            {myRoomDetail?.security_features || "Not available"}
          </p>
        </div>
      </div>

      <div className="mt-8 bg-gray-100 p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold text-gray-800">
          Near by facilities
        </h2>
        <p className="text-gray-700 mt-4">
          {myRoomDetail?.nearby_facilities || "No description available"}
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
        <div className="bg-white p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Heating/Cooling:</strong>
          <p className="text-gray-600">
            {myRoomDetail?.heating_cooling_system || "Not available"}
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Furnishing:</strong>
          <p className="text-gray-600">
            {myRoomDetail?.furnishing_status || "Not available"}
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md">
          <strong className="text-gray-700">Availability status:</strong>
          <p className="text-gray-600">
            {myRoomDetail?.status || "Not available"}
          </p>
        </div>
      </div>

      <div className="mt-8 bg-gray-100 p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold text-gray-800">Utilities</h2>
        <p className="text-gray-700 mt-4">
          {myRoomDetail?.utilities || "No description available"}
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md mt-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Location</h2>
        <div>
          <p className="text-gray-600">
            <strong>Region:</strong> {myRoomDetail?.location.region}
          </p>
          <p className="text-gray-600">
            <strong>District:</strong> {myRoomDetail?.location.district}
          </p>
          <p className="text-gray-600">
            <strong>Ward:</strong> {myRoomDetail?.location.ward}
          </p>
        </div>
      </div>
    </div>
  );
};

export default RoomDetail;
