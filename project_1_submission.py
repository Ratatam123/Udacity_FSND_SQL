import psycopg2        
import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


formatter = logging.Formatter(
    '%(message)s')

file_handler = logging.FileHandler('project_1_submission.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

query_1 = """ SELECT articles.title,
                CAST(freq_dist_views.num AS INTEGER) AS number_of_views
            FROM freq_dist_views
            RIGHT JOIN articles ON freq_dist_views.path LIKE CONCAT('%', articles.slug, '%')
            ORDER BY number_of_views DESC
            LIMIT 3
            """

query_2 = """ SELECT authors_and_slugs.name AS author_name,
                CAST(sum(freq_dist_views.num) AS INTEGER) AS views
            FROM freq_dist_views
            RIGHT JOIN authors_and_slugs ON freq_dist_views.path LIKE CONCAT('%', authors_and_slugs.slug, '%')
            GROUP BY author_name
            ORDER BY views DESC
            """

query_3 = """ SELECT TO_CHAR(dates_and_failrates.dates, 'Month, DD, YYYY'),
                ROUND(dates_and_failrates.failure_rate, 1)
            FROM
                (SELECT dates,
                    (round(failures / (successes+failures)::numeric, 3)*100) 
            AS failure_rate
                FROM
                    (SELECT dates_and_status.dates,
                        sum(CASE
                                WHEN status='200 OK' THEN 1
                                ELSE 0
                            END) AS successes,
                        sum(CASE
                                WHEN status='404 NOT FOUND' THEN 1
                                ELSE 0
                            END) AS failures
                    FROM dates_and_status
                    GROUP BY dates_and_status.dates) AS dates_success_failures) 
                AS dates_and_failrates
            WHERE failure_rate > 1
            """

query_dictionary = OrderedDict([
    ('task_1', ('The three most read articles of all time are: ', query_1)),
    ('task_2', ('The most read article authors are: ', query_2)),
    ('task_3', ('On the following date(s) more than 1 percent of the requests for an article failed: ', query_3))
    ])


def log_search_results(database_name, logger, query_dict):
    db = psycopg2.connect(dbname = database_name)
    cursor = db.cursor()
    for key, values in query_dict.items():
        question_to_answer =  values[0]
        query = values[1]
        cursor.execute(query)
        results = cursor.fetchall()
        counter = 1
        for result in results:
            if key == "task_3":
                logger.info(question_to_answer + '\n\t\t\t{} -- {} percent'.format(result[0], result[1]))
            else:
                if counter == 1 :     
                    logger.info(question_to_answer + '\n\n\t\t\t' +  str(counter) + '. \"{}\" -- {} reads\n'.format(result[0], result[1]))
                else:
                    logger.info('\t\t\t' + str(counter) + '. \"{}\" -- {} reads\n'.format(result[0], result[1]))
            counter += 1
    
    db.close()

if __name__ == "__main__":
    
    log_search_results("news", logger, query_dictionary)



