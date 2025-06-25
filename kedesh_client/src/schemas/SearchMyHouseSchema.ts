import { z } from "zod";

export const SearchMyHouseSchema = z.object({
  title: z.string().min(1, { message: "Title can not be empty" }),
});
