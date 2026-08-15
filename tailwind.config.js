/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './layout/**/*.liquid',
    './templates/**/*.liquid',
    './templates/**/*.json',
    './sections/**/*.liquid',
    './snippets/**/*.liquid',
    './assets/**/*.js'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Haffer', 'sans-serif'],
      }
    },
  },
  plugins: [
    require('@tailwindcss/aspect-ratio'),
  ],
}
