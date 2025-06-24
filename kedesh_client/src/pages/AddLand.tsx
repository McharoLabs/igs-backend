import React from "react";
import useNavigation from "../hooks/useNavigation";
import { AppDispatch, RootState } from "../state/store";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchAccount,
  hideAccountMessage,
} from "../state/account/accountSlice";
import { fetchRegionList, resetRegionState } from "../state/region/regionSlice";
import {
  fetchRegionDistrictList,
  resetDistrictState,
} from "../state/district/districtSlice";
import { SubmitHandler, useForm, useWatch } from "react-hook-form";
import { LandFormSchema, LandFormSchemaType } from "../schemas/LandSchema";
import { zodResolver } from "@hookform/resolvers/zod";
import Loader from "../components/common/Loader";
import Modal from "../components/common/Modal";
import FreePlanAlert from "../components/specific/FreePlanAlert";
import Message from "../components/common/Message";
import Card from "../components/common/Card";
import Select from "../components/common/Select";
import FileInput from "../components/common/FileInput";

import {
  LAND_TYPE_CHOICES,
  ACCESS_ROAD_TYPE_CHOICES,
  ZONING_TYPE_CHOICES,
  LAND_SIZE_UNIT_CHOICES,
} from "../types/enums";
import TextInput from "../components/common/InputText";
import TextArea from "../components/common/TextArea";
import { addLand, resetLandState } from "../state/land/landSlice";
import { MdChevronRight } from "react-icons/md";

const AddLand = () => {
  const { goToSubscriptionPlan, navigateToLand, goToDashboard } =
    useNavigation();
  const dispatch = useDispatch<AppDispatch>();

  const { detail, error, loading } = useSelector(
    (state: RootState) => state.land
  );

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
    account,
    loading: loadingAccount,
    showMessage,
  } = useSelector((state: RootState) => state.account);

  const {
    register,
    handleSubmit,
    formState: { errors },
    control,
    reset,
  } = useForm<LandFormSchemaType>({
    resolver: zodResolver(LandFormSchema),
  });

  const selectedRegionId = useWatch({
    control,
    name: "region",
  });

  React.useEffect(() => {
    if (!account) dispatch(fetchAccount());
  }, [account, dispatch]);

  React.useEffect(() => {
    dispatch(fetchRegionList());
    return () => {
      dispatch(resetRegionState());
    };
  }, [dispatch]);

  React.useEffect(() => {
    if (selectedRegionId) dispatch(fetchRegionDistrictList(selectedRegionId));
  }, [dispatch, selectedRegionId]);

  const onSubmit: SubmitHandler<LandFormSchemaType> = async (data) => {
    console.log(data);
    await dispatch(addLand(data));
  };

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
            Ardhi yangu
          </button>
          <MdChevronRight className="text-lg" />
          <span className="font-medium text-gray-600">Ardhi</span>
        </nav>

        <Loader loading={regionLoading || districtLoading || loadingAccount} />
        <Loader loading={loading} />

        <Modal isOpen={showMessage} className="bg-secondary-light">
          <FreePlanAlert
            onSubmit={goToSubscriptionPlan}
            onCancel={() => dispatch(hideAccountMessage())}
          />
        </Modal>

        <Message
          type="error"
          isOpen={!!regionError}
          message={regionError || ""}
          xClose={() => dispatch(resetRegionState())}
        />
        <Message
          type="error"
          isOpen={!!districtError}
          message={districtError || ""}
          xClose={() => dispatch(resetDistrictState())}
        />

        <Message
          type="success"
          title="Kupakia Ardhi"
          isOpen={!!detail}
          message={detail || ""}
          xClose={() => {
            reset();
            dispatch(resetLandState());
            navigateToLand();
          }}
        />

        <Message
          type="info"
          title="Kupakia Ardhi"
          isOpen={!!error}
          message={error || ""}
          xClose={() => {
            dispatch(resetLandState());
          }}
        />

        <Card className="w-full mt-8">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Select
                label="Aina ya Ardhi"
                options={LAND_TYPE_CHOICES}
                register={register("category")}
                error={errors.category?.message}
              />
              <Select
                label="Zoning Type"
                options={ZONING_TYPE_CHOICES}
                register={register("zoning_type")}
                error={errors.zoning_type?.message}
              />
              <Select
                label="Access Road"
                options={ACCESS_ROAD_TYPE_CHOICES}
                register={register("access_road_type")}
                error={errors.access_road_type?.message}
              />
              <Select
                label="Kipimo cha ukubwa"
                options={LAND_SIZE_UNIT_CHOICES}
                register={register("land_size_unit")}
                error={errors.land_size_unit?.message}
              />
              <TextInput
                label="Ukubwa wa Ardhi"
                type="number"
                placeholder="Mfano: 500"
                register={register("land_size")}
                error={errors.land_size?.message}
              />
              <TextInput
                label="Bei"
                type="number"
                placeholder="Bei"
                register={register("price")}
                error={errors.price?.message}
              />
              <TextInput
                label="Huduma za Umma"
                placeholder="Umeme, maji, n.k."
                register={register("utilities")}
                error={errors.utilities?.message}
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
                label="Maelezo ya Ardhi"
                placeholder="Elezea zaidi kuhusu ardhi..."
                register={register("description")}
                error={errors.description?.message}
              />
            </div>

            <button
              type="submit"
              className="bg-primary text-white py-2 px-4 rounded"
            >
              Tuma
            </button>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default AddLand;
