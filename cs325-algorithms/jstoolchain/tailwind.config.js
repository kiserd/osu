module.exports = {
  content: [
    '../**/templates/*.html',
    '../**/templates/**/*.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  purge: {
    enabled: true,
    content: ['../your-django-folder/path-to-your-templates/**/*.html'],
  },
}
