import { ChevronRight } from "lucide-react";
import React from "react";
import useNavMain from "../../hooks/useNavMain";

const AsideBar: React.FC<{ isOpen: boolean; toggleSidebar: () => void }> = ({
  isOpen,
  toggleSidebar,
}) => {
  const { navMain } = useNavMain();

  const [activeItemIndex, setActiveItemIndex] = React.useState<number | null>(
    null
  );
  const [openItemIndex, setOpenItemIndex] = React.useState<number | null>(null);

  const handleToggle = (index: number) => {
    if (openItemIndex === index) {
      setOpenItemIndex(null);
    } else {
      setOpenItemIndex(index);
    }
  };

  const handleItemClick = (
    index: number,
    onClick: (() => void) | undefined
  ) => {
    setActiveItemIndex(index);
    onClick?.();
    toggleSidebar();
  };

  return (
    <aside
      id="logo-sidebar"
      className={`fixed top-0 left-0 z-40 w-64 h-screen pt-20 transition-transform bg-white border-r border-gray-200 sm:translate-x-0 ${
        isOpen ? "translate-x-0" : "-translate-x-full"
      }`}
      aria-label="Sidebar"
    >
      <div className="h-full px-3 pb-4 overflow-y-auto bg-white">
        <ul className="space-y-2 font-medium">
          {navMain.map((item, index) => (
            <li key={index}>
              <a
                onClick={() => {
                  if (item.items) {
                    handleToggle(index);
                    setActiveItemIndex(index);
                  } else {
                    handleItemClick(index, item.onClick);
                  }
                }}
                className={`flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group cursor-pointer
                 ${activeItemIndex === index ? "bg-gray-200" : ""}`}
              >
                <item.icon />
                <span className="ms-3">{item.title}</span>
                {item.items && (
                  <ChevronRight
                    className={`ml-auto transition-transform duration-200 ${
                      openItemIndex === index ? "rotate-90" : ""
                    }`}
                  />
                )}
              </a>

              {openItemIndex === index && item.items && (
                <ul className="ml-4">
                  {item.items.map((subItem, subIndex) => (
                    <li key={subIndex}>
                      <a
                        onClick={() => {
                          toggleSidebar();
                          subItem.onClick?.();
                        }}
                        className="block px-4 py-2 text-gray-600 hover:text-lg rounded-lg cursor-pointer"
                      >
                        {subItem.title}
                      </a>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
};

export default AsideBar;
