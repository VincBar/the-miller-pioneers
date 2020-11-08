def line_info(df):
  line_numbers = df['linie'].unique()
  line_numbers.sort()
  all_lines = {}

  for n in range(line_numbers.shape[0]):
    one_line = df.loc[df['linie'] == line_numbers[n]]  # choose values for nth line
    one_line = one_line.sort_values(by=['km'])  # sort by distance from starting point
    all_lines[line_numbers[n]] = {
      "line_number": line_numbers[n],
      "line_name": one_line.linienname.to_list()[0],
      "n_stop": len(one_line),
      "lon": one_line['longitude'].to_list(),
      "lat": one_line['latitude'].to_list(),
      "stop_name": one_line['bezeichnung_bps'].to_list(),
      "abbr": one_line['abkurzung_bps'].to_list(),
    }

  abbr_dict = {}
  for index, line in df.iterrows():
    abbr_dict[line.abkurzung_bps] = dict(lon=line.longitude, lat=line.latitude, line_number=line.linie,
                                         line_name=line.linienname, stop_name=line.bezeichnung_bps)

  return all_lines, abbr_dict
