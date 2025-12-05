import argparse,sys,csv

# def ticket_report(csv_path: str):
#     pass


# def main():
#     pass

with open("ChatGPT/CSV_ticket_report/tickets.csv") as csvfile:
    line_counter = 0
    for line in csvfile:
        line_counter += 1
        print(f"{line_counter}: {line}")