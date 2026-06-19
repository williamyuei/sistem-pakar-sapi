/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html'],
  theme: {
    extend: {
      colors: {
        brand: { 
          DEFAULT: '#eab308', 
          dark: '#ca8a04', 
          light: '#fef3c7' 
        },
        yellow: {
          50: '#fefce8',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#eab308',
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#713f12',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'yellow-sm': '0 2px 8px rgba(234, 179, 8, 0.1)',
        'yellow-md': '0 4px 12px rgba(234, 179, 8, 0.15)',
        'yellow-lg': '0 8px 24px rgba(234, 179, 8, 0.2)',
        'yellow-xl': '0 12px 32px rgba(234, 179, 8, 0.25)',
      }
    }
  },
  plugins: [require('@tailwindcss/forms')],
}
