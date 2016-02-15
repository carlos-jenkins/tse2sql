module.exports = {
  unit: {
    options: {
      clearRequireCache: true,
      reporter: 'spec',
      require: ['test/unit/settings.js']
    },
    src: 'test/unit/**/*.js'
  }
};
