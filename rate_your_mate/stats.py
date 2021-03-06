from flask_restful import Resource
import csv
from rate_your_mate.config import (
    CATEGORIES_STATS_CSV_FILE_PATH,
    USERS_STATS_CSV_FILE_PATH,
    CSV_DELIMITER,
    CATEGORIES_CSV_HEADER,
    USERS_CSV_HEADER,
)
from rate_your_mate.mocks import CATEGORIES
from rate_your_mate.config import CHARTS_DIRECTORY_PATH
import os


def save_data_to_csv():
    with open(CATEGORIES_STATS_CSV_FILE_PATH, "w") as categories_csv_file:
        with open(USERS_STATS_CSV_FILE_PATH, "w") as users_csv_files:
            categories_writer = csv.writer(
                categories_csv_file,
                delimiter=CSV_DELIMITER,
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )
            users_writer = csv.writer(
                users_csv_files,
                delimiter=CSV_DELIMITER,
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            categories_writer.writerow(CATEGORIES_CSV_HEADER)
            users_writer.writerow(USERS_CSV_HEADER)

            for category_id, category in CATEGORIES.items():
                for date, date_data in category["dates"].items():
                    categories_writer.writerow([category_id, date, date_data["stars"]])
                    for user_id, user in date_data["users"].items():
                        users_writer.writerow(
                            [user_id, category_id, date, user["stars"]]
                        )


def read_all_charts_files():
    charts = {}
    for root, dirs, files in os.walk(CHARTS_DIRECTORY_PATH):
        for file in files:
            if file.endswith(".csv"):
                category_id = file.split(".")[0]
                charts[category_id] = {
                    "id": category_id,
                    "name": CATEGORIES[category_id]["name"],
                    "data": [],
                }
                with open(os.path.join(CHARTS_DIRECTORY_PATH, file), mode="r") as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    line_count = 0
                    for row in csv_reader:
                        charts[category_id]["data"].append(
                            {"date": row["DATE"], "stars": row["STARS"]}
                        )

    return charts


class Stats(Resource):
    def get(self) -> str:
        return read_all_charts_files()

    def head(self) -> dict:
        save_data_to_csv()
        return {}
