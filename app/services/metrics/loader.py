import json
import os

from app.config import Config
from app.services.metrics.save_in_click import save_in_click


class MetricsLoader:

    def __init__(self):
        print(Config.clickhouse_host)
        for metric_config in Config.metric_configs:
            self.row_metrics = self.__get_row_metrics(
                metric_name=metric_config.get('name'),
                metric_query=metric_config.get('query')
            )
            for metric in self.row_metrics:
                self.__save_metric(
                    metric=metric,
                    metric_name=metric_config.get('name')
                )

    @staticmethod
    def __get_row_metrics(metric_name: str, metric_query: str) -> list[dict]:
        with open('test.json', 'r') as f:
            # Load the JSON data from the file
            response = json.load(f)
            data = response.get('data')
            result = data.get('result')
            print(result)
            return result

    def format_metric(self, metric: dict, metric_name: str) -> dict:
        metric_data = metric.get('metric')
        formatted_metric = {
            'timestamp': str(metric.get('value')[0]),
            'metric': metric_name,
            'param': metric_data.get('device', 'null'),
            'data_center': metric_data.get('data_center'),
            'host': metric_data.get('host'),
            'rack': metric_data.get('rack'),
            'team': metric_data.get('team'),
            'server_group': metric_data.get('server_group'),
            'value': metric.get('value')[1]
        }
        return formatted_metric

    def __save_metric(self, metric: dict, metric_name: str):

        formatted_metric = self.format_metric(metric, metric_name)
        try:
            save_in_click(formatted_metric)
        except Exception as e:
            self.save_in_tpm_json(formatted_metric)
            print(e)

        # except Exception as e:
#     print(e)

    @staticmethod
    def save_in_tpm_json(metric):
        json_list = [metric]
        file_path = '../../../tmp.json'
        # Проверяем, есть ли файл
        if os.path.exists(file_path):
            # Если файл уже существует, загружаем его содержимое
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            # Если файла нет, создаем пустой список
            data = []

        # Добавляем новые объекты в список
        data.extend(json_list)

        # Записываем обновленный список в файл
        with open(file_path, "w") as f:
            json.dump(data, f)
