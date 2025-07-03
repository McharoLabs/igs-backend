/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { type SubmitHandler, useForm, useWatch } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { RoomSchema, type RoomSchemaType } from "../schemas/RoomShema";
import {
  CONDITION_CHOICES,
  FURNISHING_STATUS_CHOICES,
  HEATING_COOLING_SYSTEM_CHOICES,
  RENTAL_DURATION_CHOICES,
  ROOM_CATEGORY_CHOICES,
  SECURITY_FEATURES_CHOICES,
} from "../types/enums";
import { useDispatch, useSelector } from "react-redux";
import type { AppDispatch, RootState } from "../state/store";
import React from "react";
import { fetchRegionList, resetRegionState } from "../state/region/regionSlice";
import {
  fetchRegionDistrictList,
  resetDistrictState,
} from "../state/district/districtSlice";
import { resetRegistrationState } from "../state/registration/registrationSlice";
import { addRoom, resetAddRoomState } from "../state/room/AddRoomSlice";
import useNavigation from "../hooks/useNavigation";
import {
  fetchAccount,
  hideAccountMessage,
} from "../state/account/accountSlice";
import {
  Bed,
  MapPin,
  Camera,
  DollarSign,
  Shield,
  Thermometer,
  Calendar,
  FileText,
  Zap,
  Building,
  AlertCircle,
  CheckCircle,
  Loader2,
  Home,
  Settings,
} from "lucide-react";
import { MdChevronRight } from "react-icons/md";

