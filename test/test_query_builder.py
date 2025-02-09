from test import BaseTestClass
from src.query_builder import QueryBuilder


class TestQueryBuilder(BaseTestClass):

    def test_query_builder_select_success(self):
        test_cases = [
            ({}, 'SELECT * FROM test_table', False),
            ({'columns': ['user_id', 'username', 'password']},
             'SELECT user_id, username, password FROM test_table', False),
            ({'columns': ['user_id', 'username'], 'where': {'status': True}},
             'SELECT user_id, username FROM test_table WHERE status = %s', False),
            ({'columns': ['user_id', 'username'], 'where': {'status': True}},
             'SELECT user_id, username FROM test_table WHERE status = %s ORDER BY updated_at DESC', True),
            ({'columns': ['user_id', 'username'], 'where': {'status': True, 'user_id': [
             1, 2]}}, 'SELECT user_id, username FROM test_table WHERE status = %s AND user_id IN (%s, %s) ORDER BY updated_at DESC', True)
            ]

        for query_params, expectative, apply_order_by in test_cases:
            query_builder = QueryBuilder(None).table('test_table')

            if len(query_params) == 0:
                result = query_builder.select()

            with self.subTest(query_params=query_params):
                if 'columns' in query_params:
                    query_builder = query_builder.select(*query_params['columns'])

                if 'where' in query_params:
                    query_builder = query_builder.where(**query_params['where'])

                if apply_order_by:
                    query_builder = query_builder.order_by('updated_at')

                result = query_builder.show()

                self.assertEqual(result, expectative)

    def test_query_builder_insert_success(self):
        test_cases = [
            ({'columns': ['username', 'password'], 'data': {'username': 'test_user',
             'password': '1234'}}, 'INSERT INTO test_table (username, password) VALUES (%s, %s)')
            ]

        for query_params, expectative in test_cases:
            query_builder = QueryBuilder(None).table('test_table')

            with self.subTest(query_params=query_params):
                query_builder.insert(*query_params['columns']).values(**query_params['data'])

                result = query_builder.show()

                self.assertEqual(result, expectative)

    def test_query_builder_update_success(self):
        test_cases = [
            ({'data': {'username': 'test_user', 'password': '1234'}},
             'UPDATE test_table SET username = %s, password = %s'),
            ({'data': {'username': 'test_user', 'password': '1234'}, 'where': {'status': True}},
             'UPDATE test_table SET username = %s, password = %s WHERE status = %s')
            ]

        for query_params, expectative in test_cases:
            query_builder = QueryBuilder(None).table('test_table')

            with self.subTest(query_params=query_params):
                query_builder = query_builder.update()

                if 'data' in query_params:
                    query_builder = query_builder.values(**query_params['data'])

                if 'where' in query_params:
                    query_builder = query_builder.where(**query_params['where'])

                result = query_builder.show()

                self.assertEqual(result, expectative)

    def test_query_builder_delete_success(self):
        test_cases = [
            ({}, 'DELETE FROM test_table'),
            ({'where': {'status': True}}, 'DELETE FROM test_table WHERE status = %s')
            ]

        for query_params, expectative in test_cases:
            query_builder = QueryBuilder(None).table('test_table')

            with self.subTest(query_params=query_params):
                query_builder = query_builder.delete()

                if 'where' in query_params:
                    query_builder = query_builder.where(**query_params['where'])

                result = query_builder.show()

                self.assertEqual(result, expectative)
