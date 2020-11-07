import requests
import pandas as pd


def lat_long_from_geopos(geopos):
    lat = max(geopos[0], geopos[1])
    lon = min(geopos[0], geopos[1])
    return lat, lon


class LineLoader:
    REQUEST_API = "https://data.sbb.ch/api/records/1.0/search/?dataset=linie-mit-betriebspunkten"
    LOAD_FIELDS = {"linie", "km", 'abkurzung_bpk', 'abkurzung_bps'}

    params = {"rows": str(-1), "facet": "linie"}

    @staticmethod
    def get_data_from_fields(fields):
        res = {}
        for k, v in fields:
            if k == "geopos":
                res["latitude"], res["longitude"] = lat_long_from_geopos(v)
            elif k in LineLoader.LOAD_FIELDS:
                res[k] = v

        return res

    def set_sort_lines(self):
        self.params["sort"] = "-linie"
        return self

    def set_n(self, n):
        self.params["rows"] = str(n)
        return self

    def filter_line(self, line):
        self.params["refine.linie"] = str(line)
        return self

    def load(self):
        r = requests.get(LineLoader.REQUEST_API, params=self.params)
        data = r.json()["records"]
        data_list = [LineLoader.get_data_from_fields(d["fields"].items()) for d in data]
        return pd.DataFrame(data_list)
