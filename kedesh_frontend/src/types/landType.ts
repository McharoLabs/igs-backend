import { Location } from "./locationType";

export type LandItem = {
  land_id: string;
  category: string;
  land_size: string;
  price: string;
  access_road_type: string;
  zoning_type: string;
  utilities: string;
  description: string;
  is_active_account: boolean;
  status: string;
  is_deleted: boolean;
  land_size_unit: string;
  listing_date: string;
  location: Location;
  images: string[];
};

export type LandResponse = LandItem;

export type LandListResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: LandItem[];
};
