import { z } from "zod";
import {
  CATEGORY,
  CONDITION,
  FURNISHING_STATUS,
  HEATING_COOLING_SYSTEM,
  RENTAL_DURATION,
  SECURITY_FEATURES,
} from "../types/enums";

export const HouseSchema = z
  .object({
    category: z.enum([CATEGORY.RENTAL, CATEGORY.SALE], {
      message: "Tafadhali chagua aina ya mali",
    }),

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
    rental_duration: z
      .enum(
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
      )
      .optional(),
    condition: z.enum(
      [
        CONDITION.USED,
        CONDITION.NEW,
        CONDITION.RENOVATED,
        CONDITION.UNDER_CONSTRUCTION,
      ],
      { message: "Tafadhali chagua hali ya nyumba" }
    ),
    nearby_facilities: z
      .string()
      .min(1, { message: "Vitu vya karibu vinahitajika" }),
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
      { message: "Tafadhali chagua angalau kipengele kimoja cha usalama" }
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
      { message: "Tafadhali chagua hali ya samani" }
    ),
    total_bed_room: z.coerce.number().refine((value) => !isNaN(value), {
      message: "Idadi ya vyumba vya kulala inapaswa kuwa nambari halali.",
    }),
    total_dining_room: z.coerce.number().refine((value) => !isNaN(value), {
      message: "Idadi ya vyumba vya kulia inapaswa kuwa nambari halali.",
    }),
    total_bath_room: z.coerce.number().refine((value) => !isNaN(value), {
      message: "Idadi ya vyumba vya bafu inapaswa kuwa nambari halali.",
    }),
    region: z.string().min(1, { message: "Tafadhali chagua mkoa" }),
    district: z.string().min(1, { message: "Tafadhali chagua wilaya" }),
    ward: z.string().min(1, { message: "Kata inahitajika" }),
    street: z.string().min(1, { message: "Mtaa unahitajika" }),
    latitude: z.coerce
      .number()
      .default(0)
      .refine((value) => !isNaN(value), {
        message: "Latitudo inapaswa kuwa nambari halali",
      }),
    longitude: z.coerce
      .number()
      .default(0)
      .refine((value) => !isNaN(value), {
        message: "Longitude inapaswa kuwa nambari halali.",
      }),
    images: z
      .instanceof(FileList)
      .refine((files) => files.length >= 4 && files.length <= 6, {
        message: "Picha 4 au 6 tu zinahitajika kupakiwa",
      })
      .refine(
        (files) =>
          Array.from(files).every((file) => file.size <= 8 * 1024 * 1024),
        {
          message: "Kila faili inapaswa kuwa chini ya 8MB",
        }
      ),
  })
  .refine(
    (data) => {
      if (data.category === CATEGORY.RENTAL && !data.rental_duration) {
        return false;
      }
      return true;
    },
    {
      message: "Mudao wa kukodisha unahitajika wakati aina ni RENTAL",
      path: ["rental_duration"],
    }
  );

export type HouseSchemaType = z.infer<typeof HouseSchema>;
