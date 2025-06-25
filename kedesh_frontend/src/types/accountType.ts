export type PlanType = {
  subscription_plan_id: string;
  name: string;
  price: string;
  max_houses: number;
  duration_days: number;
};

export type AccountType = {
  account_id: string;
  plan: PlanType;
  start_date: string;
  end_date: string;
  is_active: boolean;
  agent: string;
};
