import React from "react";
import Image from "../components/common/Image";
import useNavigation from "../hooks/useNavigation";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { AppDispatch, RootState } from "../state/store";
import Loader from "../components/common/Loader";
import MySwiper from "../components/common/Swiper";
import { ImagePlaceholder } from "../components/common/PlaceHolder";
import Modal from "../components/common/Modal";
import { zodResolver } from "@hookform/resolvers/zod";
import { SubmitHandler, useForm } from "react-hook-form";
import { resetbookingOrderState } from "../state/booking/BookingSlice";
import TextInput from "../components/common/InputText";
import Button from "../components/common/Button";
import Notification from "../components/common/Notification";
import Message from "../components/common/Message";
import { PROPERTY_AVAILABILITY_STATUS } from "../types/enums";
import { formatPrice } from "../utils/PriceFormat";
import {
  fetchLandDetails,
  requestAgentLandPhoneNumber,
  resetLandState,
} from "../state/land/landSlice";
import {
  RequestAgentContactSchema,
  RequestAgentContactSchemaType,
} from "../schemas/LandSchema";

const Feature = ({ title, value }: { title: string; value: string }) => (
  <div className="border-l-4 border-primary pl-4 py-2 bg-accent-gray/10 rounded-md">
    <h3 className="text-md font-semibold text-secondary">{title}</h3>
    <p className="text-accent-gray">{value}</p>
  </div>
);

