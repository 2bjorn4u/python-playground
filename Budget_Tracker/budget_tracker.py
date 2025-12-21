import csv
path = "Budget_Tracker\TXT251221150048.TAB"

with open(path, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")
    fieldnames = reader.fieldnames
    for row in reader:
        if "NL44INGB0005031103" in row["Description"]:
            print(row["Amount"], row["Transaction_Date"])
        # print(fieldname)
    # print("Columns:", reader.fieldnames)
    # print("----- first 5 rows -----")


    # for i, row in enumerate(reader):
    #     print(f"{row}\n")
    #     if i == 5:
    #         break