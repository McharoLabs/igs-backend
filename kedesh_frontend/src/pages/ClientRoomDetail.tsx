import React from "react";
import Image from "../components/common/Image";
import useNavigation from "../hooks/useNavigation";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { AppDispatch, RootState } from "../state/store";
import { fetchClientRoomDetail } from "../state/filter/roomDetailSlice";
import Loader from "../components/common/Loader";
import MySwiper from "../components/common/Swiper";
import { ImagePlaceholder } from "../components/common/PlaceHolder";
import Modal from "../components/common/Modal";
import { zodResolver } from "@hookform/resolvers/zod";
import { BookingSchema, BookingType } from "../schemas/BookingSchema";
import { SubmitHandler, useForm } from "react-hook-form";
import {
  bookingOrder,
  resetbookingOrderState,
} from "../state/booking/BookingSlice";
import TextInput from "../components/common/InputText";
import Button from "../components/common/Button";
import Notification from "../components/common/Notification";
import Message from "../components/common/Message";
import { PROPERTY_AVAILABILITY_STATUS } from "../types/enums";
import { formatPrice } from "../utils/PriceFormat";
import ReactPixel from "react-facebook-pixel";

const Feature = ({ title, value }: { title: string; value: string }) => (
  <div className="border-l-4 border-primary pl-4 py-2 bg-accent-gray/10 rounded-md">
    <h3 className="text-md font-semibold text-secondary">{title}</h3>
    <p className="text-accent-gray">{value}</p>
  </div>
);

const ClientRoomDetail = () => {
  const { goToPrevPage } = useNavigation();
  const { propertyId } = useParams<{ propertyId: string }>();
  const { error, loading, room } = useSelector(
    (state: RootState) => state.clientRoomDetail
  );
  const {
    detail: orderDetail,
    loading: submittingOrder,
    statusCode: orderStatusCode,
    error: orderError,
  } = useSelector((state: RootState) => state.bookingOrder);

  const dispatch = useDispatch<AppDispatch>();

  const [isModalOpen, openModal] = React.useState<boolean>(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    reset,
  } = useForm<BookingType>({
    resolver: zodResolver(BookingSchema),
  });

  React.useEffect(() => {
    if (propertyId) {
      dispatch(fetchClientRoomDetail({ propertyId }));
      setValue("property_id", propertyId);
    }
  }, [dispatch, propertyId, setValue]);

  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  React.useEffect(() => {
    if (orderStatusCode === 200 && propertyId) {
      reset({
        customer_email: "",
        customer_name: "",
        customer_phone: "",
      });
      openModal(false);
      dispatch(fetchClientRoomDetail({ propertyId }));
    } else {
      openModal(false);
    }
  }, [dispatch, orderStatusCode, propertyId, reset]);

  const onSubmit: SubmitHandler<BookingType> = async (data) => {
    ReactPixel.track("Lead", {
      content_name: "Booking Submission",
      fn: data.customer_name,
      em: data.customer_email,
      ph: data.customer_phone,
    });

    try {
      await dispatch(bookingOrder(data));
    } catch (error) {
      console.error("Error submitting room data:", error);
    }
  };

  if (loading) {
    return (
      <Loader key="room-detail" label="Inapakia maelezo..." loading={loading} />
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-500 text-xl mt-8">
        Kulikuwa na tatizo la kupakua maelezo ya chumba.
      </div>
    );
  }

  const slides =
    room?.images?.map((image, index) => (
      <Image
        key={index}
        src={image}
        alt={`Picha ya Chumba ${index + 1}`}
        className="rounded-lg w-full h-full"
      />
    )) || [];

  return (
    <div className="max-w-7xl mx-auto px-6 py-16 space-y-12 font-poppins text-secondary-dark">
      {/* SUCCESS / ERROR MESSAGES */}
      {orderStatusCode === 200 && orderDetail && (
        <Message
          isOpen={true}
          message={`${orderDetail}`}
          type="success"
          xClose={() => dispatch(resetbookingOrderState())}
        />
      )}

      {orderStatusCode !== 200 && orderDetail && (
        <Message
          isOpen={true}
          message={orderDetail}
          type="error"
          xClose={() => {
            reset();
            dispatch(resetbookingOrderState());
          }}
        />
      )}

      <Message
        isOpen={!!orderError}
        title="Tatizo la Booking"
        message={orderError || ""}
        type="error"
        xClose={() => dispatch(resetbookingOrderState())}
      />

      {/* MODAL FORM */}
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
            {errors.property_id?.message && (
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
              disabled={submittingOrder}
              isLoading={submittingOrder}
              className="mt-6 bg-primary hover:bg-secondary"
            >
              Tuma maombi
            </Button>
          </form>
        </div>
      </Modal>

      {/* NAVIGATION BUTTONS */}
      <div className="mb-4 flex justify-between items-center">
        <button
          onClick={goToPrevPage}
          className="px-4 py-2 bg-secondary text-white rounded-lg shadow hover:bg-secondary-dark focus:outline-none"
        >
          Rudi Nyuma
        </button>
        {room?.status.toLowerCase() ===
          PROPERTY_AVAILABILITY_STATUS.AVAILABLE.toLowerCase() && (
          <button
            onClick={() => openModal(true)}
            className="px-4 py-2 bg-primary text-white rounded-lg shadow hover:bg-primary-dark focus:outline-none"
          >
            Pata Mawasiliano
          </button>
        )}
      </div>

      {/* room IMAGE GALLERY */}
      <div>
        {room?.images && room.images.length > 0 ? (
          <MySwiper slides={slides} />
        ) : (
          <ImagePlaceholder />
        )}
      </div>

      {/* room DESCRIPTION */}
      <section className="mt-8">
        <h2 className="text-2xl font-semibold text-secondary-dark mb-2">
          Maelezo
        </h2>
        <p className="text-accent-gray leading-relaxed">
          {room?.description || "Hakuna maelezo yaliyopatikana"}
        </p>
      </section>

      <section className="mt-8 bg-primary text-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold text-secondary-dark mb-2">
          Mahali
        </h2>
        <p>
          <strong>Mkoa:</strong> {room?.location?.region || "Haipatikani"}
        </p>
        <p>
          <strong>Wilaya:</strong> {room?.location?.district || "Haipatikani"}
        </p>
        <p>
          <strong>Kata:</strong> {room?.location?.ward || "Haipatikani"}
        </p>
        <p>
          <strong>Mtaa:</strong> {room?.location?.street || "Haipatikani"}
        </p>
      </section>

      {/* room FEATURES */}
      <section className="mt-12 space-y-6">
        <Feature
          title="Bei"
          value={
            formatPrice(room?.price, "TZS") + " / " + room?.rental_duration
          }
        />

        <Feature title="Hali" value={room?.condition || "Haipatikani"} />
        <Feature
          title="Vitu Vilivyo Karibu"
          value={room?.nearby_facilities || "Haipatikani"}
        />
        <Feature
          title="Huduma za Umeme"
          value={room?.utilities || "Haipatikani"}
        />
        <Feature
          title="Vipengele vya Usalama"
          value={room?.security_features || "Haipatikani"}
        />
        <Feature
          title="Mifumo ya Joto/Kivuli"
          value={room?.heating_cooling_system || "Haipatikani"}
        />
        <Feature
          title="Samani"
          value={room?.furnishing_status || "Haipatikani"}
        />
      </section>
    </div>
  );
};

export default ClientRoomDetail;
