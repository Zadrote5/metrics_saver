import clickhouse_connect

from app.config import Config

click_client = clickhouse_connect.get_client(
    host=Config.clickhouse_host,
    port=Config.clickhouse_port,
    # username=Config.clickhouse_user,
    # password=Config.clickhouse_pass
)


def save_in_click(metric: dict):
    query = f'INSERT INTO {Config.clickhouse_table}' \
            f' (timestamp, metric, param, data_center, host, rack, team, server_group, value) VALUES'
    query += ' ({}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {})'.format(
        metric['timestamp'],
        metric['metric'],
        metric['param'],
        metric['data_center'],
        metric['host'],
        metric['rack'],
        metric['team'],
        metric['server_group'],
        metric['value'],
    )
    result = click_client.query(query)
    return result
