export const scrollToElement = (
  selector: string,
  behavior: ScrollBehavior = "smooth"
) => {
  const element = document.querySelector(selector);
  if (element) {
    element.scrollIntoView({ behavior });
  }
};
