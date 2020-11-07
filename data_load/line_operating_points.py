import requests
import pandas as pd


def lat_long_from_geopos(geopos):
    lat = max(geopos[0], geopos[1])
    lon = min(geopos[0], geopos[1])
    return lat, lon


def line_info(df):
    line_numbers = df['linie'].unique()
    all_lines = []

    for n in range(line_numbers.shape[0]):

        one_line = df.loc[df['linie'] == line_numbers[n]]  # choose values for nth line
        one_line = one_line.sort_values(by=['km'])  # sort by distance from starting point

        line_dict = {
            "line_number": one_line.linie[n],
            "line_name": one_line.linienname[n],
            "n_stop": one_line.shape[0],
            "lon": one_line['longitude'].to_list(),
            "lat": one_line['longitude'].to_list(),
            "stop_name": one_line['bezeichnung_bps'].to_list(),
            "abbr": one_line['abkurzung_bps'].to_list(),
        }
        #print(int(line_numbers[n]))
        # line_numbers[n].to_string()
        #int(line_numbers[n])
        all_lines.append(line_dict)

    return one_line, all_lines




class LineLoader:
    REQUEST_API = "https://data.sbb.ch/api/records/1.0/search/?dataset=linie-mit-betriebspunkten"
    LOAD_FIELDS = {"linie", "km", 'abkurzung_bpk', 'abkurzung_bps', 'linienname', "bezeichnung_bps"}

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


loader = LineLoader()
d = loader.set_sort_lines()
d = loader.load()

[blub, blab] = line_info(d)

#loader.set_n(4).load()


print(line_info(d))

