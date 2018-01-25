SELECT count(*) as 'Women', province.name_province
FROM voter
JOIN district ON voter.district_id_district = district.id_district
JOIN canton ON district.canton_id_canton = canton.id_canton
JOIN province ON canton.province_id_province = province.id_province
AND voter.sex = 2 GROUP BY province.name_province;

/*
+--------+---------------+
| Women  | name_province |
+--------+---------------+
| 312920 | Alajuela      |
| 195205 | Cartago       |
|  15336 | Consulado     |
| 119283 | Guanacaste    |
| 169184 | Heredia       |
| 132177 | Limon         |
| 151629 | Puntarenas    |
| 571490 | San Jose      |
+--------+---------------+
*/