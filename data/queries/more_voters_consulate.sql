SELECT count(*) AS Cantidad, district.name_district  FROM voter JOIN district ON voter.district_id_district = district.id_district JOIN canton ON district.canton_id_canton = canton.id_canton JOIN province ON canton.province_id_province = province.id_province WHERE province.id_province = 8 GROUP BY district.name_district ORDER BY Cantidad DESC;

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
*/
