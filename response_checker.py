import requests
import json
import jsonschema
import copy
from urllib.parse import parse_qs


class ResponseChecker:
    def __init__(self, url, **kwargs):
        self.check_statement = True
        self.url = url
        self.status_code = kwargs.get("status_code")
        self.request_params = {
            "request_group": 0,
            "limit": 10,
            "sort": 0
        }
        qs_d = parse_qs(url)
        if qs_d.get("response_group") is not None:
            self.request_params["response_group"] = qs_d.get("response_group")[
                0]
        if qs_d.get("limit") is not None:
            self.request_params["limit"] = qs_d.get("limit")[
                0]
        if qs_d.get("sort") is not None:
            self.request_params["sort"] = qs_d.get("sort")[
                0]
        with open("response_schema.json") as fp:
            self.response_schema = json.load(fp)

    def check(self):
        self._get_json()
        if self._validate_response() and self._check_status_code():
            self.check_statement = False
        if self.status_code == 200:
            if self._limit_check() and self._sort_check():
                self.check_statement=False
        return self.check_statement

    def _validate_response(self):
        jsonschema.validate(self.response, self.response_schema)

    def _get_json(self):
        self.response = requests.get(self.url).json()
    def _check_status_code(self):
        if self.status_code != self.response.get("status_code"):
            return False
        return True
    def _limit_check(self):
        if len(self.response.get("result")) < self.request_params["limit"]:
            return False
        return True
    def _sort_check(self):
        expected_result = self.response["result"]
        if self.request_params["sort"]==0:
            # promotion_noで昇順
            expected_result.sort(key=lambda x:x["promotion_no"]) 
        elif self.request_params["sort"]==1:
            # promotion_noで降順
            expected_result.sort(key=lambda x:x["promotion_no"],reverse=True) 
        elif self.request_params["sort"]==2:
            # send_timeで昇順
            expected_result.sort(key=lambda x:x["send_time"])             
        elif self.request_params["sort"]==3:
            # send_timeで降順
            expected_result.sort(key=lambda x:x["send_time"],reverse=True) 
        else:
            expected_result = None
        if expected_result != self.response:
            return False
        return True

        