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
  safelist: [
    // dark mode variants that get stripped by purge in multi-line Jinja2 class attrs
    'dark:text-blue-300', 'dark:text-blue-400', 'dark:text-blue-600',
    'dark:bg-blue-900/20', 'dark:bg-blue-900/40',
    'dark:bg-blue-50', 'dark:bg-blue-100',
    'dark:hover:bg-gray-700',
    'dark:group-hover:text-blue-400',
    'dark:border-blue-500',
    'dark:hover:border-blue-500',
    'text-blue-700', 'text-blue-600',
    'bg-blue-100', 'bg-blue-50',
    'col-span-full',
  ],
  plugins: [],
}
