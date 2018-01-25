SELECT id_district, name_district FROM district
JOIN canton ON district.canton_id_canton = canton.id_canton
JOIN province ON canton.province_id_province = province.id_province
WHERE province.id_province = 8
ORDER BY id_district ASC;

/*
+-------------+------------------+
| id_district | name_district    |
+-------------+------------------+
|      801001 | Berlin           |
|      802001 | Buenos Aires     |
|      803001 | Viena            |
|      804001 | Bruselas         |
|      805001 | Belmopan         |
|      806001 | Brasilia         |
|      807001 | Ottawa           |
|      807002 | Toronto          |
|      808001 | Santiago         |
|      809001 | Beijin           |
|      809002 | Shanghai         |
|      810001 | Bogota           |
|      811001 | Seul             |
|      812001 | La Habana        |
|      813001 | Quito            |
|      814001 | Atlanta          |
|      814002 | Houston          |
|      814003 | Los Angeles      |
|      814004 | Miami            |
|      814005 | Nueva York       |
|      814006 | Washington       |
|      814007 | Chicago          |
|      815001 | San Salvador     |
|      816001 | Madrid           |
|      817001 | Paris            |
|      818001 | Guatemala        |
|      819001 | Tegucigalpa      |
|      820001 | Tel Aviv         |
|      821001 | Roma             |
|      822001 | Tokio            |
|      823001 | Mexico           |
|      824001 | Chinandega       |
|      824002 | Managua          |
|      826001 | La Haya          |
|      827001 | Ciudad De Panama |
|      827002 | David            |
|      828001 | Lima             |
|      829001 | Londres          |
|      830001 | Santo Domingo    |
|      831001 | Moscu            |
|      832001 | Singapur         |
|      833001 | Berna            |
|      834001 | Puerto España    |
|      835001 | Montevideo       |
|      836001 | Caracas          |
|      837001 | Nueva Delhi      |
|      838001 | Doha             |
|      839001 | La Paz           |
|      840001 | Asuncion         |
|      841001 | Sidney           |
|      843001 | Kingston Jamaica |
|      844001 | Ankara           |
+-------------+------------------+
52 rows in set (0.01 sec)
*/
