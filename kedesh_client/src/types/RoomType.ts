import { Location } from "./locationType";

export interface Room {
  property_id: string;
  location: Location;
  images: string[];
  room_category: string;
  price: string;
  rental_duration: string;
  status: string;
  description: string;
  condition: string;
  nearby_facilities: string;
  utilities: string;
  security_features: string;
  heating_cooling_system: string;
  furnishing_status: string;
  is_deleted: boolean;
  listing_date: string;
  updated_at: string;
}

export interface RoomResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Room[];
}

export type RoomDetail = Room;