const ClientLandDetail = () => {
  const { goToPrevPage } = useNavigation();
  const { id } = useParams<{ id: string }>();
  const { error, loading, landDetails } = useSelector(
    (state: RootState) => state.land
  );

  const {
    detail: orderDetail,
    loading: laodinSubmittingOrder,
    error: orderError,
  } = useSelector((state: RootState) => state.land);

  const dispatch = useDispatch<AppDispatch>();
  const [isModalOpen, openModal] = React.useState(false);
  const [showBookingMessage, setShowBookingMessage] =
    React.useState<boolean>(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    reset,
  } = useForm<RequestAgentContactSchemaType>({
    resolver: zodResolver(RequestAgentContactSchema),
  });

  React.useEffect(() => {
    if (id) {
      dispatch(fetchLandDetails({ landId: id }));
      setValue("land_id", id);
    }
  }, [dispatch, id, setValue]);

  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const onSubmit: SubmitHandler<RequestAgentContactSchemaType> = (data) => {
    dispatch(requestAgentLandPhoneNumber(data))
      .unwrap()
      .then(() => {
        setShowBookingMessage(true);
        reset();
      })
      .catch(() => {
        setShowBookingMessage(true);
        reset();
      });
  };

  if (loading) {
    return <Loader key="land-detail" label="Inapakia maelezo..." loading />;
  }

  if (error) {
    return (
      <div className="text-center text-red-500 text-xl mt-8">
        Kulikuwa na tatizo la kupakua maelezo ya kiwanja.
      </div>
    );
  }

  const slides =
    landDetails?.images?.map((image, index) => (
      <Image
        key={index}
        src={image}
        alt={`Picha ya Kiwanja ${index + 1}`}
        className="rounded-lg w-full h-full"
      />
    )) || [];

  return (
    <div className="max-w-7xl mx-auto px-6 py-16 space-y-12 font-poppins text-secondary-dark">
      <Message
        isOpen={showBookingMessage}
        message={orderDetail || orderDetail || ""}
        type="info"
        xClose={() => {
          setShowBookingMessage(false);
          dispatch(resetbookingOrderState());
          dispatch(resetLandState());
        }}
      />

      <Message
        isOpen={!!orderError}
        title="Tatizo la Booking"
        message={orderError || ""}
        type="error"
        xClose={() => dispatch(resetbookingOrderState())}
      />

      {/* MODAL */}
      <Modal isOpen={isModalOpen} title="" xButton={() => openModal(false)}>
        <div className="flex flex-col space-y-1">
          <p className="text-center text-lg font-semibold text-gray-800 border-l-4 border-primary pl-4 py-2 bg-accent-gray/10 rounded-md mb-4">
            Weka taarifa zako tukutumie meseji ya mawasiliano ya mmiliki kwenye
            namba yako ya simu
          </p>
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-2"
          >
            {errors.land_id?.message && (
              <Notification
                message={"Tafadhali rejesha ukurasa wako"}
                title="Hitilafu"
                type="error"
              />
            )}

            <TextInput
              label="Jina Kamili"
              type="text"
              register={register("customer_name")}
              error={errors.customer_name?.message}
            />
            <TextInput
              label="Barua pepe"
              type="email"
              register={register("customer_email")}
              error={errors.customer_email?.message}
            />
            <TextInput
              label="Namba ya Simu"
              type="tel"
              register={register("customer_phone")}
              error={errors.customer_phone?.message}
            />

            <Button
              type="submit"
              disabled={laodinSubmittingOrder}
              isLoading={laodinSubmittingOrder}
              className="mt-6 bg-primary hover:bg-secondary"
            >
              Tuma maombi
            </Button>
          </form>
        </div>
      </Modal>

      {/* NAVIGATION */}
      <div className="mb-4 flex justify-between items-center">
        <button
          onClick={goToPrevPage}
          className="px-4 py-2 bg-secondary text-white rounded-lg shadow hover:bg-secondary-dark focus:outline-none"
        >
          Rudi Nyuma
        </button>
        {landDetails?.status.toLowerCase() ===
          PROPERTY_AVAILABILITY_STATUS.AVAILABLE.toLowerCase() && (
          <button
            onClick={() => openModal(true)}
            className="px-4 py-2 bg-primary text-white rounded-lg shadow hover:bg-primary-dark focus:outline-none"
          >
            Pata Mawasiliano
          </button>
        )}
      </div>

      {/* IMAGES */}
      <div>
        {landDetails?.images && landDetails.images.length > 0 ? (
          <MySwiper slides={slides} />
        ) : (
          <ImagePlaceholder />
        )}
      </div>

      {/* DESCRIPTION */}
      <section className="mt-8">
        <h2 className="text-2xl font-semibold text-secondary-dark mb-2">
          Maelezo
        </h2>
        <p className="text-accent-gray leading-relaxed">
          {landDetails?.description || "Hakuna maelezo yaliyopatikana"}
        </p>
      </section>

      {/* LOCATION */}
      <section className="mt-8 bg-primary text-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold text-secondary-dark mb-2">
          Mahali
        </h2>
        <p>
          <strong>Mkoa:</strong>{" "}
          {landDetails?.location?.region || "Haipatikani"}
        </p>
        <p>
          <strong>Wilaya:</strong>{" "}
          {landDetails?.location?.district || "Haipatikani"}
        </p>
        <p>
          <strong>Kata:</strong> {landDetails?.location?.ward || "Haipatikani"}
        </p>
        <p>
          <strong>Mtaa:</strong>{" "}
          {landDetails?.location?.street || "Haipatikani"}
        </p>
      </section>

      {/* FEATURES */}
      <section className="mt-12 space-y-6">
        <Feature
          title="Bei"
          value={formatPrice(landDetails?.price, "TZS") + " kwa eneo lote"}
        />
        <Feature
          title="Ukubwa wa Eneo"
          value={
            landDetails?.land_size + " " + landDetails?.land_size_unit ||
            "Haipatikani"
          }
        />
        <Feature
          title="Aina ya Barabara"
          value={landDetails?.access_road_type || "Haipatikani"}
        />
        <Feature
          title="Zoning Type"
          value={landDetails?.zoning_type || "Haipatikani"}
        />
        <Feature
          title="Huduma"
          value={landDetails?.utilities || "Haipatikani"}
        />
        <Feature
          title="Maelezo"
          value={landDetails?.description || "Haipatikani"}
        />
        <Feature
          title="Tarehe ya Kutangazwa"
          value={landDetails?.listing_date || "Haipatikani"}
        />
      </section>
    </div>
  );
};

export default ClientLandDetail;
