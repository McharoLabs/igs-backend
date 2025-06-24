import { Location } from "./locationType";

export interface Property {
  property_id: string;
  location: Location;
  images: string[];
  category: string;
  price: string;
  rental_duration: string;
  title: string;
  description: string;
  condition: string;
  nearby_facilities: string;
  utilities: string;
  security_features: string;
  heating_cooling_system: string;
  furnishing_status: string;
  status: string;
  listing_date: string;
  property_type: string;
  updated_at: string;
}

export interface PropertyResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Property[];
}

export type PropertyDetail = Property;
