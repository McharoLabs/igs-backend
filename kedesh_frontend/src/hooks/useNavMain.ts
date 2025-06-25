import {
  Settings2,
  Home,
  LayoutDashboard,
  PersonStanding,
  CreditCard,
} from "lucide-react";
import { AsideBarProps, QUICK_LINKS_TYPE } from "../types/asideBarTypes";
import useNavigation from "./useNavigation";

const useNavMain = () => {
  const navigation = useNavigation();

  const quickLinks: QUICK_LINKS_TYPE[] = [
    {
      title: "Dashibodi",
      icon: LayoutDashboard,
      onClick: navigation.goToDashboard,
    },
    {
      title: "Ongeza Nyumba Mpya",
      icon: Home,
      onClick: navigation.goToAddHouse,
    },
    {
      title: "Tazama Nyumba Zote",
      icon: Home,
      onClick: navigation.goToHouseList,
    },
    { title: "Ongeza Chumba", icon: Home, onClick: navigation.goToAddRoom },
    {
      title: "Tazama Vyumba Vyote",
      icon: Home,
      onClick: navigation.goToRoomList,
    },
    {
      title: "Profaili",
      icon: PersonStanding,
      onClick: navigation.goToProfile,
    },
  ];

  const navMain: AsideBarProps[] = [
    {
      title: "Dashibodi",
      icon: LayoutDashboard,
      onClick: navigation.goToDashboard,
    },
    {
      title: "Nyumba",
      icon: Home,
      items: [
        {
          title: "Ongeza Nyumba Mpya",
          onClick: navigation.goToAddHouse,
        },
        {
          title: "Tazama Nyumba Zote",
          onClick: navigation.goToHouseList,
        },
      ],
    },
    {
      title: "Chumba",
      icon: Home,
      items: [
        {
          title: "Ongeza Chumba",
          onClick: navigation.goToAddRoom,
        },
        {
          title: "Tazama Vyumba Vyote",
          onClick: navigation.goToRoomList,
        },
      ],
    },
    {
      title: "Akaunti Plani",
      icon: CreditCard,
      onClick: navigation.goToSubscriptionPlan,
    },
    {
      title: "Mipangilio",
      icon: Settings2,
      items: [
        {
          title: "Profaili",
          onClick: navigation.goToProfile,
        },
      ],
    },
    {
      title: "Ondoka",
      icon: Settings2,
      onClick: navigation.logout,
    },
  ];

  return { navMain, quickLinks };
};

export default useNavMain;
