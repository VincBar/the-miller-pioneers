import pandas as pd


class TroubleManager:
    def __init__(self, constructions_dataset, operation_points_dataset):
        self.constructions_dataset = constructions_dataset
        self.constructions_dataset["date_from"] = pd.to_datetime(self.constructions_dataset["date_from"],
                                                                 infer_datetime_format=True)
        self.constructions_dataset["date_to"] = pd.to_datetime(self.constructions_dataset["date_to"],
                                                               infer_datetime_format=True)
        self.operation_points_dataset = operation_points_dataset
        self.working_dataset = self.constructions_dataset

        self.filters_used = {}

    def reset_filters(self):
        self.working_dataset = self.constructions_dataset
        self.filters_used = {}

    def apply_filters(self):
        self.working_dataset = self.constructions_dataset
        for f_name, args in self.filters_used.items():
            if f_name == "time":
                self.filter_by_time(*args)
            elif f_name == "line":
                self.filter_by_line(args)

    def filter_by_time(self, start_time, end_time):
        if "time" in self.filters_used:
            self.filters_used.pop("time")
            self.apply_filters()
        self.filters_used["time"] = (start_time, end_time)
        self.working_dataset = self.working_dataset[
            (self.working_dataset["date_from"] >= pd.to_datetime(start_time, infer_datetime_format=True)) &
            (self.working_dataset["date_from"] <= pd.to_datetime(end_time, infer_datetime_format=True))]

    def filter_by_line(self, line):
        if "line" in self.filters_used:
            self.filters_used.pop("line")
            self.apply_filters()
        self.filters_used["line"] = line
        points = self.operation_points_dataset["abkurzung_bpk"][self.operation_points_dataset["linie"] == line]
        self.working_dataset = self.working_dataset[
            self.working_dataset["bp_from"].isin(points) | self.working_dataset["bp_to"].isin(points)]

    def get_working_dataset(self):
        return_dataset = self.working_dataset.copy()
        return_dataset["date_from"] = pd.DatetimeIndex(return_dataset.loc[:, "date_from"]).strftime("%Y-%m-%d")
        return_dataset["date_to"] = pd.DatetimeIndex(return_dataset.loc[:, "date_to"]).strftime("%Y-%m-%d")
        return return_dataset
