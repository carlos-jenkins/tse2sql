module.exports = function(grunt) {
  // Project configuration.
  var configs = require('load-grunt-configs')(grunt, {
    config: {
      src: ['grunt/config/*.js']
    }
  });
  grunt.initConfig(configs);

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-githooks');

  grunt.registerTask('default', ['']);
  grunt.registerTask('sanity', ['jshint', 'githooks']);
};
