from .logs import add_to_log
from .configs import get_config
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame

def execute_sql(query):
    """
    :param query: the query which need to be run
    :return: query output in dataframe
    """
    login = get_config('db')
    user = login.get('username')
    password = login.get('password')
    host = login.get('host')
    port = login.get('port')
    db = login.get('dbname')
    url = 'postgres://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

    engine = create_engine(url)

    df = pd.read_sql_query(query, con=engine)

    add_to_log("Query output been returned")

    return df
