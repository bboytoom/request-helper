
class QueryBuilder:
    def __init__(self, db):
        self.db = db
        self.table_name = None
        self.query = ''
        self.params = []
        self.columns = []
        self.update_values = {}

    def table(self, table: str):
        self.table_name = table

        return self

    def select(self, *columns):
        if not self.table_name:
            raise ValueError('You must specify a table')

        col = ', '.join(columns) if columns else '*'
        self.query = f'SELECT {col} FROM {self.table_name}'

        return self

    def insert(self, *columns):
        if not self.table_name:
            raise ValueError('You must specify a table')

        if not columns:
            raise ValueError('You must specify one column')

        self.columns = columns

        return self

    def update(self):
        if not self.table_name:
            raise ValueError('You must specify a table')

        return self

    def delete(self):
        if not self.table_name:
            raise ValueError('You must specify a table')

        self.query = f'DELETE FROM {self.table_name}'

        return self

    def values(self, **values):
        if not self.table_name:
            raise ValueError('You must specify a table')

        if not values:
            raise ValueError('You must provide at least one value')

        if self.columns:
            if set(values.keys()) != set(self.columns):
                raise ValueError('Provided values do not match specified columns')

            placeholders = ', '.join(['%s'] * len(values))
            col_names = ', '.join(self.columns)
            self.query = f'INSERT INTO {self.table_name} ({col_names}) VALUES ({placeholders})'
            self.params = list(values.values())
        else:
            set_clause = ', '.join([f'{key} = %s' for key in values.keys()])
            self.query = f'UPDATE {self.table_name} SET {set_clause}'
            self.params = list(values.values())

        return self

    def where(self, **conditions):
        if not conditions:
            return self

        where_clauses = []

        for key, value in conditions.items():
            if isinstance(value, (list, tuple)):
                placeholders = ', '.join(['%s'] * len(value))
                where_clauses.append(f'{key} IN ({placeholders})')

                self.params.extend(value)
            else:
                where_clauses.append(f'{key} = %s')
                self.params.append(value)

        self.query += ' WHERE ' + ' AND '.join(where_clauses)

        return self

    def order_by(self, column: str, order: str = 'DESC'):
        self.query += f' ORDER BY {column} {order}'

        return self

    def show(self):
        return self.query

    def execute(self, query=None):
        try:
            with self.db.cursor() as cursor:
                if query:
                    cursor.execute(self.query)
                else:
                    cursor.execute(self.query, tuple(self.params))

                self.db.commit()

                return True
        except Exception as e:
            raise ValueError(f'Error {e}')

    def all(self, query=None):
        try:
            with self.db.cursor() as cursor:

                if query:
                    cursor.execute(self.query)
                else:
                    cursor.execute(self.query, tuple(self.params))

                query_all = cursor.fetchall()

                if not query_all:
                    return None

                return [dict(zip(self.columns, values)) for values in query_all]
        except Exception as e:
            raise ValueError(f'Error {e}')

    def one(self, query=None):
        try:
            with self.db.cursor() as cursor:
                if query:
                    cursor.execute(self.query)
                else:
                    cursor.execute(self.query, tuple(self.params))

                query_one = cursor.fetchone()

                if not query_one:
                    return None

                return dict(zip(self.columns, query_one))
        except Exception as e:
            raise ValueError(f'Error {e}')
