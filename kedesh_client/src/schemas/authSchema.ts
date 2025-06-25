import { z } from "zod";

// Login Schema
export const loginSchema = z.object({
  phone_number: z
    .string()
    .regex(
      /^0\d{9}$/,
      "Namba ya simu sio sahihi. Lazima ianze na 0 ikifatiwa na number 9."
    )
    .nonempty("Namba ya simu inatakiwa"),
  password: z
    .string()
    .min(6, "Nywira lazima iwe na urefu kuanzia herufi 6")
    .nonempty("Nywila inatakiwa"),
});

export type LoginFormData = z.infer<typeof loginSchema>;
