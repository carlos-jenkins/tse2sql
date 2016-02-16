var _ = require('underscore');
var db = require('../../db');

var voter = {};

var voterByIdQuery = 'SELECT id_voter, name, family_name_1, family_name_2, sex, id_expiration, ' +
                'name_province, name_canton, name_district, site FROM voter ' +
                'JOIN district ON voter.district_id_district = district.id_district ' +
                'JOIN canton ON district.canton_id_canton = canton.id_canton '+
                'JOIN province ON canton.province_id_province = province.id_province ' +
                'WHERE voter.id_voter = ?;';

voter.getInfo = function(voterId, callback) {
    db.query(voterByIdQuery, [voterId], function(err, rows, fields) {
        callback(null, _.first(rows));
    });
};

module.exports = voter;
