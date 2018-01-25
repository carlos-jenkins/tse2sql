SELECT count(*) as 'Women', province.name_province
FROM voter
JOIN district ON voter.district_id_district = district.id_district
JOIN canton ON district.canton_id_canton = canton.id_canton
JOIN province ON canton.province_id_province = province.id_province
AND voter.sex = 2 GROUP BY province.name_province
ORDER BY Women DESC;

/*
+--------+---------------+
| Women  | name_province |
+--------+---------------+
| 571490 | San Jose      |
| 312920 | Alajuela      |
| 195205 | Cartago       |
| 169184 | Heredia       |
| 151629 | Puntarenas    |
| 132177 | Limon         |
| 119283 | Guanacaste    |
|  15336 | Consulado     |
+--------+---------------+
*/