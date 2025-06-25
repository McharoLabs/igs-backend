import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import { useParams } from "react-router-dom";
import { fetchAgentLand } from "../state/land/landSlice";
import { MdChevronRight } from "react-icons/md";
import useNavigation from "../hooks/useNavigation";
import Image from "../components/common/Image";
import MySwiper from "../components/common/Swiper";
import { ImagePlaceholder } from "../components/common/PlaceHolder";

const AgentLandDetail: React.FC = () => {
  const { navigateToLand, goToDashboard } = useNavigation();
  const { id } = useParams<{ id: string }>();
  const dispatch = useDispatch<AppDispatch>();
  const { land, loading } = useSelector((state: RootState) => state.land);

  React.useEffect(() => {
    if (id) {
      dispatch(fetchAgentLand({ landId: id }));
    }
  }, [dispatch, id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-primary text-lg font-medium animate-pulse">
          Loading your land listing...
        </div>
      </div>
    );
  }

  if (!land) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-red-500 text-lg font-medium">
          Hakuna ardhi iliyopatikana
        </div>
      </div>
    );
  }

  const slides =
    land?.images?.map((image, index) => (
      <Image
        key={index}
        src={image}
        alt={`House Image ${index + 1}`}
        className="rounded-lg w-full h-full"
      />
    )) || [];

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="max-w-7xl w-full px-5 py-14">
        <nav className="text-sm text-primary flex items-center space-x-1">
          <button
            onClick={goToDashboard}
            className="hover:underline hover:text-blue-600 transition-colors"
          >
            Dashibodi
          </button>
          <MdChevronRight className="text-lg" />
          <button
            onClick={navigateToLand}
            className="hover:underline hover:text-blue-600 transition-colors"
          >
            Ardhi
          </button>
          <MdChevronRight className="text-lg" />
          <span className="font-medium text-gray-600">Ardhi</span>
        </nav>

        <h1 className="text-2xl font-semibold text-secondary my-8">
          Taarifa za Ardhi yako
        </h1>
        <div className="flex flex-col md:flex-row">
          {/* Image */}
          <div className="flex-shrink-0 mb-6 md:mb-0 md:w-1/2">
            <div className="mt-8">
              {land?.images && land?.images.length > 0 ? (
                <MySwiper slides={slides} />
              ) : (
                <ImagePlaceholder />
              )}
            </div>
          </div>

          {/* Details */}
          <div className="md:w-1/2 md:pl-6">
            <h2 className="text-3xl font-semibold text-primary mb-2">
              {land.category}
            </h2>
            <p className="text-xl text-secondary mb-4">{land.description}</p>

            <div className="grid grid-cols-2 gap-4 text-gray-800">
              <div>
                <strong>Size:</strong> {land.land_size} {land.land_size_unit}
              </div>
              <div>
                <strong>Price:</strong> {land.price}
              </div>
              <div>
                <strong>Zoning:</strong> {land.zoning_type}
              </div>
              <div>
                <strong>Access Road:</strong> {land.access_road_type}
              </div>
              <div>
                <strong>Utilities:</strong> {land.utilities}
              </div>
              <div>
                <strong>Status:</strong> {land.status}
              </div>
              <div>
                <strong>Listed on:</strong>{" "}
                {new Date(land.listing_date).toLocaleDateString()}
              </div>
              <div>
                <strong>Active:</strong> {land.is_active_account ? "Yes" : "No"}
              </div>
            </div>

            {/* Location */}
            <div className="mt-6 bg-secondary text-white p-4 rounded-lg">
              <h3 className="text-xl font-semibold mb-1">Location</h3>
              <p>
                {land.location.region}, {land.location.district},{" "}
                {land.location.ward}
              </p>
            </div>

            {/* Owner Actions */}
            {/* <div className="mt-6 flex gap-4">
              <button className="px-6 py-3 bg-primary text-white rounded-full hover:bg-primary-dark transition duration-300">
                Edit Listing
              </button>
              <button className="px-6 py-3 bg-red-600 text-white rounded-full hover:bg-red-700 transition duration-300">
                Delete Listing
              </button>
            </div> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentLandDetail;
