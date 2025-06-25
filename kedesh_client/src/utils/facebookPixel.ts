import ReactPixel from "react-facebook-pixel";

const pixelId = "1939868953491112";

const options = {
  autoConfig: true, // Automatically configure Pixel
  debug: false, // Set to true to enable debugging in the console
};

const initFacebookPixel = () => {
  ReactPixel.init(
    pixelId,
    {
      fn: "",
      em: "",
      ph: "",
      ct: "",
      country: "",
      db: "",
      ge: "",
      ln: "",
      st: "",
      zp: "",
    },
    options
  );
  ReactPixel.pageView(); // Track the initial page load
};

export default initFacebookPixel;
