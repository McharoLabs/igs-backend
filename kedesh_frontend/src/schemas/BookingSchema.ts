import { z } from "zod";

export const BookingSchema = z.object({
  property_id: z
    .string({
      message: "Fungua upya ukurasa",
    })
    .uuid(),
  customer_name: z.string().min(1, { message: "Tafadhali andika jina lako" }),
  customer_email: z
    .string()
    .email({ message: "Tafadhali andika barua pepe yako" }),
  customer_phone: z
    .string()
    .min(1, "Number ya simu inahitajika")
    .regex(
      /^0\d{9}$/,
      "Namba ya simu sio sahihi. Lazima ianze na 0 ikifatiwa na number 9."
    ),
});

export type BookingType = z.infer<typeof BookingSchema>;
