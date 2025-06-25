// import { SquareTerminal, Bot, BookOpen, Settings2 } from "lucide-react";
// import { AsideBarProps } from "../types/asideBarTypes";
// import useNavigation from "../hooks/useNavigation";

// const useNavMain = () => {
//   const { goToDashboard, goToLogin, goToPage, signOut } = useNavigation();
// };

// export default useNavMain;
// export const navMain: AsideBarProps[] = [
//   {
//     title: "Playground",
//     icon: SquareTerminal,
//     onClick: () => goToDashboard(), // Go to the home page
//     items: [
//       {
//         title: "History",
//         onClick: () => goToPage("/history"), // Navigate to the "History" page
//       },
//       {
//         title: "Starred",
//         onClick: () => goToPage("/starred"), // Navigate to the "Starred" page
//       },
//       {
//         title: "Settings",
//         onClick: () => goToPage("/settings"), // Navigate to the "Settings" page
//       },
//     ],
//   },
//   {
//     title: "Models",
//     icon: Bot,
//     onClick: () => goToLogin(), // Go to the login page
//     items: [
//       {
//         title: "Genesis",
//         onClick: () => goToPage("/models/genesis"),
//       },
//       {
//         title: "Explorer",
//         onClick: () => goToPage("/models/explorer"),
//       },
//       {
//         title: "Quantum",
//         onClick: () => goToPage("/models/quantum"),
//       },
//     ],
//   },
//   {
//     title: "Documentation",
//     icon: BookOpen,
//     onClick: () => goToPage("/docs"), // Navigate to docs
//     items: [
//       {
//         title: "Introduction",
//         onClick: () => goToPage("/docs/introduction"),
//       },
//       {
//         title: "Get Started",
//         onClick: () => goToPage("/docs/get-started"),
//       },
//       {
//         title: "Tutorials",
//         onClick: () => goToPage("/docs/tutorials"),
//       },
//       {
//         title: "Changelog",
//         onClick: () => goToPage("/docs/changelog"),
//       },
//     ],
//   },
//   {
//     title: "Settings",
//     icon: Settings2,
//     onClick: () => goToPage("/settings"), // Navigate to settings
//     items: [
//       {
//         title: "General",
//         onClick: () => goToPage("/settings/general"),
//       },
//       {
//         title: "Team",
//         onClick: () => goToPage("/settings/team"),
//       },
//       {
//         title: "Billing",
//         onClick: () => goToPage("/settings/billing"),
//       },
//       {
//         title: "Limits",
//         onClick: () => goToPage("/settings/limits"),
//       },
//     ],
//   },
//   {
//     title: "Sign Out",
//     icon: Settings2, // Use an appropriate icon for sign out
//     onClick: signOut, // Use the signOut function for logout
//   },
// ];
