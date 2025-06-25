import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import { fetchAccount } from "../state/account/accountSlice";
import { fetchPlanList } from "../state/account/planSlice";
import apiClient from "../api/apiClient";
import { endpoints } from "../api/endpoints";
import { formatPrice } from "../utils/PriceFormat";
import useNavigation from "../hooks/useNavigation";

const Dashboard = () => {
  const { navigateToRoom, navigateToHouse, navigateToLand } = useNavigation();
  const { user, tokens } = useSelector((state: RootState) => state.auth);
  const { plans } = useSelector((state: RootState) => state.plan);
  const { account, loading: loadingAccount } = useSelector(
    (state: RootState) => state.account
  );
  useSelector((state: RootState) => state.subscribe);
  const [avatarUrl, setAvatarUrl] = React.useState<string | null>(null);

  const dispatch = useDispatch<AppDispatch>();

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

  if (loadingAccount) {
    return null;
  }

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="max-w-7xl w-full px-5 py-14">
        <div className="bg-white-20 text-black/70 p-6 rounded-xl shadow-md mb-6">
          <h2 className="text-2xl font-bold mb-4">Maelezo ya Agent</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Agent Details */}
            <div className="flex items-center space-x-6 mb-6">
              <img
                src={avatarUrl ?? ""}
                alt="Agent Avatar"
                className="w-32 h-32 rounded-full ring-4 ring-white"
              />
              <div className="flex flex-col">
                <h3 className="text-md font-semibold text-black/70">
                  {`${user.full_name}`}
                </h3>
                <p className="text-sm text-black/70">{user.email}</p>
              </div>
            </div>

            {/* Plan Details */}
            {account && account.is_active ? (
              <div className="flex flex-col items-start space-y-2 mb-6">
                <p className="text-lg text-black/70">
                  <span className="font-semibold text-black">
                    Mpango wa Akaunti: {account.is_active}
                  </span>
                  {account.plan.name}
                </p>
                <p className="text-lg text-black/70">
                  <span className="font-semibold text-black">
                    Hali ya Akaunti:
                  </span>
                  {account.is_active ? "Aktivu" : "Haipo"}
                </p>
                <p className="text-lg text-black/70">
                  <span className="font-semibold text-black">
                    Muda wa Usajili:
                  </span>
                  {account.start_date} - {account?.end_date}
                </p>
                <p className="text-lg text-black/70">
                  <span className="font-semibold text-black">
                    Bei ya Mpango:
                  </span>
                  {formatPrice(account.plan.price)}
                </p>
                <p className="text-lg text-black/70">
                  <span className="font-semibold text-black">
                    Nyumba Zinazoruhusiwa:
                  </span>
                  {account.plan.max_houses}
                </p>
                <p className="text-lg text-black/70">
                  <span className="font-semibold text-black">
                    Muda wa Mpango:
                  </span>
                  {account.plan.duration_days} siku
                </p>
              </div>
            ) : (
              <p className="text-lg text-red-600">
                Akaunti yako haijawashwa. Tafadhali washa akaunti yako ili
                kupakia mali.
              </p>
            )}
          </div>
        </div>

        {/* Second Row (Flex Layout for Full Width Grow) */}
        <div className="flex flex-col md:flex-row flex-wrap gap-6">
          {/* Room Management Card */}
          <div className="bg-secondary text-white p-6 rounded-lg shadow-lg flex-1 min-w-[250px] flex flex-col items-center hover:shadow-lg hover:scale-105 duration-300">
            <h2 className="text-xl font-bold mb-2">Chumba</h2>
            <p className="text-center">
              Simamia na ongeza vyumba vyako vya kukodi kwa bei nafuu na hali
              nzuri.
            </p>
            <div className="mt-4 flex space-x-3">
              <button
                className="bg-primary text-white px-4 py-2 rounded hover:white-shadow"
                onClick={() => navigateToRoom()}
              >
                Simamia Chumba
              </button>
            </div>
          </div>

          {/* House Management Card */}
          <div className="bg-primary text-white p-6 rounded-lg shadow-lg flex-1 min-w-[250px] flex flex-col items-center hover:shadow-lg hover:scale-105 duration-300">
            <h2 className="text-xl font-bold mb-2">Nyumba</h2>
            <p className="text-center">
              Simamia nyumba zako za kukodi au kuuza. Pata wateja kwa urahisi.
            </p>
            <div className="mt-4 flex space-x-3">
              <button
                className="bg-secondary text-white px-4 py-2 rounded hover:white-shadow"
                onClick={() => navigateToHouse()}
              >
                Simamia Nyumba
              </button>
            </div>
          </div>

          {/* Land Management Card */}
          <div className="bg-teal-500 text-white p-6 rounded-lg shadow-lg flex-1 min-w-[250px] flex flex-col items-center hover:shadow-lg hover:scale-105 duration-300">
            <h2 className="text-xl font-bold mb-2">Ardhi</h2>
            <p className="text-center">
              Simamia viwanja vyako. Tafuta wateja wanaohitaji ardhi kwa bei
              nzuri.
            </p>
            <div className="mt-4 flex space-x-3">
              <button
                className="bg-primary text-white px-4 py-2 rounded hover:white-shadow"
                onClick={navigateToLand}
              >
                Simamia Ardhi
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
