SELECT count(*) as 'Women Abroad Voters' FROM voter
JOIN district ON voter.district_id_district = district.id_district
JOIN canton ON district.canton_id_canton = canton.id_canton
JOIN province ON canton.province_id_province = province.id_province
WHERE province.id_province = 8 and voter.sex = 2;

/*
+-------------------+
| Men Abroad Voters |
+-------------------+
|             15336 |
+-------------------+
*/