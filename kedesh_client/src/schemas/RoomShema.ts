import { z } from "zod";
import {
  CONDITION,
  FURNISHING_STATUS,
  HEATING_COOLING_SYSTEM,
  RENTAL_DURATION,
  ROOM_CATEGORY,
  SECURITY_FEATURES,
} from "../types/enums";

export const RoomSchema = z.object({
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

  rental_duration: z.enum(
    [
      RENTAL_DURATION.ONE_DAY,
      RENTAL_DURATION.TWO_DAY,
      RENTAL_DURATION.THREE_DAY,
      RENTAL_DURATION.ONE_WEEK,
      RENTAL_DURATION.TWO_WEEK,
      RENTAL_DURATION.THREE_WEEK,
      RENTAL_DURATION.ONE_MONTH,
      RENTAL_DURATION.THREE_MONTHS,
      RENTAL_DURATION.SIX_MONTHS,
      RENTAL_DURATION.ONE_YEAR,
    ],
    { message: "Tafadhali chagua muda wa kukodisha" }
  ),

  condition: z.enum(
    [
      CONDITION.USED,
      CONDITION.NEW,
      CONDITION.RENOVATED,
      CONDITION.UNDER_CONSTRUCTION,
    ],
    { message: "Tafadhali chagua hali ya chumba" }
  ),

  nearby_facilities: z
    .string()
    .min(1, { message: "Vifaa vya karibu vinahitajika" }),

  utilities: z.string().min(1, { message: "Huduma za umma zinahitajika" }),

  security_features: z.enum(
    [
      SECURITY_FEATURES.CCTV,
      SECURITY_FEATURES.GATED_COMMUNITY,
      SECURITY_FEATURES.ALARM_SYSTEM,
      SECURITY_FEATURES.SECURITY_GUARD,
      SECURITY_FEATURES.INTERCOM,
      SECURITY_FEATURES.FENCED,
      SECURITY_FEATURES.ELECTRONIC_GATE,
      SECURITY_FEATURES.OTHERS,
    ],
    { message: "Tafadhali chagua kipengele kimoja cha usalama" }
  ),

  heating_cooling_system: z.enum(
    [
      HEATING_COOLING_SYSTEM.CENTRAL_HEATING,
      HEATING_COOLING_SYSTEM.AIR_CONDITIONING,
      HEATING_COOLING_SYSTEM.UNDERFLOOR_HEATING,
      HEATING_COOLING_SYSTEM.HEAT_PUMP,
      HEATING_COOLING_SYSTEM.RADIATORS,
      HEATING_COOLING_SYSTEM.FAN_COOLING,
      HEATING_COOLING_SYSTEM.NONE,
    ],
    { message: "Tafadhali chagua mfumo wa joto au baridi" }
  ),

  furnishing_status: z.enum(
    [
      FURNISHING_STATUS.FULLY_FURNISHED,
      FURNISHING_STATUS.PARTIALLY_FURNISHED,
      FURNISHING_STATUS.UNFURNISHED,
    ],
    { message: "Tafadhali chagua hali ya fanicha" }
  ),

  room_category: z.enum(
    [
      ROOM_CATEGORY.SELF_CONTAINED,
      ROOM_CATEGORY.SHARED,
      ROOM_CATEGORY.SINGLE_ROOM,
      ROOM_CATEGORY.DOUBLE_ROOM,
      ROOM_CATEGORY.MASTER_ROOM,
      ROOM_CATEGORY.ENSUITE,
      ROOM_CATEGORY.COMMON_ROOM,
      ROOM_CATEGORY.STUDIO,
      ROOM_CATEGORY.BUNK_ROOM,
    ],
    { message: "Tafadhali chagua aina ya chumba" }
  ),

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

export type RoomSchemaType = z.infer<typeof RoomSchema>;
