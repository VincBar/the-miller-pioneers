import requests
import pandas as pd


def lat_long_from_geopos(geopos):
    lat = max(geopos[0], geopos[1])
    lon = min(geopos[0], geopos[1])
    return lat, lon


class DataLoader:
    REQUEST_API = None
    LOAD_FIELDS = None

    params = {"rows": str(-1)}

    def get_data_from_fields(self, fields):
        res = {}
        for k, v in fields:
            if k in self.LOAD_FIELDS:
                if k == "geopos":
                    res["latitude"], res["longitude"] = lat_long_from_geopos(v)
                else:
                    res[k] = v
        return res

    def set_sort(self, param):
        self.params["sort"] = "-{}".format(param)
        return self

    def set_n(self, n):
        self.params["rows"] = str(n)
        return self

    def load(self):
        r = requests.get(self.REQUEST_API, params=self.params)
        data = r.json()["records"]
        data_list = [self.get_data_from_fields(d["fields"].items()) for d in data]
        return pd.DataFrame(data_list)


class LineLoader(DataLoader):
    REQUEST_API = "https://data.sbb.ch/api/records/1.0/search/?dataset=linie-mit-betriebspunkten"
    LOAD_FIELDS = {"linie", "km", 'abkurzung_bpk'}

    params = {"rows": str(-1), "facet": "linie"}

    def set_sort_lines(self):
        return self.set_sort("linie")

    def filter_line(self, line):
        self.params["refine.linie"] = str(line)
        return self


class ConstructionSiteLoader(DataLoader):
    REQUEST_API = "https://data.sbb.ch/api/records/1.0/search/?dataset=construction-site"
    LOAD_FIELDS = {"bp_from", "bp_to", 'region', 'reduction_capacity',
                   "umsetzung_intervalltyp_umleitung", "date_from", "date_to"}

    params = {"rows": str(-1), "facet": "region"}

    def set_sort_start_time(self):
        self.params["sort"] = "-date_from"
        return self

    def filter_region(self, region):
        self.params["refine.region"] = str(region)
        return self


class RoutesLoader(DataLoader):
    REQUEST_API = "https://data.sbb.ch/api/records/1.0/search/?dataset=zugzahlen"
    LOAD_FIELDS = {"strecke", "bp_von_abschnitt", "geschaeftscode", "bp_bis_abschnitt",
                   "gesamtbelastung_bruttotonnen", "anzahl_zuege"}

    params = {"rows": str(-1)}

    def load(self):
        df = super().load()
        df["geschaeftscode"] = (df["geschaeftscode"] == "PERSONENVERKEHR")
        df = df.rename(columns={"geschaeftscode": "is_passenger", "gesamtbelastung_bruttotonnen": "size", "in_richtung": "direction",
                                "anzahl_zuege": "num_trains", "bp_von_abschnitt": "bp_from", "bp_bis_abschnitt": "bp_to"})

        return df
