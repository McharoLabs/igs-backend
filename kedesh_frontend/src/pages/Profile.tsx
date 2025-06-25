import React from "react";
import Message from "../components/common/Message";
import Loader from "../components/common/Loader";
import Modal from "../components/common/Modal";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import apiClient from "../api/apiClient";
import { endpoints } from "../api/endpoints";
import { PlanType } from "../types/accountType";
import { fetchAccount } from "../state/account/accountSlice";
import { SubmitHandler, useForm } from "react-hook-form";
import { SubscribeSchema, SubscribeSchemaType } from "../schemas/Subscribe";
import { zodResolver } from "@hookform/resolvers/zod";
import TextInput from "../components/common/InputText";
import Button from "../components/common/Button";
import { resetSubscribe, subscribe } from "../state/account/subscribeSlice";
import { formatDate } from "../utils/dateUtils";
import { fetchPlanList } from "../state/account/planSlice";

const Profile = () => {
  const { user, tokens } = useSelector((state: RootState) => state.auth);
  const { plans } = useSelector((state: RootState) => state.plan);
  const { account, loading: loadingAccount } = useSelector(
    (state: RootState) => state.account
  );
  const {
    detail,
    error: subscribeError,
    loading: loadingSubscribe,
  } = useSelector((state: RootState) => state.subscribe);
  const [avatarUrl, setAvatarUrl] = React.useState<string | null>(null);

  const [selectedPlan, setSelectedPlan] = React.useState<PlanType | null>(null);
  const [isModalOpen, setIsModalOpen] = React.useState(false);

  const dispatch = useDispatch<AppDispatch>();

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    reset,
  } = useForm<SubscribeSchemaType>({
    resolver: zodResolver(SubscribeSchema),
  });

  const handlePlanSelect = (plan: PlanType) => {
    setValue("plan_id", plan.subscription_plan_id);
    setSelectedPlan(plan);
    setIsModalOpen(true);
  };

  const handlePayment: SubmitHandler<SubscribeSchemaType> = async (data) => {
    setIsModalOpen(false);
    try {
      await dispatch(subscribe(data));
    } catch (error) {
      console.error(error);
    }
  };

  const handleCloseMessage = () => {
    reset();
    dispatch(resetSubscribe());
  };

  React.useEffect(() => {
    if (!account) {
      dispatch(fetchAccount());
    }
  }, [account, dispatch]);

  React.useEffect(() => {
    if (plans.length === 0) {
      dispatch(fetchPlanList());
    }
  }, [dispatch, plans.length]);

  React.useEffect(() => {
    const fetchAvatar = async () => {
      try {
        const response = await apiClient.get(endpoints.avatar, {
          responseType: "blob",
          headers: {
            Authorization: `Bearer ${tokens.access}`,
          },
        });
        const imageUrl = URL.createObjectURL(response.data);
        setAvatarUrl(imageUrl);
      } catch (error) {
        console.error("Error fetching avatar:", error);
        setAvatarUrl(null);
      }
    };

    if (!avatarUrl) {
      fetchAvatar();
    }
  }, [avatarUrl, tokens.access]);

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      {/* Profile Header */}
      <div className="text-center mb-8">
        <img
          src={`${avatarUrl}`}
          alt="Profile"
          className="w-32 h-32 rounded-full mx-auto object-cover"
        />
        <h1 className="text-3xl font-bold mt-4">{user.full_name}</h1>
        <p className="text-lg text-gray-500">Kedesh Agent</p>
      </div>

      {/* Sehemu ya Hali ya Akaunti */}
      <section className="mb-8 pb-8 border-b border-gray-300">
        <h2 className="text-2xl font-semibold text-green-600 mb-4">
          Hali ya Akaunti
        </h2>
        {account?.is_active ? (
          <p className="text-lg text-green-600">
            Akaunti yako imewashwa! Sasa unaweza kupakia mali.
          </p>
        ) : (
          <p className="text-lg text-red-600">
            Akaunti yako haijawashwa. Tafadhali washa akaunti yako ili kupakia
            mali.
          </p>
        )}
      </section>

      {/* Subscription Plan Details */}
      {account?.is_active && (
        <section className="mb-8 pb-8 border-b border-gray-300">
          <h2 className="text-2xl font-semibold text-green-600 mb-6">
            Mpango Wako wa Sasa
          </h2>
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-semibold text-gray-900">
                {account.plan.name}
              </h3>
              <p className="text-lg text-gray-700">{account.plan.price}</p>
            </div>

            <div className="space-y-1">
              <p className="text-sm text-gray-500">
                <strong>Idadi ya nyumba:</strong> {account.plan.max_houses}
              </p>
              <p className="text-sm text-gray-500">
                <strong>Muda wa Mpango:</strong> {account.plan.duration_days}{" "}
                siku
              </p>
            </div>

            <div className="space-y-1">
              <p className="text-sm text-gray-500">
                <strong>Tarehe ya Kuanza Mpango:</strong>{" "}
                {formatDate(account.start_date)}
              </p>
              <p className="text-sm text-gray-500">
                <strong>Tarehe ya Kumaliza Mpango:</strong>{" "}
                {formatDate(account.end_date)}
              </p>
            </div>
          </div>
        </section>
      )}

      {/* Divider for better separation */}
      <section className="mb-8 pb-8 border-b border-gray-300">
        <h2 className="text-2xl font-semibold text-green-600 mb-4">
          Chagua plani ili mali zako zipewe kipaumbele
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {plans.map((plan, index) => (
            <div
              key={index}
              className="p-6 bg-gray-100 rounded-lg shadow-lg hover:bg-gray-200 cursor-pointer"
              onClick={() => handlePlanSelect(plan)}
            >
              <h3 className="text-xl font-semibold">{plan.name}</h3>
              <p className="text-lg text-gray-700">{plan.price}</p>
              <p className="text-sm text-gray-500">
                Idadi ya mali: {plan.max_houses}
              </p>
              <p className="text-sm text-gray-500">
                Muda wa plani: Siku {plan.duration_days}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Message Modal for successful payment */}
      {detail && (
        <Message
          isOpen={!!detail}
          message={detail}
          type="success"
          xClose={handleCloseMessage}
        />
      )}

      {subscribeError && (
        <Message
          isOpen={!!subscribeError}
          message={subscribeError}
          type="error"
          xClose={handleCloseMessage}
        />
      )}

      {/* Loader */}
      <Loader label="Inatafuta plani..." loading={loadingSubscribe} />
      <Loader label="Inatafuta taarifa..." loading={loadingAccount} />

      {/* Payment Confirmation Modal */}
      <Modal
        isOpen={isModalOpen}
        title={`Confirm Payment for ${selectedPlan?.name}`}
      >
        <form onSubmit={handleSubmit(handlePayment)}>
          {errors.plan_id?.message && (
            <div className="rounded-md bg-red-500 p-4 text-white">
              {errors.plan_id.message}
            </div>
          )}
          <p>
            Do you want to proceed with the payment of {selectedPlan?.price}?
          </p>

          <TextInput
            className="mt-6"
            type="tel"
            error={errors.phone_number?.message}
            register={register("phone_number")}
            label="Payment phone number"
          />

          <div className="flex gap-4 justify-end mt-6">
            <Button
              type={"button"}
              onClick={() => setIsModalOpen(false)}
              className="bg-red-500 hover:bg-red-400"
            >
              Cancel
            </Button>

            <Button type={"submit"} className="bg-green-500 hover:bg-green-400">
              Submit
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Profile;
