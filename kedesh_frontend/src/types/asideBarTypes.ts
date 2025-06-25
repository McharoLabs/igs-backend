import { type LucideIcon } from "lucide-react";

export interface AsideBarProps {
  title: string;
  icon: LucideIcon;
  onClick?: () => void;
  items?: {
    title: string;
    onClick: () => void;
  }[];
}

export interface QUICK_LINKS_TYPE {
  title: string;
  icon: LucideIcon;
  onClick: () => void;
}
