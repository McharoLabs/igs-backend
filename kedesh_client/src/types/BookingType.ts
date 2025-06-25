import { Location } from "./locationType";

type Property = {
  property_id: string;
  category: string;
  price: string;
  status: string;
  heating_cooling_system: string;
  description: string;
  condition: string;
  nearby_facilities: string;
  utilities: string;
  security_features: string;
  furnishing_status: string;
  location: Location;
  images: string[];
};

export type Booking = {
  booking_id: string;
  property: Property;
  customer_name: string;
  customer_email: string;
  customer_phone_number: string;
  has_owner_read: boolean;
  listing_date: string;
};

export interface BookingResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Booking[];
}
