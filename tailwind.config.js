/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.jinja',
    './apps/**/*.py',
    './**/*.py',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1A3A5C',
          light: '#2C5F8A',
        },
        accent: {
          DEFAULT: '#FF6B35',
          dark: '#E55A24',
        },
      },
      fontFamily: {
        inter: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
