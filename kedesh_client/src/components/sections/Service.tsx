import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchPlanList, resetPlanState } from "../../state/account/planSlice";
import { AppDispatch, RootState } from "../../state/store";
import Message from "../common/Message";

const ServiceSection: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { plans, loading, error } = useSelector(
    (state: RootState) => state.plan
  );

  React.useEffect(() => {
    if (plans.length === 0) {
      dispatch(fetchPlanList());
    }
  }, [dispatch, plans.length]);

  return (
    <div className="max-w-7xl mx-auto px-6 py-8 space-y-10">
      {/* Sehemu ya Kwa Nini Utuchague */}
      <div className="mx-auto text-left">
        <h2 className="text-3xl font-bold text-primary mb-8 text-center">
          Kwa Nini Utuchague?
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="flex flex-col items-center text-center">
            <div className="bg-accent-yellow text-white w-14 h-14 rounded-full flex items-center justify-center text-lg">
              1
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-800">
              Ufikio Mkubwa
            </h3>
            <p className="text-gray-600 text-sm mt-2">
              Mali zako zitaonekana kwa maelfu ya wapangaji na wanunuzi nchini.
            </p>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="bg-accent-yellow text-white w-14 h-14 rounded-full flex items-center justify-center text-lg">
              2
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-800">
              Usimamizi Rahisi
            </h3>
            <p className="text-gray-600 text-sm mt-2">
              Tumia dashibodi yetu kudhibiti mali zako kwa urahisi popote ulipo.
            </p>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="bg-accent-yellow text-white w-14 h-14 rounded-full flex items-center justify-center text-lg">
              3
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-800">
              Bei Nafuu na Kubadilika
            </h3>
            <p className="text-gray-600 text-sm mt-2">
              Tuna mpango kwa kila bajeti — chagua unachokimudu na kilicho bora
              kwako.
            </p>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="bg-accent-yellow text-white w-14 h-14 rounded-full flex items-center justify-center text-lg">
              4
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-800">
              Msaada wa Haraka Saa 24
            </h3>
            <p className="text-gray-600 text-sm mt-2">
              Timu yetu ipo tayari kukusaidia saa yoyote ukiwa na changamoto.
            </p>
          </div>
        </div>
      </div>

      {/* Kichwa Kikuu */}
      <h1 className="text-4xl font-bold text-primary mb-4 text-center">
        Mipango ya Bei Inayokidhi Mahitaji Yako
      </h1>
      <p className="text-xl text-secondary mb-12 text-center">
        Tunatoa mipango inayofaa kwa wakala na wamiliki wa mali, iwe ni ya
        nyumba, vyumba, au mashamba.
      </p>

      {loading ? (
        <div></div>
      ) : error ? (
        <Message
          isOpen={!!error}
          message={error}
          xClose={() => dispatch(resetPlanState())}
          type="info"
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {plans.map((plan) => (
            <div
              key={plan.subscription_plan_id}
              className="bg-white shadow-lg rounded-lg overflow-hidden transition-all hover:scale-105 hover:shadow-2xl"
            >
              {/* Jina la Mpango */}
              <div className="bg-secondary-light text-white p-6">
                <h2 className="text-2xl font-semibold">{plan.name}</h2>
              </div>

              {/* Maelezo ya Mpango */}
              <div className="p-6 text-left space-y-4">
                <p className="text-3xl font-bold text-accent-coral">
                  {plan.price} Tzs
                </p>
                <ul className="text-sm text-accent-gray space-y-2">
                  <li>
                    <span className="font-semibold text-secondary">
                      Mali Zinazoruhusiwa:
                    </span>{" "}
                    {plan.max_houses}
                  </li>
                  <li>
                    <span className="font-semibold text-secondary">
                      Muda wa Matumizi:
                    </span>{" "}
                    {plan.duration_days} siku
                  </li>
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* How It Works Section */}
      <div className="mx-auto px-6 text-center">
        <h2 className="text-2xl sm:text-3xl md:text-4xl text-primary mb-12">
          Jinsi Tunavyofanya Kazi
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="flex flex-col items-center text-center">
            <div className="bg-primary text-white w-14 h-14 rounded-full flex items-center justify-center text-lg">
              1
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-800">
              Tafuta Mali
            </h3>
            <p className="text-gray-600 text-sm mt-2">
              Tumia mfumo wetu kutafuta nyumba, vyumba, au mashamba.
            </p>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="bg-primary text-white w-14 h-14 rounded-full flex items-center justify-center text-lg">
              2
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-800">
              Wasiliana Moja kwa Moja
            </h3>
            <p className="text-gray-600 text-sm mt-2">
              Wasiliana na mmiliki au wakala bila mtu wa kati.
            </p>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="bg-primary text-white w-14 h-14 rounded-full flex items-center justify-center text-lg">
              3
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-800">
              Tembelea Mali
            </h3>
            <p className="text-gray-600 text-sm mt-2">
              Pata nafasi ya kuona mali kabla ya kufanya maamuzi.
            </p>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="bg-primary text-white w-14 h-14 rounded-full flex items-center justify-center text-lg">
              4
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-800">
              Fanya Uamuzi
            </h3>
            <p className="text-gray-600 text-sm mt-2">
              Kamilisha makubaliano kwa haraka na salama.
            </p>
          </div>
        </div>
      </div>

      {/* Ushuhuda kutoka kwa Wateja */}
      <div className="text-center mt-16">
        <h2 className="text-2xl sm:text-3xl text-primary mb-6 font-bold">
          Ushuhuda kutoka kwa Wateja
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded shadow-md">
            <p className="text-sm text-gray-600 italic">
              “Nilifanikiwa kuuza nyumba yangu ndani ya wiki mbili kupitia
              tovuti hii. Imekuwa msaada mkubwa!”
            </p>
            <p className="mt-4 font-semibold text-primary">
              — Fatma, Mmiliki wa Mali
            </p>
          </div>
          <div className="bg-white p-6 rounded shadow-md">
            <p className="text-sm text-gray-600 italic">
              “Kama dalali, napenda jinsi mfumo unavyonirahisishia kutangaza
              mali na kupata wateja.”
            </p>
            <p className="mt-4 font-semibold text-primary">— Musa, Dalali</p>
          </div>
          <div className="bg-white p-6 rounded shadow-md">
            <p className="text-sm text-gray-600 italic">
              “Nimepata chumba kizuri kwa bei nzuri. Ilikuwa rahisi na ya haraka
              sana.”
            </p>
            <p className="mt-4 font-semibold text-primary">— John, Mnunuzi</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ServiceSection;
