var voterService = require('../lib/voter-info-service');

module.exports = function(app) {
    app.get('/voter/info-by-id/:voterId', function(req, res) {
        voterService.getVoterById(req.params.voterId, function(err, result) {
            if(!err) {
                res.send(result);
            } else {
                res.send(result, err.code);
            }
        });
    });

    app.get('/voter/info-by-name/:voterName', function(req, res) {
        voterService.getVoterByName(req.params.voterName, function(err, result) {
            if(!err) {
                res.send(result);
            } else {
                res.send(result, err.code);
            }
        });
    });
};
