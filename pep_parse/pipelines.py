import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent


class PepParsePipeline:
    total_peps = 0

    def __init__(self):
        self.pep_status_count = None

    def open_spider(self, spider):
        self.pep_status_count = defaultdict(int)

    def process_item(self, item, spider):
        self.total_peps += 1
        self.pep_status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        total_peps = self.total_peps
        date_format = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file = BASE_DIR / 'results' / f'status_summary_{date_format}.csv'

        with open(file, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Статус', 'Количество'])
            writer.writerows(self.pep_status_count.items())
            writer.writerow(['Total', total_peps])
