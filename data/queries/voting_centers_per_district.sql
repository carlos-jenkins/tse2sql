# Find voting center is a specific district
SELECT DISTINCT id_voting_center, voting_center.name, voting_center.district_id_district
FROM voting_center
WHERE voting_center.district_id_district = 111005;
/*
+------------------+-------------------------------------------------+----------------------+
| id_voting_center | name                                            | district_id_district |
+------------------+-------------------------------------------------+----------------------+
|        111005001 | Escuela Estado De Israel                        |               111005 |
|        111005002 | Colegio Tecnico Profesional Vazquez De Coronado |               111005 |
+------------------+-------------------------------------------------+----------------------+
*/
