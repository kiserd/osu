const defaultTheme = require('tailwindcss/defaultTheme')

/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /* 
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',
        
        /* 
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            screens: {
                'xs': '420px',
                ...defaultTheme.screens,
            },
            colors: {
                'custom-cool-extraDark': '#001219',
                'custom-cool-dark': '#005f73',
                'custom-cool-med': '#0a9396',
                'custom-cool-light': '#94d2bd',
                'custom-cool-extraLight': '#e9d8a6',
                'custom-warm-extraLight': '#ee9b00',
                'custom-warm-light': '#ca6702',
                'custom-warm-med': '#bb3e03',
                'custom-warm-dark': '#ae2012',
                'custom-warm-extraDark': '#9b2226',
                'custom-background': '#18191A',
                'custom-card': '#242526',
                'custom-hover': '#3A3B3C',
                'custom-text-primary': '#E4E6EB',
                'custom-text-secondary': '#B0B3B8'
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
