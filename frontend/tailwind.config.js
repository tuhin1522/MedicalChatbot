/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'primary': 'rgb(var(--color-primary) / <alpha-value>)',
                'success': 'rgb(var(--color-success) / <alpha-value>)',
                'base-100': 'rgb(var(--color-base-100) / <alpha-value>)',
                'base-200': 'rgb(var(--color-base-200) / <alpha-value>)',
                'base-300': 'rgb(var(--color-base-300) / <alpha-value>)',
                'base-content': 'rgb(var(--color-base-content) / <alpha-value>)',
            },
            borderColor: {
                'base-300': 'rgb(var(--color-border) / <alpha-value>)',
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
            },
        },
    },
    plugins: [],
}