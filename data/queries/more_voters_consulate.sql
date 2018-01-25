SELECT COUNT(*) AS Cantidad, district.name_district FROM voter
JOIN district ON voter.district_id_district = district.id_district
JOIN canton ON district.canton_id_canton = canton.id_canton
JOIN province ON canton.province_id_province = province.id_province
WHERE province.id_province = 8 AND voter.sex = 2
GROUP BY district.name_district
ORDER BY Cantidad DESC;

/*
+----------+------------------+
| Cantidad | name_district    |
+----------+------------------+
|     8674 | Nueva York       |
|     3545 | Los Angeles      |
|     3408 | Miami            |
|     2300 | Atlanta          |
|     1845 | Houston          |
|     1841 | Washington       |
|      883 | Mexico           |
|      789 | Madrid           |
|      771 | Chicago          |
|      564 | Ciudad De Panama |
|      543 | Toronto          |
|      481 | Berlin           |
|      453 | Ottawa           |
|      440 | Managua          |
|      434 | Guatemala        |
|      390 | Caracas          |
|      371 | Paris            |
|      352 | Bogota           |
|      298 | Berna            |
|      295 | Londres          |
|      286 | San Salvador     |
|      251 | Roma             |
|      232 | Santiago         |
|      228 | Tegucigalpa      |
|      225 | Buenos Aires     |
|      225 | La Haya          |
|      169 | David            |
|      159 | Lima             |
|      147 | Bruselas         |
|      142 | Quito            |
|      123 | Sidney           |
|      116 | Santo Domingo    |
|      107 | Beijin           |
|      102 | Viena            |
|       91 | Brasilia         |
|       90 | Tel Aviv         |
|       79 | Tokio            |
|       67 | Chinandega       |
|       43 | La Habana        |
|       42 | Singapur         |
|       39 | Moscu            |
|       39 | Doha             |
|       39 | La Paz           |
|       35 | Shanghai         |
|       33 | Seul             |
|       29 | Asuncion         |
|       20 | Montevideo       |
|        9 | Nueva Delhi      |
|        9 | Belmopan         |
|        6 | Puerto España    |
|        3 | Kingston Jamaica |
|        2 | Ankara           |
+----------+------------------+

MEN:
+----------+------------------+
| Cantidad | name_district    |
+----------+------------------+
|     5214 | Nueva York       |
|     1644 | Miami            |
|     1617 | Los Angeles      |
|     1198 | Atlanta          |
|      975 | Washington       |
|      941 | Houston          |
|      405 | Chicago          |
|      391 | Mexico           |
|      378 | Madrid           |
|      307 | Toronto          |
|      279 | Berlin           |
|      261 | Ciudad De Panama |
|      253 | Ottawa           |
|      236 | Managua          |
|      180 | Guatemala        |
|      179 | Caracas          |
|      164 | Bogota           |
|      148 | Paris            |
|      128 | Londres          |
|      123 | Tegucigalpa      |
|      123 | San Salvador     |
|      122 | Berna            |
|      116 | Santiago         |
|      109 | Buenos Aires     |
|       96 | La Haya          |
|       86 | Roma             |
|       82 | Lima             |
|       72 | David            |
|       70 | Bruselas         |
|       68 | Quito            |
|       64 | Santo Domingo    |
|       63 | Sidney           |
|       57 | Beijin           |
|       52 | Brasilia         |
|       48 | Viena            |
|       39 | Tel Aviv         |
|       34 | Tokio            |
|       29 | Chinandega       |
|       25 | Moscu            |
|       21 | Singapur         |
|       20 | Asuncion         |
|       20 | Doha             |
|       19 | La Paz           |
|       18 | La Habana        |
|       16 | Shanghai         |
|       15 | Seul             |
|       13 | Montevideo       |
|        6 | Nueva Delhi      |
|        2 | Belmopan         |
|        1 | Puerto España    |
|        1 | Ankara           |
+----------+------------------+
51 rows in set (0.25 sec)

WOMEN:
+----------+------------------+
| Cantidad | name_district    |
+----------+------------------+
|     3460 | Nueva York       |
|     1928 | Los Angeles      |
|     1764 | Miami            |
|     1102 | Atlanta          |
|      904 | Houston          |
|      866 | Washington       |
|      492 | Mexico           |
|      411 | Madrid           |
|      366 | Chicago          |
|      303 | Ciudad De Panama |
|      254 | Guatemala        |
|      236 | Toronto          |
|      223 | Paris            |
|      211 | Caracas          |
|      204 | Managua          |
|      202 | Berlin           |
|      200 | Ottawa           |
|      188 | Bogota           |
|      176 | Berna            |
|      167 | Londres          |
|      165 | Roma             |
|      163 | San Salvador     |
|      129 | La Haya          |
|      116 | Santiago         |
|      116 | Buenos Aires     |
|      105 | Tegucigalpa      |
|       97 | David            |
|       77 | Lima             |
|       77 | Bruselas         |
|       74 | Quito            |
|       60 | Sidney           |
|       54 | Viena            |
|       52 | Santo Domingo    |
|       51 | Tel Aviv         |
|       50 | Beijin           |
|       45 | Tokio            |
|       39 | Brasilia         |
|       38 | Chinandega       |
|       25 | La Habana        |
|       21 | Singapur         |
|       20 | La Paz           |
|       19 | Doha             |
|       19 | Shanghai         |
|       18 | Seul             |
|       14 | Moscu            |
|        9 | Asuncion         |
|        7 | Belmopan         |
|        7 | Montevideo       |
|        5 | Puerto España    |
|        3 | Nueva Delhi      |
|        3 | Kingston Jamaica |
|        1 | Ankara           |
+----------+------------------+
52 rows in set (0.20 sec)
*/
