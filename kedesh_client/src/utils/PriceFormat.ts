export const formatPrice = (
  price?: string | number,
  currency: string = "TZS"
) => {
  if (!price) return "Not available";

  const numericPrice = typeof price === "string" ? parseFloat(price) : price;
  if (isNaN(numericPrice)) return "Not available";

  return `${numericPrice.toLocaleString()} ${currency}`;
};
