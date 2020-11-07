def line_info(df):
  line_numbers = df['linie'].unique()
  all_lines = []

  for n in range(line_numbers.shape[0]):
    one_line = df.loc[df['linie'] == line_numbers[n]]  # choose values for nth line
    one_line = one_line.sort_values(by=['km'])  # sort by distance from starting point


    line_dict = {
      "line_number": line_numbers[0],
      "line_name": one_line.linienname.to_list(),
      "n_stop": one_line.shape[0],
      "lon": one_line['longitude'].to_list(),
      "lat": one_line['latitude'].to_list(),
      "stop_name": one_line['bezeichnung_bps'].to_list(),
      "abbr": one_line['abkurzung_bps'].to_list(),
    }
    all_lines.append(line_dict)

  return all_lines
