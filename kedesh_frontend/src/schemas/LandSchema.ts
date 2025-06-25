import { z } from "zod";

export const LandFormSchema = z.object({
  description: z
    .string()
    .min(50, { message: "Maelezo yanapaswa kuwa na angalau herufi 50" })
    .refine(
      (data) =>
        !/\+255?\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{3}|\d{9}|0\d{3}[\s-]?\d{6}/.test(
          data
        ),
      {
        message: "Maelezo haya hayaruhusiwi kuwa na namba za simu",
      }
    ),

  price: z.coerce.number().refine((value) => !isNaN(value) && value > 0, {
    message: "Bei inapaswa kuwa kubwa kuliko 0",
  }),

  category: z.enum(["RESIDENTIAL", "COMMERCIAL", "AGRICULTURAL", "VACANT"]),
  land_size_unit: z.enum(["SQUARE_METERS", "SQUARE_FEET", "HECTARES", "ACRES"]),
  land_size: z.coerce.number().refine((value) => !isNaN(value) && value > 0, {
    message: "Ukubwa wa ardhi unatakiwa",
  }),
  access_road_type: z.enum(["PAVED", "GRAVEL", "DIRT", "NONE"]),
  zoning_type: z.enum(["RESIDENTIAL", "COMMERCIAL", "INDUSTRIAL", "MIXED_USE"]),
  utilities: z.string().min(1, { message: "Huduma za umma zinahitajika" }),
  region: z.string().min(1, { message: "Tafadhali chagua kanda" }),
  district: z.string().min(1, { message: "Tafadhali chagua wilaya" }),
  ward: z.string().min(1, { message: "Kata inahitajika" }),
  street: z.string().min(1, { message: "Mtaa unahitajika" }),

  latitude: z.coerce.number().default(0),
  longitude: z.coerce.number().default(0),

  images: z
    .instanceof(FileList)
    .refine((files) => files.length >= 4 && files.length <= 5, {
      message: "Picha 4 au 5 pekee ndizo zinahitajika kupakia",
    })
    .refine(
      (files) =>
        Array.from(files).every((file) => file.size <= 8 * 1024 * 1024),
      {
        message: "Kila faili inapaswa kuwa ndogo kuliko 8MB",
      }
    ),
});

export const RequestAgentContactSchema = z.object({
  customer_name: z.string().min(1, { message: "Jina linahitajika" }),
  customer_email: z
    .string()
    .email({ message: "Tafadhali ingiza barua pepe halali" })
    .min(1, { message: "Barua pepe inahitajika" }),
  land_id: z.string().uuid({ message: "Tafadhali ingiza ID halali ya ardhi" }),
  customer_phone: z
    .string()
    .min(1, "Number ya simu inahitajika")
    .regex(
      /^0\d{9}$/,
      "Namba ya simu sio sahihi. Lazima ianze na 0 ikifatiwa na number 9."
    ),
});
export type RequestAgentContactSchemaType = z.infer<
  typeof RequestAgentContactSchema
>;

export type LandFormSchemaType = z.infer<typeof LandFormSchema>;