const AddRoom = () => {
  const { goToSubscriptionPlan, goToProfile, goToDashboard, goToRoomList } =
    useNavigation();

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
    <div className="min-h-screen bg-body py-8 px-4">
      <div className="max-w-6xl mx-auto px-5 py-14">
        {/* Loading Overlays */}
        {(loadingAccount || regionLoading || districtLoading || loading) && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 flex items-center space-x-3">
              <Loader2 className="h-6 w-6 animate-spin text-primary" />
              <span className="text-secondary font-medium">
                {loadingAccount && "Inatafuta tarifa za akaunti yako"}
                {regionLoading && "Inatafuta mikoa"}
                {districtLoading && "Inatafuta wilaya"}
                {loading && "Inapakia taarifa za chumba"}
              </span>
            </div>
          </div>
        )}

        {/* Free Plan Modal */}
        {showMessage && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-blue-50 rounded-lg p-6 max-w-md mx-4">
              <div className="text-center">
                <AlertCircle className="h-12 w-12 text-blue-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-secondary mb-2">
                  Mpango wa Bure
                </h3>
                <p className="text-gray-600 mb-6">
                  Bonyeza hapa kupata mpango wa malipo
                </p>
                <div className="flex space-x-3">
                  <button
                    onClick={goToSubscriptionPlan}
                    className="flex-1 bg-primary text-white py-2 px-4 rounded-lg hover:bg-primary-dark transition-colors"
                  >
                    Nenda Mpango
                  </button>
                  <button
                    onClick={() => dispatch(hideAccountMessage())}
                    className="flex-1 bg-gray-200 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors"
                  >
                    Funga
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Error Messages */}
        {regionError && (
          <div className="fixed top-4 right-4 bg-red-50 border border-red-200 rounded-lg p-4 max-w-md z-40">
            <div className="flex items-start">
              <AlertCircle className="h-5 w-5 text-red-500 mt-14 mr-3" />
              <div className="flex-1">
                <p className="text-red-800">{regionError}</p>
                <button
                  onClick={() => dispatch(resetRegistrationState())}
                  className="text-red-600 hover:text-red-800 text-sm mt-1"
                >
                  Funga
                </button>
              </div>
            </div>
          </div>
        )}

        {districtError && (
          <div className="fixed top-4 right-4 bg-red-50 border border-red-200 rounded-lg p-4 max-w-md z-40">
            <div className="flex items-start">
              <AlertCircle className="h-5 w-5 text-red-500 mt-14 mr-3" />
              <div className="flex-1">
                <p className="text-red-800">{districtError}</p>
                <button
                  onClick={() => dispatch(resetDistrictState())}
                  className="text-red-600 hover:text-red-800 text-sm mt-1"
                >
                  Funga
                </button>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="fixed top-4 right-4 bg-red-50 border border-red-200 rounded-lg p-4 max-w-md z-40">
            <div className="flex items-start">
              <AlertCircle className="h-5 w-5 text-red-500 mt-14 mr-3" />
              <div className="flex-1">
                <p className="text-red-800">{error}</p>
                <div className="flex space-x-2 mt-3">
                  <button
                    onClick={() => dispatch(resetAddRoomState())}
                    className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600 transition-colors"
                  >
                    Sitisha
                  </button>
                  {statusCode === 403 && (
                    <button
                      onClick={goToProfile}
                      className="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600 transition-colors"
                    >
                      Activate
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Success Message */}
        {detail && (
          <div className="fixed top-4 right-4 bg-green-50 border border-green-200 rounded-lg p-4 max-w-md z-40">
            <div className="flex items-start">
              <CheckCircle className="h-5 w-5 text-green-500 mt-14 mr-3" />
              <div className="flex-1">
                <p className="text-green-800">{detail}</p>
                <button
                  onClick={() => {
                    reset();
                    dispatch(resetAddRoomState());
                  }}
                  className="text-green-600 hover:text-green-800 text-sm mt-1"
                >
                  Funga
                </button>
              </div>
            </div>
          </div>
        )}

        <nav className="text-sm text-primary flex items-center space-x-1 mb-8">
          <span
            className="hover:underline hover:text-blue-600 cursor-pointer"
            onClick={() => goToDashboard()}
          >
            Dashibodi
          </span>
          <MdChevronRight className="text-lg" />
          <span
            className="hover:underline hover:text-blue-600 cursor-pointer"
            onClick={() => goToRoomList()}
          >
            Mali Zangu
          </span>
          <MdChevronRight className="text-lg" />
          <span className="font-medium text-gray-600">Ongeza Mali</span>
        </nav>

        {/* Main Form */}

        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-primary to-primary-light p-6">
            <div className="flex items-center space-x-3">
              <Bed className="h-8 w-8 text-white" />
              <div>
                <h1 className="text-2xl font-bold text-white">
                  Ongeza Chumba Chako
                </h1>
                <p className="text-green-100">
                  Jaza fomu hii kuongeza chumba chako
                </p>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="p-6">
            {/* Room Details Section */}
            <div className="mb-8">
              <div className="flex items-center space-x-2 mb-4">
                <Bed className="h-5 w-5 text-primary" />
                <h2 className="text-lg font-semibold text-secondary">
                  Taarifa za Chumba
                </h2>
              </div>
              <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
                <FormSelect
                  label="Aina ya Chumba"
                  icon={<Bed className="h-4 w-4" />}
                  options={ROOM_CATEGORY_CHOICES}
                  register={register("room_category")}
                  error={errors.room_category?.message}
                />
                <FormSelect
                  label="Hali ya Chumba"
                  icon={<Settings className="h-4 w-4" />}
                  options={CONDITION_CHOICES}
                  register={register("condition")}
                  error={errors.condition?.message}
                />
                <FormInput
                  label="Bei ya Chumba"
                  type="number"
                  placeholder="Bei"
                  icon={<DollarSign className="h-4 w-4" />}
                  register={register("price")}
                  error={errors.price?.message}
                />
                <FormSelect
                  label="Muda wa Kukodisha"
                  icon={<Calendar className="h-4 w-4" />}
                  options={RENTAL_DURATION_CHOICES}
                  register={register("rental_duration")}
                  error={errors.rental_duration?.message}
                />
              </div>
            </div>

            {/* Features Section */}
            <div className="mb-8">
              <div className="flex items-center space-x-2 mb-4">
                <Shield className="h-5 w-5 text-primary" />
                <h2 className="text-lg font-semibold text-secondary">
                  Vipengele vya Chumba
                </h2>
              </div>
              <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
                <FormSelect
                  label="Vipengele vya Usalama"
                  icon={<Shield className="h-4 w-4" />}
                  options={SECURITY_FEATURES_CHOICES}
                  register={register("security_features")}
                  error={errors.security_features?.message}
                />
                <FormSelect
                  label="Mfumo wa Joto au Baridi"
                  icon={<Thermometer className="h-4 w-4" />}
                  options={HEATING_COOLING_SYSTEM_CHOICES}
                  register={register("heating_cooling_system")}
                  error={errors.heating_cooling_system?.message}
                />
                <FormSelect
                  label="Hali ya Fanicha"
                  icon={<Home className="h-4 w-4" />}
                  options={FURNISHING_STATUS_CHOICES}
                  register={register("furnishing_status")}
                  error={errors.furnishing_status?.message}
                />
              </div>
            </div>

            {/* Location Section */}
            <div className="mb-8">
              <div className="flex items-center space-x-2 mb-4">
                <MapPin className="h-5 w-5 text-primary" />
                <h2 className="text-lg font-semibold text-secondary">Mahali</h2>
              </div>
              <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-4">
                <FormSelect
                  label="Chagua Kanda"
                  icon={<MapPin className="h-4 w-4" />}
                  options={regions.map((region) => ({
                    value: region.region_id,
                    label: region.name,
                  }))}
                  register={register("region")}
                  error={errors.region?.message}
                />
                <FormSelect
                  label="Chagua Wilaya"
                  icon={<MapPin className="h-4 w-4" />}
                  options={districts.map((district) => ({
                    value: district.district_id,
                    label: district.name,
                  }))}
                  register={register("district")}
                  error={errors.district?.message}
                />
                <FormInput
                  label="Kata"
                  placeholder="Kata"
                  icon={<MapPin className="h-4 w-4" />}
                  register={register("ward")}
                  error={errors.ward?.message}
                />
                <FormInput
                  label="Mtaa"
                  placeholder="Mtaa"
                  icon={<MapPin className="h-4 w-4" />}
                  register={register("street")}
                  error={errors.street?.message}
                />
              </div>
            </div>

            {/* Images Section */}
            <div className="mb-8">
              <div className="flex items-center space-x-2 mb-4">
                <Camera className="h-5 w-5 text-primary" />
                <h2 className="text-lg font-semibold text-secondary">
                  Picha za Chumba
                </h2>
              </div>
              <FormFileInput
                label="Picha za Chumba"
                register={register("images")}
                error={errors.images?.message}
                multiple={true}
              />
            </div>

            {/* Description Section */}
            <div className="mb-8">
              <div className="flex items-center space-x-2 mb-4">
                <FileText className="h-5 w-5 text-primary" />
                <h2 className="text-lg font-semibold text-secondary">
                  Maelezo ya Chumba
                </h2>
              </div>
              <div className="grid md:grid-cols-1 gap-4">
                <FormTextArea
                  label="Maelezo ya Chumba"
                  placeholder="Maelezo ya chumba"
                  register={register("description")}
                  error={errors.description?.message}
                />
                <div className="grid md:grid-cols-2 gap-4">
                  <FormTextArea
                    label="Huduma (mfano: maji, umeme...)"
                    placeholder="Huduma"
                    icon={<Zap className="h-4 w-4" />}
                    register={register("utilities")}
                    error={errors.utilities?.message}
                  />
                  <FormTextArea
                    label="Vifaa vya Karibu (mfano: shule...)"
                    placeholder="Vifaa vya Karibu"
                    icon={<Building className="h-4 w-4" />}
                    register={register("nearby_facilities")}
                    error={errors.nearby_facilities?.message}
                  />
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={loading}
                className="bg-gradient-to-r from-primary to-primary-light text-white px-8 py-3 rounded-lg font-semibold hover:from-primary-dark hover:to-primary transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    <span>Inatuma...</span>
                  </>
                ) : (
                  <>
                    <CheckCircle className="h-5 w-5" />
                    <span>Tuma Chumba</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

// Form Components (Reusable)
const FormInput = ({ label, icon, register, error, ...props }: any) => (
  <div className="space-y-2">
    <label className="block text-sm font-medium text-secondary">
      <div className="flex items-center space-x-2">
        {icon && <span className="text-primary">{icon}</span>}
        <span>{label}</span>
      </div>
    </label>
    <input
      {...register}
      {...props}
      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors ${
        error ? "border-red-300 bg-red-50" : "border-gray-300 bg-white"
      }`}
    />
    {error && (
      <p className="text-red-600 text-sm flex items-center space-x-1">
        <AlertCircle className="h-4 w-4" />
        <span>{error}</span>
      </p>
    )}
  </div>
);

const FormSelect = ({ label, icon, options, register, error }: any) => (
  <div className="space-y-2">
    <label className="block text-sm font-medium text-secondary">
      <div className="flex items-center space-x-2">
        {icon && <span className="text-primary">{icon}</span>}
        <span>{label}</span>
      </div>
    </label>
    <select
      {...register}
      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors ${
        error ? "border-red-300 bg-red-50" : "border-gray-300 bg-white"
      }`}
    >
      <option value="">Chagua...</option>
      {options.map((option: any) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
    {error && (
      <p className="text-red-600 text-sm flex items-center space-x-1">
        <AlertCircle className="h-4 w-4" />
        <span>{error}</span>
      </p>
    )}
  </div>
);

const FormTextArea = ({ label, icon, register, error, ...props }: any) => (
  <div className="space-y-2">
    <label className="block text-sm font-medium text-secondary">
      <div className="flex items-center space-x-2">
        {icon && <span className="text-primary">{icon}</span>}
        <span>{label}</span>
      </div>
    </label>
    <textarea
      {...register}
      {...props}
      rows={4}
      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors resize-none ${
        error ? "border-red-300 bg-red-50" : "border-gray-300 bg-white"
      }`}
    />
    {error && (
      <p className="text-red-600 text-sm flex items-center space-x-1">
        <AlertCircle className="h-4 w-4" />
        <span>{error}</span>
      </p>
    )}
  </div>
);

const FormFileInput = ({ label, register, error, multiple }: any) => (
  <div className="space-y-2">
    <label className="block text-sm font-medium text-secondary">
      <div className="flex items-center space-x-2">
        <Camera className="h-4 w-4 text-primary" />
        <span>{label}</span>
      </div>
    </label>
    <div
      className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
        error
          ? "border-red-300 bg-red-50"
          : "border-gray-300 hover:border-primary"
      }`}
    >
      <Camera className="h-12 w-12 text-gray-400 mx-auto mb-4" />
      <input
        {...register}
        type="file"
        multiple={multiple}
        accept="image/*"
        className="hidden"
        id="room-file-upload"
      />
      <label
        htmlFor="room-file-upload"
        className="cursor-pointer text-primary hover:text-primary-dark font-medium"
      >
        Bonyeza hapa kupakia picha za chumba
      </label>
      <p className="text-gray-500 text-sm mt-2">PNG, JPG hadi 8MB kila moja</p>
    </div>
    {error && (
      <p className="text-red-600 text-sm flex items-center space-x-1">
        <AlertCircle className="h-4 w-4" />
        <span>{error}</span>
      </p>
    )}
  </div>
);

export default AddRoom;
