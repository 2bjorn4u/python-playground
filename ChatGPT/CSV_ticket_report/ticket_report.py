import argparse,sys,csv

def ticket_report(csv_path: str):
    with open(csv_path, "r", newline='') as src:
        data = csv.DictReader(src)
        line_counter = 0
        open_tickets = 0
        closed_tickets = 0
        pending_tickets = 0
        tickets_per_agent = {}
        tickets_per_status = {}
        for line in data:
            agent = line["agent"]
            status = line["status"]
            if agent not in tickets_per_agent:
                tickets_per_agent[agent] = 0
            tickets_per_agent[agent] += 1
            if status not in tickets_per_status:
                tickets_per_status[status] = 0
            tickets_per_status[status] += 1
            line_counter += 1
            if line["status"] == "open":
                open_tickets += 1
            elif line["status"] == "closed":
                closed_tickets += 1
            elif line["status"] == "pending":
                pending_tickets =+ 1
        print(f'Total Ticket count: {line_counter}')
        print(f'Open Tickets: {open_tickets}')
        print(f'Pending Tickets: {pending_tickets}')
        print(f'Closed Tickets: {closed_tickets}')
        print(tickets_per_agent)
        print(tickets_per_status)
            
            

ticket_report("ChatGPT/CSV_ticket_report/tickets.csv")


#     with open(csv_path, "r", newline="") as src:
#         reader = csv.DictReader()
        
# #     pass


# # def main():
# #     pass

# with open("ChatGPT/CSV_ticket_report/tickets.csv", newline="") as csvfile, \
#     open("ChatGPT/CSV_ticket_report/placeholder.csv", "w", newline="") as newcsvfile:
#     reader = csv.reader(csvfile)
#     writer = csv.writer(newcsvfile)
#     # line_counter = 0
#     for row in reader:
#         # line_counter += 1
#         # print(f"{line_counter}: {line}")
#         writer.writerow(row)

# with open("ChatGPT/CSV_ticket_report/tickets.csv", "r", newline="") as src:
#         with open("ChatGPT/CSV_ticket_report\placeholder.csv", "w", newline="") as dst:
#             # fieldnames = ["ticket_id","status","priority","created_at","closed_at","agent"]
#             reader = csv.DictReader(src)
#             # writer = csv.DictWriter(dst, fieldnames=fieldnames)
#             print(type(reader))
#             for row in reader:
#                     # writer.writerow(row)
#                     print(f"\n{row}")
#                     print(type(row))