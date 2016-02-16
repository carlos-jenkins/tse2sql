var _ = require('underscore');
var db = require('../../db');
var dbMinTokenSize = 3;

var voter = {};

var voterByIdQuery =
    'SELECT id_voter, name, family_name_1, family_name_2, sex, ' +
    'id_expiration, name_province, name_canton, name_district, site ' +
    'FROM voter' +
    'JOIN district ON voter.district_id_district = district.id_district ' +
    'JOIN canton ON district.canton_id_canton = canton.id_canton ' +
    'JOIN province ON canton.province_id_province = province.id_province ' +
    'WHERE voter.id_voter = ?;';

var voterByNameQuery =
    'SELECT * FROM voter ' +
    'WHERE MATCH(name, family_name_1, family_name_2) ' +
    'AGAINST (? IN BOOLEAN MODE) LIMIT 30;';

voter.getVoterById = function(params, type, callback) {
    db.query(voterByIdQuery, params, function(err, rows, fields) {
        callback(null, _.first(rows));
    });
};

voter.getVoterByName = function(voterName, type, callback) {
    voterName = _.map(voterName.split(' '), function(token) {
        /*
            To implement the full search, MySQL uses Boolean logic, in which:

            + stands for AND
            - stands for NOT
            [no operator] implies OR

            The minimum default token size in InnoDB is 3 characters and the
            indexing engine ignores words shorter than this minimum size, then
            in our case when the length of the token is minor than 3 the
            tokenOperator is not added, otherwise we add the + operator
        */
        var tokenOperator = (token.length < dbMinTokenSize) ? '' : '+';
        return tokenOperator + token;
    }).join(' ');

    db.query(voterByNameQuery, ['\'' + voterName + '\''],
        function(err, rows, fields) {
            callback(null, rows);
        }
    );
};

module.exports = voter;
