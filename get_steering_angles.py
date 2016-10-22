with open("center_camera.ts", "r") as f:
  cc_ts = f.readlines()

with open("steering.ts", "r") as f:
  ts_sa = f.readlines()

ts_to_sa = {}
for line in ts_sa:
  parts = line.split(" ")
  ts_to_sa[int(parts[0])] = float(parts[1])

with open("labels", "wb") as f:
  for ts in cc_ts:
    ts = int(ts.replace("\n", ""))
    if ts in ts_to_sa:
      f.write(str(ts_to_sa[ts]))
      f.write("\n")
    else:
      if ts + 50 in ts_to_sa:
        f.write(str(ts_to_sa[ts+50]))
        f.write("\n")
      elif ts - 50 in ts_to_sa:
        f.write(str(ts_to_sa[ts-50]))
        f.write("\n")
