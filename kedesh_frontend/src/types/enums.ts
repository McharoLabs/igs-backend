export enum PROPERTY_AVAILABILITY_STATUS {
  AVAILABLE = "Available",
  BOOKED = "Booked",
  SOLD = "Sold",
}

export enum PROPERTY_TYPE {
  ROOM = "Room",
  HOUSE = "House",
}

export enum GENDER {
  MALE = "Male",
  FEMALE = "Female",
}

export enum CATEGORY {
  RENTAL = "Rental",
  SALE = "Sale",
}

export enum CONDITION {
  USED = "Used",
  NEW = "New",
  RENOVATED = "Renovated",
  UNDER_CONSTRUCTION = "Under Construction",
}

export enum SECURITY_FEATURES {
  CCTV = "CCTV",
  GATED_COMMUNITY = "Gated Community",
  ALARM_SYSTEM = "Alarm System",
  SECURITY_GUARD = "Security Guard",
  INTERCOM = "Intercom",
  FENCED = "Fenced",
  ELECTRONIC_GATE = "Electronic Gate",
  OTHERS = "Others",
}

export enum HEATING_COOLING_SYSTEM {
  CENTRAL_HEATING = "Central Heating",
  AIR_CONDITIONING = "Air Conditioning",
  UNDERFLOOR_HEATING = "Underfloor Heating",
  HEAT_PUMP = "Heat Pump",
  RADIATORS = "Radiators",
  FAN_COOLING = "Fan Cooling",
  NONE = "None",
}

export enum FURNISHING_STATUS {
  FULLY_FURNISHED = "Fully Furnished",
  PARTIALLY_FURNISHED = "Partially Furnished",
  UNFURNISHED = "Unfurnished",
}

export enum ROOM_CATEGORY {
  SELF_CONTAINED = "Self-contained",
  SHARED = "Shared",
  SINGLE_ROOM = "Single Room",
  DOUBLE_ROOM = "Double Room",
  MASTER_ROOM = "Master Room",
  ENSUITE = "En-suite",
  COMMON_ROOM = "Common Room",
  STUDIO = "Studio",
  BUNK_ROOM = "Bunk Room",
}

// RENTAL_DURATION Enum
export enum RENTAL_DURATION {
  ONE_DAY = "1 Day",
  TWO_DAY = "2 Days",
  THREE_DAY = "3 Days",
  ONE_WEEK = "1 Week",
  TWO_WEEK = "2 Weeks",
  THREE_WEEK = "3 Weeks",
  ONE_MONTH = "1 Month",
  THREE_MONTHS = "3 Months",
  SIX_MONTHS = "6 Months",
  ONE_YEAR = "1 Year",
}

// RENTAL_DURATION Choices
export const RENTAL_DURATION_CHOICES = Object.values(RENTAL_DURATION).map(
  (duration) => ({
    value: duration,
    label: duration,
  })
);

// CATEGORY
export const CATEGORY_CHOICES = Object.values(CATEGORY).map((category) => ({
  value: category,
  label: category,
}));

export const ROOM_CATEGORY_CHOICES = Object.values(ROOM_CATEGORY).map((c) => ({
  value: c,
  label: c,
}));

export const isCategoryValid = (category: string): boolean => {
  return Object.values(CATEGORY).includes(category as CATEGORY);
};

export const CATEGORY_DEFAULT = CATEGORY.RENTAL;

export const isHouseTypeValid = (houseType: string): boolean => {
  return Object.values(CATEGORY).includes(houseType as CATEGORY);
};

// CONDITION
export const CONDITION_CHOICES = Object.values(CONDITION).map((condition) => ({
  value: condition,
  label: condition,
}));

export const CONDITION_DEFAULT = CONDITION.USED;

export const isConditionValid = (condition: string): boolean => {
  return Object.values(CONDITION).includes(condition as CONDITION);
};

// SECURITY_FEATURES
export const SECURITY_FEATURES_CHOICES = Object.values(SECURITY_FEATURES).map(
  (securityFeature) => ({
    value: securityFeature,
    label: securityFeature,
  })
);

