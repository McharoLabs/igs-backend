import { useSelector } from "react-redux";
import { RootState } from "../../state/store";
import React from "react";
import apiClient from "../../api/apiClient";
import { endpoints } from "../../api/endpoints";

const Nav = ({ onSidebarToggle }: { onSidebarToggle: () => void }) => {
  const { user, tokens } = useSelector((state: RootState) => state.auth);
  const [avatarUrl, setAvatarUrl] = React.useState<string | null>(null);

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

    fetchAvatar();
  }, [tokens.access]);

  return (
    <div>
      <nav className="fixed top-0 z-50 w-full bg-white text-secondary">
        <div className="px-3 py-3 lg:px-5 lg:pl-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center justify-start rtl:justify-end">
              <button
                type="button"
                className="inline-flex items-center p-2 text-sm rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200"
                onClick={onSidebarToggle}
              >
                <span className="sr-only">Open sidebar</span>
                <svg
                  className="w-6 h-6"
                  aria-hidden="true"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    clipRule="evenodd"
                    fillRule="evenodd"
                    d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
                  ></path>
                </svg>
              </button>
              <a
                href={`https://www.rental.seranise.co.tz/`}
                className="flex ms-2 md:me-24"
              >
                <img src="/logo.png" className="h-8 me-3" alt="Logo" />
                <span className="self-center text-xl font-semibold sm:text-2xl whitespace-nowrap">
                  Kedesh
                </span>
              </a>
            </div>
            <div className="flex items-center">
              <div className="flex items-center ms-3 flex-row">
                <div className="text-sm bg-gray-800 rounded-full">
                  <span className="sr-only">Open user menu</span>
                  <img
                    className="w-8 h-8 rounded-full"
                    src={`${avatarUrl}`}
                    alt="user photo"
                  />
                </div>
                <div className="hidden sm:flex">
                  <div className="px-2">
                    <p className="text-sm text-gray-900">{user.full_name}</p>
                    <p className="text-sm text-gray-500 truncate">
                      {user.email}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Nav;
