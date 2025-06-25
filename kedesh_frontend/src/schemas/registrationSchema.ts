import { z } from "zod";
import { GENDER } from "../types/enums";

export const registrationSchema = z
  .object({
    first_name: z.string().min(1, "Jina la kwanza nilazima").max(30),
    middle_name: z.string().max(30).optional(),
    last_name: z.string().min(1, "Jinal al wmisho nilazima").max(30),
    phone_number: z
      .string()
      .min(1, "Namba ya simu nilazima")
      .regex(
        /^0\d{9}$/,
        "Namba ya simu sio sahihi. Lazima ianze na 0 ikifatiwa na number 9."
      ),
    gender: z.enum([GENDER.MALE, GENDER.FEMALE], {
      message: "Chagua jisnia yako",
    }),
    email: z.string().email("Barua pepe sio sahihi").max(100),
    password: z
      .string()
      .min(6, "Nywira lazima iwe na urefu kuanzia herufi 6")
      .max(255),
    confirm_password: z.string().min(6, "Tafadhali rudia nywila yako").max(255),
    avatar: z
      .instanceof(FileList)
      .refine((files) => files?.length === 1, {
        message: "Tafadhali passport yako inatakiwa",
      })
      .refine((files) => files && files[0]?.size < 1.2 * 1024 * 1024, {
        message: "Faili la passport lazima liwe na ukubwa chini ya 1.2MB",
      }),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Nywila zako hazifanani",
    path: ["confirm_password"],
  });

export type RegistrationFormData = z.infer<typeof registrationSchema>;
