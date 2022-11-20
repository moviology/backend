/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "api/templates/**/*.html",
    "api/static/src/**/*.js",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
        require("flowbite/plugin")
    ]
}