from data_load.loader import LineLoader


def filter_small_lines(df, km=5):
    g = df[["linie", "km"]].groupby("linie").max()
    d_filter = df.loc[df["linie"].isin(g[g > km].dropna().index)]
    return d_filter


def line_info(df):
    line_numbers = df['linie'].unique()
    all_lines = []

    for n in range(line_numbers.shape[0]):

        one_line = df.loc[df['linie'] == line_numbers[n]]  # choose values for nth line
        one_line = one_line.sort_values(by=['km'])  # sort by distance from starting point

        line_dict = {
            "line_number": one_line.linie.iloc[0],
            "line_name": one_line.linienname.iloc[0],
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


if "__name__" == "__main__":
    loader = LineLoader()
    loader.set_sort_lines()
    d = loader.load()

    [blub, blab] = line_info(d)

    #loader.set_n(4).load()


    print(line_info(d))