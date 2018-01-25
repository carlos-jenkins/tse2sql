CREATE FULLTEXT INDEX `name_idx` ON voter(name);

SELECT COUNT(*) FROM voter WHERE MATCH(name) AGAINST ('+Maria' IN BOOLEAN MODE);

/*
+----------+
| COUNT(*) |
+----------+
|   350171 |
+----------+
1 row in set (0.31 sec)
*/