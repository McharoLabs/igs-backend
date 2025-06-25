/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        satisfy: ["Satisfy", "cursive"],
        poppins: ["Poppins", "sans-serif"],
      },
      colors: {
        primary: {
          DEFAULT: "#28a745",
          light: "#5cd68d",
          dark: "#1e7e34",
        },
        secondary: {
          DEFAULT: "#2c3e50",
          light: "#34495e",
          dark: "#1a252f",
        },
        accent: {
          yellow: "#f1c40f",
          coral: "#ff6f61",
          gray: "#7f8c8d",
        },
        body: "#f7fdf9",
        "white-20": "rgba(255, 255, 255, 0.2)",
      },
      container: {
        center: true,
        padding: {
          lg: "1rem",
          xl: "1rem",
          "2xl": "2rem",
        },
      },
      animation: {
        "spin-superslow": "spin 4s linear infinite",
        rocket: "rocket 3s linear infinite",
        shimmer: "shimmer 8s linear infinite",
        "slide-in-down": "slideInDown 0.6s ease-out both",
        "bounce-delayed": "bounce 2s infinite 1s",
        "pulse-fast": "pulse 2s infinite",
      },
      keyframes: {
        rocket: {
          "0%, 100%": { transform: "rotate(-2deg) translate(0px, 0px)" },
          "50%": { transform: "rotate(2deg) translate(50px, 50px)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        slideInDown: {
          "0%": { transform: "translateY(-50%)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};
