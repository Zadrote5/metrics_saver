import os

from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


class Config:
    tmp_read_period = os.getenv('TMP_READ_PERIOD')
    api_read_period = os.getenv('API_READ_PERIOD')
    redis_url = os.getenv('REDIS_URL')
    clickhouse_port = os.getenv('CLICKHOUSE_PORT')
    clickhouse_table = os.getenv('CLICKHOUSE_TABLE')
    clickhouse_host = os.getenv('CLICKHOUSE_HOST')
    clickhouse_user = os.getenv('CLICKHOUSE_USER')
    clickhouse_pass = os.getenv('CLICKHOUSE_PASS')

    metric_configs = [
        {
            'name': 'CPU',
            'query': "(sum by(instance,data_center,rack,server_group,env,team,host)"
                     " (irate(node_cpu_seconds_total{source='node_exporter',env='prod'"
                     ",team='tarm',mode!='idle'}[5m])) / on(instance) group_left sum by"
                     " (instance)((irate(node_cpu_seconds_total{source='node_exporter'"
                     ",env='prod',team='tarm'}[5m])))) * 100"
        },
        {
            'name': 'DISKIO',
            'query': "irate(node_disk_io_time_seconds_total{source='node_exporter',"
                     "env='prod',team='tarm',device=~'[a-z]+|nvme[0-9]+n[0-9]+|mmcblk[0-9]+'} [5m])"
        }
    ]
