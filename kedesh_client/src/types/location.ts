export interface Region {
  region_id: string;
  name: string;
}

export interface District {
  district_id: string;
  name: string;
  region: string;
}

export interface Ward {
  ward_id: string;
  name: string;
  district: string;
}

export interface Street {
  street_id: string;
  name: string;
  ward: string;
}
