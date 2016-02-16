var _ = require('underscore');
var db = require('../../db');

var voter = {};

var baseQuery = 'SELECT id_voter, name, family_name_1, family_name_2, sex, id_expiration, ' +
                'name_province, name_canton, name_district, site FROM voter ' +
                'JOIN district ON voter.district_id_district = district.id_district ' +
                'JOIN canton ON district.canton_id_canton = canton.id_canton ' +
                'JOIN province ON canton.province_id_province = province.id_province ';

var voterByIdQuery = baseQuery + 'WHERE voter.id_voter = ?;';

var voterByNameQuery = baseQuery + 'WHERE voter.name LIKE ? ' +
                'AND voter.family_name_1 LIKE ? ' +
                'AND voter.family_name_2 LIKE ? ;'

voter.getVoterById = function(params, type, callback) {
    db.query(voterByIdQuery, params, function(err, rows, fields) {
        callback(null, _.first(rows));
    });
};

voter.getVoterByName = function(voterName, type, callback) {
    var params = _.map(voterName.split(' '), function(token) {
        return '%' + token + '%';
    });

    db.query(voterByNameQuery, params, function(err, rows, fields) {
        callback(null, rows);
    });
};

module.exports = voter;
