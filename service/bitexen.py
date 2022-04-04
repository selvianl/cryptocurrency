import json
import os

from cryptocurrency.settings import redis as client
import requests
from api.models import Transaction
from django.db.models import Max


class BitexenService:
    def __init__(self):
        self.host = os.environ.get("SERVICE_URL", "https://www.bitexen.com/api/v1")
        self.headers = {
            "accept": "application/json",
        }

    def _get_last_transactions(self):
        url = self.host + "/order_book/BTCTRY/"
        resp = requests.get(url, headers=self.headers)

        if resp.ok:
            cache_timestamp = (
                json.loads(client.get("time")) if client.get("time") else None
            )
            if not cache_timestamp:
                max_timestamp_in_db = (
                    Transaction.objects.all().aggregate(max=Max("time")).get("max")
                )
                last_timestamp_in_db = (
                    max_timestamp_in_db if max_timestamp_in_db else "1"
                )
                client.mset({"time": last_timestamp_in_db})
                cache_timestamp = json.loads(client.get("time"))

            content = json.loads(resp.content)
            if content.get("status") == "success":
                bulk_list = []

                # last row will be biggest timestamp
                datas = content["data"]["last_transactions"]
                datas = sorted(datas, key=lambda l: l["time"])

                for row in datas:
                    if row.get("time") > str(cache_timestamp):
                        bulk_list.append(
                            Transaction(
                                amount=row.get("amount"),
                                price=float(row.get("price")),
                                time=row.get("time"),
                                type=row.get("type"),
                            )
                        )
                # always set highest timestamp
                cache_timestamp = str(max(float(row.get("time")), cache_timestamp))
                client.mset({"time": cache_timestamp})
                return bulk_list
