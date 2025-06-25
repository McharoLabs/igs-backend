import { z } from "zod";

export const SubscribeSchema = z.object({
  phone_number: z
    .string()
    .min(1, "Phone number is required")
    .regex(
      /^0\d{9}$/,
      "Invalid Tanzanian phone number. Must start with 0 followed by 9 digits."
    ),
  plan_id: z.string().min(1, { message: "Please select a plan" }),
});

export type SubscribeSchemaType = z.infer<typeof SubscribeSchema>;
