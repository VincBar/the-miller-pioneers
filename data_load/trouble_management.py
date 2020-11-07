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

    def filter_by_time(self, start_time, end_time):
        self.working_dataset = self.constructions_dataset[
            (self.constructions_dataset["date_from"] >= pd.to_datetime(start_time, infer_datetime_format=True)) &
            (self.constructions_dataset["date_from"] <= pd.to_datetime(start_time, infer_datetime_format=True))]

    def filter_by_line(self, line):
        points = self.operation_points_dataset["abkurzung_bpk"][self.operation_points_dataset["linie"] == line]
        self.working_dataset = self.constructions_dataset[
            self.constructions_dataset["bp_from"].isin(points) | self.constructions_dataset["bp_to"].isin(points)]
