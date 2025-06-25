import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import { fetchPlanList, resetPlanState } from "../state/account/planSlice";
import { fetchAccount, resetAccount } from "../state/account/accountSlice";
import { PlanType } from "../types/accountType";
import { CreditCard } from "lucide-react";
import { SubscribeSchema, SubscribeSchemaType } from "../schemas/Subscribe";
import { SubmitHandler, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { resetSubscribe, subscribe } from "../state/account/subscribeSlice";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";
import Modal from "../components/common/Modal";
import TextInput from "../components/common/InputText";
import Button from "../components/common/Button";

const SubscriptionPlan = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { plans, loading, error } = useSelector(
    (state: RootState) => state.plan
  );
  const { account } = useSelector((state: RootState) => state.account);
  const {
    detail,
    error: subscribeError,
    loading: loadingSubscribe,
  } = useSelector((state: RootState) => state.subscribe);

  const [selectedPlan, setSelectedPlan] = React.useState<PlanType | null>(null);
  const [isModalOpen, setIsModalOpen] = React.useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    reset,
  } = useForm<SubscribeSchemaType>({
    resolver: zodResolver(SubscribeSchema),
  });

  React.useEffect(() => {
    dispatch(fetchPlanList());
    dispatch(fetchAccount()); // Fetch account details to get the current plan

    // Cleanup if component unmounts
    return () => {
      dispatch(resetPlanState());
      dispatch(resetAccount()); // Reset account state on component unmount
    };
  }, [dispatch]);

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

  if (loading) {
    return <div className="text-center p-6">Inapakia...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500 p-6">{error}</div>;
  }

  return (
    <div className="max-w-screen-xl mx-auto px-6 py-12">
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

      {/* Payment Confirmation Modal */}
      <Modal
        isOpen={isModalOpen}
        title={`Malipo ya mpangilio ${selectedPlan?.name}`}
      >
        <form onSubmit={handleSubmit(handlePayment)}>
          {errors.plan_id?.message && (
            <div className="rounded-md bg-red-500 p-4 text-white">
              {errors.plan_id.message}
            </div>
          )}
          <div className="mb-6 text-sm text-gray-600">
            <h3 className="font-semibold text-gray-700">Faida:</h3>
            <ul className="list-disc pl-5 mt-2">
              <li>Ingiza namba ya simu yakufanyia malipo</li>
              <li>Bonyeza tuma</li>
              <li>Kwenye simu yako yenye namba ya simu itakuja popup</li>
              <li>Soma kuthibitisha kua utakatwa {selectedPlan?.price}</li>
              <li>Ingiza nywila yako kuthibitisha</li>
              <li>
                Rudi kwenye tovuti hii na kuendelea kutangaza nasi, akaunti yako
                itakua tayari
              </li>
            </ul>
          </div>

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
              Ghairi
            </Button>

            <Button type={"submit"} className="bg-green-500 hover:bg-green-400">
              Tuma
            </Button>
          </div>
        </form>
      </Modal>

      <h1 className="text-4xl font-bold text-center text-primary mb-12">
        Chagua Mpango wako wa Uanachama
      </h1>

      {/* Display Current Plan Information */}
      {account && (
        <div className="bg-blue-100 p-6 rounded-lg mb-8">
          <h2 className="text-2xl font-semibold text-primary mb-4">
            Mpango Wako wa Sasa
          </h2>
          <p className="text-lg text-gray-800 mb-4">
            Mpango: <strong>{account.plan.name}</strong>
          </p>
          <p className="text-lg text-gray-800 mb-4">
            Bei:{" "}
            <strong>{`Tsh ${account.plan.price} / ${account.plan.duration_days} Siku`}</strong>
          </p>
          <p className="text-sm text-gray-600">
            Muda wa Mpango: {account.plan.duration_days} siku za upatikanaji
            bila kuingiliwa.
          </p>
        </div>
      )}

      {/* Displaying All Plans */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {plans.map((plan: PlanType) => (
          <div
            key={plan.subscription_plan_id}
            className="bg-white shadow-lg rounded-lg p-6 transition transform hover:scale-105 hover:shadow-2xl flex flex-col"
          >
            <div className="flex items-center mb-4">
              <CreditCard className="w-8 h-8 text-primary mr-3" />
              <h2 className="text-2xl font-semibold text-primary">
                {plan.name}
              </h2>
            </div>

            <div className="mb-6 text-gray-800">
              <p className="text-lg font-semibold">{`Tsh ${plan.price} / ${plan.duration_days} Siku`}</p>
              <p className="mt-2 text-sm text-gray-600">
                Muda wa Mpango: {plan.duration_days} siku za upatikanaji bila
                kuingiliwa.
              </p>
            </div>

            <div className="flex flex-col mb-4">
              <p className="text-sm text-gray-600">{`Nyumba Zaidi: ${plan.max_houses}`}</p>
              <p className="mt-2 text-sm text-gray-600">
                Kwa mpango huu, unaweza kuorodhesha hadi nyumba{" "}
                {plan.max_houses}. Inafaa kwa mashirika madogo na ya kati.
              </p>
            </div>

            {/* <div className="mb-6 text-sm text-gray-600">
              <h3 className="font-semibold text-gray-700">Faida:</h3>
              <ul className="list-disc pl-5 mt-2">
                <li>Orodha ya Kipaumbele</li>
                <li>Upatikanaji wa Vipengele vya Premium</li>
                <li>Msaada wa Wateja wa Kipekee</li>
              </ul>
            </div> */}

            <button
              className="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600 transition"
              onClick={() => handlePlanSelect(plan)}
            >
              Chagua Mpango
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SubscriptionPlan;
