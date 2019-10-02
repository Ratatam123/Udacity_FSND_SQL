# Fullstack Nanodegree; Project 1; 2019

## Info
The project comprises a python script and a txt-file with a sample of its output that is normally written to a log-file.
The python script comprises 3 psql-queries that in turn are making use of the _views_ listed below and a function that sends the queries to the _news_ database and writes the results to a log-file. The file normally expects a sql-database to be in the same folder. The queries are handed to the function _log_search_results_ in form of a dictionary with _task_1_, _task_2_, _task_3_ as keys and the questions to be answered as well as the queries as values. The script is run like any regular python script in the shell: _python3 project_1_submission.py_

## Views used in psql queries

### used in queries 1 & 2

CREATE VIEW freq_dist_views AS
SELECT count(PATH) AS num,
       PATH
FROM log
WHERE (PATH LIKE '_article%')
  AND (status = '200 OK')
GROUP BY PATH;

### used in query 2:

CREATE VIEW authors_and_slugs AS
SELECT articles.slug,
       authors.name
FROM articles
INNER JOIN authors ON articles.author = authors.id;

### used in query 3

CREATE VIEW dates_and_status AS
SELECT date(time) AS dates,
       status
FROM log;
