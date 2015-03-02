"""  The module that produces statistics, maps and plots. """

from m5.utilities import DEBUG, FILL_1, FILL_2, SKIP, CENTER

from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np




class Stats():

    def __init__(self, session: Session, engine: Engine):
        """ Instantiate an empty object. """

        self.session = session
        self.engine = engine
        self.df = dict()

        self.orders = None
        self.clients = None
        self.checkins = None
        self.checkpoints = None

    def fetch_data(self):
        """ Pull the database tables into Pandas. """

        self.clients = pd.read_sql_table('client', self.engine, index_col='client_id')
        self.orders = pd.read_sql('order', self.engine, index_col='order_id', parse_dates=['date'])
        self.checkins = pd.read_sql('checkin', self.engine, index_col='checkin_id', parse_dates=['timestamp', 'after_', 'until'])
        self.checkpoints = pd.read_sql('checkpoint', self.engine, index_col='checkpoint_id')

        self.df['clients'] = self.clients
        self.df['orders'] = self.orders
        self.df['checkins'] = self.checkins
        self.df['checkpoints'] = self.checkpoints

        if DEBUG:
            pd.set_option('expand_frame_repr', False)
            print(self.clients)
            print(self.orders.tail(3500))
            print(self.checkins)
            print(self.checkpoints)

    def count_empty_cells(self):
        """ Count the number of empty cells (NaN and 0). """

        # This is definitely not the Pandas way to do it.
        # Especially when it comes to counting NaN instances.
        # But hey, it's a beginner's exercise like any other.
        reports = dict()
        count = dict()
        percentages = list()
        print(SKIP)

        indices = [('NaN', 'total'), ('NaN', '%'), ('Zero', 'total'), ('Zero', '%')]
        index = pd.MultiIndex.from_tuples(indices, names=['type', 'count'])

        for table_name, table in self.df.items():
            # Start by producing an empty report
            # table for each table in the database.
            columns = list(table.columns.values)
            reports[table_name] = pd.DataFrame(None, index=index, columns=columns)

            for column in columns:
                # In each column, we now look
                # for occurrences of 0 and NaN.
                series = self.df[table_name][column]
                conditions = {'Zero': series == 0, 'NaN': series.isnull()}

                for index_name, condition in conditions.items():
                    total = series[condition].size

                    count['total'] = total
                    count['%'] = total / series.size * 100

                    # Done: store the results in the right place inside the report table.
                    reports[table_name].loc[(index_name, 'total'), column] = count['total']
                    reports[table_name].loc[(index_name, '%'), column] = count['%']

            print('{title:{fill}{align}100}'.format(title=table_name, fill=FILL_2, align=CENTER))
            print(reports[table_name], end=SKIP)

            # Keep the percentages only for the graph
            percentages.append(reports[table_name].xs('%', level='count'))

        # Make a nice bar plot of the results
        percentages = pd.concat(percentages, join='inner', axis=1)
        print(percentages)
        percentages.plot(kind='bar')
        plt.show()

    def diagnose_data(self):
        """
        The quality of the data scraped from the website is crucial.
        This method gives a quick overview of what the data looks like.
        """

        print(SKIP)

        def percent(count, total=None):
            return (1 - count/total) * 100

        def iszero(cell):
            return True if cell is 0 else False

        # Table sizes
        # -----------------------------------------------------------------------------------------------------
        print('{title:{fill}{align}100}'.format(title='Table sizes', fill=FILL_1, align=CENTER), end=SKIP)

        print('Clients table: {shape}'.format(shape=self.clients.shape))
        print('Orders table: {shape}'.format(shape=self.orders.shape))
        print('Checkins table : {shape}'.format(shape=self.checkins.shape))
        print('Checkpoints table: {shape}'.format(shape=self.checkpoints.shape), end=SKIP)

        # Table info
        # -----------------------------------------------------------------------------------------------------
        print('{title:{fill}{align}100}'.format(title='Table infos', fill=FILL_1, align=CENTER), end=SKIP)

        print('{title:{fill}{align}50}'.format(title='CLIENTS', fill=FILL_2, align=CENTER))
        print(self.clients.info(), end=SKIP)

        print('{title:{fill}{align}50}'.format(title='ORDERS', fill=FILL_2, align=CENTER))
        print(self.orders.info(), end=SKIP)

        print('{title:{fill}{align}50}'.format(title='CHECKINS', fill=FILL_2, align=CENTER))
        print(self.checkins.info(), end=SKIP)

        print('{title:{fill}{align}50}'.format(title='CHECKPOINTS', fill=FILL_2, align=CENTER))
        print(self.checkpoints.info(), end=SKIP)

        # Count NaNs
        # -----------------------------------------------------------------------------------------------------
        print('{title:{fill}{align}100}'.format(title='NaN occurences', fill=FILL_1, align=CENTER), end=SKIP)
        pd.set_option('precision', 1)

        nan_clients = self.clients.count(axis=0).to_frame(name='count')
        nan_orders = self.orders.count(axis=0).to_frame(name='count')
        nan_checkins = self.checkins.count(axis=0).to_frame(name='count')
        nan_checkpoints = self.checkpoints.count(axis=0).to_frame(name='count')

        nan_orders['NaN (%)'] = nan_orders.apply(percent, total=self.orders.shape[0])
        nan_clients['NaN (%)'] = nan_clients.apply(percent, total=self.clients.shape[0])
        nan_checkins['NaN (%)'] = nan_checkins.apply(percent, total=self.checkins.shape[0])
        nan_checkpoints['NaN (%)'] = nan_checkpoints.apply(percent, total=self.checkpoints.shape[0])

        print('{title:{fill}{align}50}'.format(title='CLIENTS', fill=FILL_2, align=CENTER))
        print(nan_clients, end='\n\n')

        print('{title:{fill}{align}50}'.format(title='ORDERS', fill=FILL_2, align=CENTER))
        print(nan_orders, end='\n\n')

        print('{title:{fill}{align}50}'.format(title='CHECKINS', fill=FILL_2, align=CENTER))
        print(nan_checkins, end='\n\n')

        print('{title:{fill}{align}50}'.format(title='CHECKPOINTS', fill=FILL_2, align=CENTER))
        print(nan_checkpoints, end='\n\n')

        # Count Zeros
        # -----------------------------------------------------------------------------------------------------
        print('{title:{fill}{align}100}'.format(title='Zeros occurences', fill=FILL_1, align=CENTER), end=SKIP)

        iszero_all = np.vectorize(iszero)
        zeros_orders = iszero_all(self.orders.values)
        print(zeros_orders)
#
#         print(self.orders.groupby('overnight').size(), end='\n\n')
#         print(self.orders.groupby('fax_confirm').size(), end='\n\n')
#         print(self.orders.groupby('waiting_time').size(), end='\n\n')
#         print(self.orders.groupby('city_tour').size(), end='\n\n')
#         print(self.orders.groupby('extra_stops').size(), end='\n\n')
#         print(self.checkpoints.groupby('postal_code').size(), end='\n\n')
#         print(self.orders.groupby('client_id').size(), end='\n\n')


