import { z } from "zod";

export const UploadImagesSchema = z.object({
  property_id: z.string().uuid().min(1, { message: "No house selected" }),
  images: z
    .instanceof(FileList)
    .refine((files) => files.length >= 1 && files.length <= 5, {
      message: "You must select between 1 and 5 images",
    })
    .refine(
      (files) =>
        Array.from(files).every((file) => file.size < 1.2 * 1024 * 1024),
      {
        message: "Each file size should be less than 1.2MB",
      }
    ),
});

export type UploadImagesSchemaType = z.infer<typeof UploadImagesSchema>;
