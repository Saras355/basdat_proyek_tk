import uuid
from django.db import connection

def query_add(query):
  connection.cursor().execute(query)
  connection.close()

def query_result_two(query):
  with connection.cursor() as cursor:
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query_result(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description] 
        results = cursor.fetchall()
        data = []
        for row in results:
            data.append(dict(zip(columns, row))) 
        return data

# def query_result(query, params=None):
#     with connection.cursor() as cursor:
#         cursor.execute(query, params)
#         columns = [col[0] for col in cursor.description]
#         results = [
#             dict(zip(columns, row))
#             for row in cursor.fetchall()
#         ]
#         # Convert UUID fields to strings
#         for result in results:
#             for key, value in result.items():
#                 if isinstance(value, uuid.UUID):
#                     result[key] = str(value)
#         return results


def parse(result):
    data = result[0][0]
    return data