export const SECURITY_FEATURES_DEFAULT = SECURITY_FEATURES.OTHERS;

export const isSecurityFeaturesValid = (securityFeature: string): boolean => {
  return Object.values(SECURITY_FEATURES).includes(
    securityFeature as SECURITY_FEATURES
  );
};

// HEATING_COOLING_SYSTEM
export const HEATING_COOLING_SYSTEM_CHOICES = Object.values(
  HEATING_COOLING_SYSTEM
).map((system) => ({
  value: system,
  label: system,
}));

export const HEATING_COOLING_SYSTEM_DEFAULT = HEATING_COOLING_SYSTEM.NONE;

export const isHeatingCoolingSystemValid = (system: string): boolean => {
  return Object.values(HEATING_COOLING_SYSTEM).includes(
    system as HEATING_COOLING_SYSTEM
  );
};

// FURNISHING_STATUS
export const FURNISHING_STATUS_CHOICES = Object.values(FURNISHING_STATUS).map(
  (status) => ({
    value: status,
    label: status,
  })
);

export const FURNISHING_STATUS_DEFAULT = FURNISHING_STATUS.UNFURNISHED;

export const isFurnishingStatusValid = (status: string): boolean => {
  return Object.values(FURNISHING_STATUS).includes(status as FURNISHING_STATUS);
};

// LAND_TYPE
export enum LAND_TYPE {
  RESIDENTIAL = "Makazi",
  COMMERCIAL = "Biashara",
  AGRICULTURAL = "Kilimo",
  VACANT = "Tupu",
}

export const LAND_TYPE_CHOICES = Object.entries(LAND_TYPE).map(
  ([key, value]) => ({
    value: key,
    label: value,
  })
);

export const LAND_TYPE_DEFAULT = "RESIDENTIAL";

// ACCESS_ROAD_TYPE
export enum ACCESS_ROAD_TYPE {
  PAVED = "Barabara ya lami",
  GRAVEL = "Barabara ya kokoto",
  DIRT = "Barabara ya udongo",
  NONE = "Hakuna barabara",
}

export const ACCESS_ROAD_TYPE_CHOICES = Object.entries(ACCESS_ROAD_TYPE).map(
  ([key, value]) => ({
    value: key,
    label: value,
  })
);

export const ACCESS_ROAD_TYPE_DEFAULT = "PAVED";

// ZONING_TYPE
export enum ZONING_TYPE {
  RESIDENTIAL = "Eneo la makazi",
  COMMERCIAL = "Eneo la biashara",
  INDUSTRIAL = "Eneo la viwanda",
  MIXED_USE = "Matumizi mchanganyiko",
}

export const ZONING_TYPE_CHOICES = Object.entries(ZONING_TYPE).map(
  ([key, value]) => ({
    value: key,
    label: value,
  })
);

export const ZONING_TYPE_DEFAULT = "RESIDENTIAL";

// LAND_STATUS
export enum LAND_STATUS {
  AVAILABLE = "Available",
  SOLD = "Sold",
  RENTED = "Rented",
}

export const LAND_STATUS_CHOICES = Object.entries(LAND_STATUS).map(
  ([key, value]) => ({
    value: key,
    label: value,
  })
);

export const LAND_STATUS_DEFAULT = "AVAILABLE";

// LAND_SIZE_UNIT
export enum LAND_SIZE_UNIT {
  SQUARE_METERS = "Mita za Mraba (m²)",
  HECTARES = "Hekta (ha)",
  SQUARE_FEET = "Futi za Mraba (sq ft)",
  ACRES = "Ekari (ac)",
}

export const LAND_SIZE_UNIT_CHOICES = Object.entries(LAND_SIZE_UNIT).map(
  ([key, value]) => ({
    value: key,
    label: value,
  })
);

export const LAND_SIZE_UNIT_DEFAULT = "SQUARE_METERS";
