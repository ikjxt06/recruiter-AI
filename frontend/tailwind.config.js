/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17202A",
        steel: "#52616B",
        mint: "#2FBF9F",
        coral: "#E96C4C"
      }
    }
  },
  plugins: []
};
