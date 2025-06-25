import { SubmitHandler, useForm, useWatch } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Select from "../components/common/Select";
import {
  CONDITION_CHOICES,
  FURNISHING_STATUS_CHOICES,
  HEATING_COOLING_SYSTEM_CHOICES,
  RENTAL_DURATION_CHOICES,
  ROOM_CATEGORY_CHOICES,
  SECURITY_FEATURES_CHOICES,
} from "../types/enums";
import TextInput from "../components/common/InputText";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import TextArea from "../components/common/TextArea";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import React from "react";
import { fetchRegionList, resetRegionState } from "../state/region/regionSlice";
import Loader from "../components/common/Loader";
import {
  fetchRegionDistrictList,
  resetDistrictState,
} from "../state/district/districtSlice";
import Message from "../components/common/Message";
import FileInput from "../components/common/FileInput";
import { RoomSchema, RoomSchemaType } from "../schemas/RoomShema";
import { resetRegistrationState } from "../state/registration/registrationSlice";
import { addRoom, resetAddRoomState } from "../state/room/AddRoomSlice";
import useNavigation from "../hooks/useNavigation";
import {
  fetchAccount,
  hideAccountMessage,
} from "../state/account/accountSlice";
import Modal from "../components/common/Modal";
import FreePlanAlert from "../components/specific/FreePlanAlert";

const AddRoom = () => {
  const { goToSubscriptionPlan, goToProfile } = useNavigation();
  const {
    loading: regionLoading,
    regions,
    error: regionError,
  } = useSelector((state: RootState) => state.region);
  const {
    loading: districtLoading,
    districts,
    error: districtError,
  } = useSelector((state: RootState) => state.district);

  const { detail, error, loading, statusCode } = useSelector(
    (state: RootState) => state.addRoom
  );

  const {
    account,
    loading: loadingAccount,
    showMessage,
  } = useSelector((state: RootState) => state.account);

  const dispatch = useDispatch<AppDispatch>();

  const {
    register,
    handleSubmit,
    formState: { errors },
    control,
    reset,
  } = useForm<RoomSchemaType>({
    resolver: zodResolver(RoomSchema),
  });

  const selectedRegionId = useWatch({
    control,
    name: "region",
  });

  React.useEffect(() => {
    if (!account) {
      dispatch(fetchAccount());
    }
  }, [account, dispatch]);

  React.useEffect(() => {
    dispatch(fetchRegionList());

    return () => {
      dispatch(resetRegionState());
    };
  }, [dispatch]);

  React.useEffect(() => {
    if (selectedRegionId) {
      dispatch(fetchRegionDistrictList(selectedRegionId));
    }
  }, [dispatch, selectedRegionId]);

  const onSubmit: SubmitHandler<RoomSchemaType> = async (data) => {
    try {
      await dispatch(addRoom(data));
    } catch (error) {
      console.error("Error submitting Room data:", error);
    }
  };

  return (
    <div>
      <Loader
        loading={loadingAccount}
        label="Inatafuta tarifa za akaunti yako"
      />

      <Modal isOpen={showMessage} className="bg-blue-100">
        <FreePlanAlert
          onSubmit={goToSubscriptionPlan}
          onCancel={() => dispatch(hideAccountMessage())}
        />
      </Modal>

      <Loader loading={regionLoading} label="Inatafuta mikoa" />
      <Loader loading={districtLoading} label="Inatafuta wilaya" />
      <Loader loading={loading} label="Inapakia taarifa za chumba" />

      <Message
        type="error"
        isOpen={!!regionError}
        message={regionError || ""}
        xClose={() => dispatch(resetRegistrationState())}
      />

      {/* District Error */}
      <Message
        type="error"
        isOpen={!!districtError}
        message={districtError || ""}
        xClose={() => dispatch(resetDistrictState())}
      />

      <Message
        type="error"
        isOpen={!!error}
        message={error || ""}
        buttons={[
          {
            label: "Sitisha",
            style: "bg-red-500 text-white",
            onClick: () => dispatch(resetAddRoomState()),
          },
          ...(statusCode === 403
            ? [
                {
                  label: "Activate",
                  onClick: goToProfile,
                  style: "bg-green-500 text-white",
                },
              ]
            : []),
        ]}
        xClose={() => dispatch(resetAddRoomState())}
      />

      <Message
        type="success"
        isOpen={!!detail}
        message={detail || ""}
        xClose={() => {
          reset();
          dispatch(resetAddRoomState());
        }}
      />

      <Card className="w-full">
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
            <Select
              label="Aina ya Chumba"
              options={ROOM_CATEGORY_CHOICES}
              register={register("room_category")}
              error={errors.room_category?.message}
            />

            <Select
              label="Hali ya Chumba"
              options={CONDITION_CHOICES}
              register={register("condition")}
              error={errors.condition?.message}
            />

            <Select
              label="Vipengele vya Usalama"
              options={SECURITY_FEATURES_CHOICES}
              register={register("security_features")}
              error={errors.security_features?.message}
            />

            <Select
              label="Mfumo wa Joto au Baridi"
              options={HEATING_COOLING_SYSTEM_CHOICES}
              register={register("heating_cooling_system")}
              error={errors.heating_cooling_system?.message}
            />

            <Select
              label="Hali ya Fanicha"
              options={FURNISHING_STATUS_CHOICES}
              register={register("furnishing_status")}
              error={errors.furnishing_status?.message}
            />

            <TextInput
              label="Bei ya Chumba"
              type="number"
              placeholder="Bei"
              register={register("price")}
              error={errors.price?.message}
            />

            <Select
              label="Muda wa Kukodisha"
              options={RENTAL_DURATION_CHOICES}
              register={register("rental_duration")}
              error={errors.rental_duration?.message}
            />

            <Select
              options={regions.map((region) => ({
                value: region.region_id,
                label: region.name,
              }))}
              label="Chagua Kanda"
              register={register("region")}
              error={errors.region?.message}
            />

            <Select
              options={districts.map((district) => ({
                value: district.district_id,
                label: district.name,
              }))}
              label="Chagua Wilaya"
              register={register("district")}
              error={errors.district?.message}
            />

            <TextInput
              label="Kata"
              placeholder="Kata"
              register={register("ward")}
              error={errors.ward?.message}
            />

            <TextInput
              label="Mtaa"
              placeholder="Mtaa"
              register={register("street")}
              error={errors.street?.message}
            />

            <FileInput
              label="Picha"
              error={errors.images?.message}
              register={register("images")}
              multiple={true}
            />

            <TextArea
              register={register("description")}
              label="Maelezo"
              placeholder="Maelezo ya chumba"
              error={errors.description?.message}
            />

            <TextArea
              register={register("utilities")}
              label="Huduma. eg., maji, Umeme..."
              placeholder="Huduma"
              error={errors.utilities?.message}
            />

            <TextArea
              register={register("nearby_facilities")}
              label="Vifaa vya Karibu. eg., Shule..."
              placeholder="Vifaa vya Karibu"
              error={errors.nearby_facilities?.message}
            />
          </div>

          <div className="mt-6">
            <Button
              disabled={loading}
              isLoading={loading}
              type="submit"
              className="w-full"
            >
              Tuma
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default AddRoom;
