
var express = require('express');
var http = require('http');

/* Init App */
var app = express();


app.set('port', process.env.PORT || 3000);

app.use(app.router);

process.on('uncaughtException', function(err) {
    console.error('!!!uncaughtException = ' + err.stack);
});

/* Load database connection */
require('./db');

/* Load routes */
require('./routes')(app);

/* Start the app */
http.createServer(app).listen(app.get('port'), function() {
    console.log('Express server listening on port ' + app.get('port'));
});
