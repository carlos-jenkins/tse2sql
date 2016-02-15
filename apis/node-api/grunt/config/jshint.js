module.exports = {
  options: {
    asi: false,
    boss: true,
    browser: false,
    curly: true,
    eqnull: true,
    evil: true,
    expr: true,
    latedef: true,
    maxerr: 100,
    newcap: true,
    noarg: true,
    node: true,
    noempty: true,
    shadow: true
  },
  src: [
    '**/*.js',
    'db/*.js',
    'routes/*.js',
    'settings/*.js',
    '!node_modules/**/*.js'
  ]
};
