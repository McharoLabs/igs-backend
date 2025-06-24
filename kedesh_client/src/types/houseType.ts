import { Location } from "./locationType";

export interface House {
  property_id: string;
  location: Location;
  images: string[];
  category: string;
  price: string;
  rental_duration: string;
  description: string;
  condition: string;
  nearby_facilities: string;
  utilities: string;
  security_features: string;
  heating_cooling_system: string;
  furnishing_status: string;
  total_bed_room: number;
  total_dining_room: number;
  total_bath_room: number;
  status: string;
  is_deleted: string;
  listing_date: string;
  updated_at: string;
}

export interface HouseResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: House[];
}

export type HouseDetail = House;
