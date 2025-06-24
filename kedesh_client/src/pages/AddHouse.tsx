import { SubmitHandler, useForm, useWatch } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { HouseSchema, HouseSchemaType } from "../schemas/AddHouseSchema";
import Select from "../components/common/Select";
import {
  CATEGORY_CHOICES,
  CONDITION_CHOICES,
  FURNISHING_STATUS_CHOICES,
  HEATING_COOLING_SYSTEM_CHOICES,
  CATEGORY,
  RENTAL_DURATION_CHOICES,
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
import { fetchRegionDistrictList } from "../state/district/districtSlice";
import Message from "../components/common/Message";
import { addHouse, resetAddHouseState } from "../state/house/addHouseSlice";
import FileInput from "../components/common/FileInput";
import {
  fetchAccount,
  hideAccountMessage,
} from "../state/account/accountSlice";
import useNavigation from "../hooks/useNavigation";
import Modal from "../components/common/Modal";
import FreePlanAlert from "../components/specific/FreePlanAlert";

const AddHouse = () => {
  const { goToSubscriptionPlan } = useNavigation();
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
  const {
    detail,
    error: houseError,
    loading: houseLoading,
  } = useSelector((state: RootState) => state.addHouse);

  const {
    account,
    loading: loadingAccount,
    showMessage,
  } = useSelector((state: RootState) => state.account);

  const dispatch = useDispatch<AppDispatch>();

  const [isRegionErrorVisible, setRegionErrorVisible] = React.useState<boolean>(
    !!regionError
  );
  const [isDistrictErrorVisible, setDistrictErrorVisible] =
    React.useState<boolean>(!!districtError);
  const [isHouseErrorVisible, setHouseErrorVisible] = React.useState<boolean>(
    !!houseError
  );
  const [isHouseSuccessVisible, setHouseSuccessVisible] =
    React.useState<boolean>(!!detail);

  const {
    register,
    handleSubmit,
    formState: { errors },
    control,
    reset,
    watch,
  } = useForm<HouseSchemaType>({
    resolver: zodResolver(HouseSchema),
  });

  const selectedRegionId = useWatch({
    control,
    name: "region",
  });

  const selectedCategory: CATEGORY = watch("category");

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

  React.useEffect(() => {
    if (regionError) {
      setRegionErrorVisible(true);
    } else {
      setRegionErrorVisible(false);
    }

    if (districtError) {
      setDistrictErrorVisible(true);
    } else {
      setDistrictErrorVisible(false);
    }

    if (houseError) {
      setHouseErrorVisible(true);
    } else {
      setHouseErrorVisible(false);
    }

    if (detail) {
      setHouseSuccessVisible(true);
    } else {
      setHouseSuccessVisible(false);
    }
  }, [regionError, districtError, houseError, detail]);

  // Close handlers
  const handleRegionClose = () => setRegionErrorVisible(false);
  const handleDistrictClose = () => setDistrictErrorVisible(false);
  const handleHouseErrorClose = () => setHouseErrorVisible(false);
  const handleHouseSuccessClose = () => {
    setHouseSuccessVisible(false);
    reset();
    dispatch(resetAddHouseState());
  };

  const onSubmit: SubmitHandler<HouseSchemaType> = async (data) => {
    try {
      await dispatch(addHouse(data));
    } catch (error) {
      console.error("Error submitting house data:", error);
    }
  };

  return (
    <div className="">
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
      <Loader loading={houseLoading} label="Inapakia taarifa za mali" />

      {/* Region Error */}
      {isRegionErrorVisible && regionError && (
        <Message
          type="error"
          isOpen={isRegionErrorVisible}
          message={regionError}
          buttons={[{ label: "Hairisha", onClick: handleRegionClose }]}
          xClose={handleRegionClose}
        />
      )}

      {/* District Error */}
      {isDistrictErrorVisible && districtError && (
        <Message
          type="error"
          isOpen={isDistrictErrorVisible}
          message={districtError}
          xClose={handleDistrictClose}
        />
      )}

      {/* House Error */}
      {isHouseErrorVisible && houseError && (
        <Message
          type="error"
          title="Akaunti"
          isOpen={isHouseErrorVisible}
          message={houseError}
          xClose={handleHouseErrorClose}
        />
      )}

      {/* House Success */}
      {isHouseSuccessVisible && detail && (
        <Message
          type="success"
          title="Kupakia nyumba"
          isOpen={isHouseSuccessVisible}
          message={detail || ""}
          xClose={handleHouseSuccessClose}
        />
      )}

      <Card className="w-full">
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
            <Select
              label="Aina"
              options={CATEGORY_CHOICES}
              register={register("category")}
              error={errors.category?.message}
            />

            <Select
              label="Hali"
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
              label="Mfumo wa Kupasha joto au Baridi"
              options={HEATING_COOLING_SYSTEM_CHOICES}
              register={register("heating_cooling_system")}
              error={errors.heating_cooling_system?.message}
            />

            <Select
              label="Hali ya Samani"
              options={FURNISHING_STATUS_CHOICES}
              register={register("furnishing_status")}
              error={errors.furnishing_status?.message}
            />

            <TextInput
              label="Bei ya Nyumba"
              type="number"
              placeholder="Bei"
              register={register("price")}
              error={errors.price?.message}
            />

            {selectedCategory === CATEGORY.RENTAL && (
              <Select
                label="Muda wa Kukodi"
                options={RENTAL_DURATION_CHOICES}
                register={register("rental_duration")}
                error={errors.rental_duration?.message}
              />
            )}

            <TextInput
              label="Idadi ya Vyumba vya Kulala"
              type="number"
              placeholder="Vyumba vya kulala"
              register={register("total_bed_room")}
              error={errors.total_bed_room?.message}
            />

            <TextInput
              label="Idadi ya sebure"
              type="number"
              placeholder="Sebure"
              register={register("total_dining_room")}
              error={errors.total_dining_room?.message}
            />

            <TextInput
              label="Idadi ya Vyumba vya Bafu"
              type="number"
              placeholder="Vyumba vya bafu"
              register={register("total_bath_room")}
              error={errors.total_bath_room?.message}
            />

            <Select
              options={regions.map((region) => ({
                value: region.region_id,
                label: region.name,
              }))}
              label="Chagua Mikoa"
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
              placeholder="Maelezo ya nyumba"
              error={errors.description?.message}
            />

            <TextArea
              register={register("utilities")}
              label="Huduma, mfano, maji, Umeme..."
              placeholder="Huduma"
              error={errors.utilities?.message}
            />

            <TextArea
              register={register("nearby_facilities")}
              label="Vitu vilivyo karibu, mfano, Shule..."
              placeholder="Vitu vilivyo karibu"
              error={errors.nearby_facilities?.message}
            />
          </div>

          <div className="mt-6">
            <Button
              disabled={houseLoading}
              isLoading={houseLoading}
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

export default AddHouse;
