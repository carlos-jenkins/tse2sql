var voterService = require('../lib/voter-info-service');

module.exports = function(app) {
    app.get('/voter-info/:voterId', function(req, res) {
        voterService.getInfo(req.params.voterId, function(err, result) {
            if(!err) {
                res.send(result);
            }
        });
    });
};
