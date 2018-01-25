# To find the voting centers of a district but looking by a person id

SELECT id_voting_center, voting_center.name, voting_center.district_id_district
FROM voting_center
JOIN voter ON voter.district_id_district = voting_center.district_id_district
WHERE id_voter = <ID_PERSON>;

/*
+------------------+-------------------------------------------------+----------------------+
| id_voting_center | name                                            | district_id_district |
+------------------+-------------------------------------------------+----------------------+
|        111005001 | Escuela Estado De Israel                        |               111005 |
|        111005002 | Colegio Tecnico Profesional Vazquez De Coronado |               111005 |
+------------------+-------------------------------------------------+----------------------+
*/

# To find women in voting centers by voting center id
SELECT COUNT(*) AS Mujeres, voting_center.name AS `Centro de Votacion`
FROM voter
JOIN site_per_voting_center ON voter.id_site = site_per_voting_center.id_site
JOIN voting_center ON  site_per_voting_center.voting_center_id_voting_center = voting_center.id_voting_center
WHERE voting_center.id_voting_center = 111005001 AND voter.sex = 2
GROUP BY voting_center.name
ORDER BY Mujeres DESC;
/*
+---------+--------------------------+
| Mujeres | Centro de Votacion       |
+---------+--------------------------+
|    6321 | Escuela Estado De Israel |
+---------+--------------------------+
1 row in set (0.11 sec)
*/

# To find women in voting centers by district id
SELECT COUNT(*) AS Mujeres, voting_center.name AS `Centro de Votacion`
FROM voter
JOIN site_per_voting_center ON voter.id_site = site_per_voting_center.id_site
JOIN voting_center ON  site_per_voting_center.voting_center_id_voting_center = voting_center.id_voting_center
WHERE voting_center.district_id_district = 111005 AND voter.sex = 2
GROUP BY voting_center.name
ORDER BY Mujeres DESC;
/*
+---------+-------------------------------------------------+
| Mujeres | Centro de Votacion                              |
+---------+-------------------------------------------------+
|    6321 | Escuela Estado De Israel                        |
|    2534 | Colegio Tecnico Profesional Vazquez De Coronado |
+---------+-------------------------------------------------+
2 rows in set (0.11 sec)
*/
