#   IMPORTING REQUIRED MODULES
import argparse,sys,csv
from datetime import datetime,timedelta

#   DEFINING CORE FUNCTIONALITY
def ticket_report(csv_path: str):

    #   OPENING CSV FILE USING CSV DICTREADER
    with open(csv_path, "r", newline='') as src:
        data = csv.DictReader(src)     

        #   TICKET TOTAL COUNT AND SPLIT INTO DICTIONARIES
        line_counter = 0
        agents = []
        tickets_per_agent = {}
        tickets_per_status = {}
        tickets_per_priority = {}
        closed_tickets = []
        total_work_time = timedelta()

        #   PROCESSING OF DICTIONARY DATA
        for line in data:

            #   COUNTING TOTAL NUMBER OF TICKETS
            line_counter += 1

            #   DECLARING VARIABLES FROM DICTIONARIES
            ticket_id = line["ticket_id"]
            status = line["status"]
            priority = line["priority"]
            agent = line["agent"]
            created_at = line["created_at"]
            closed_at = line["closed_at"]
            
            #   PARSING FOR AGENTS
            if agent not in tickets_per_agent:
                tickets_per_agent[agent] = 0
            tickets_per_agent[agent] += 1
            if agent not in agents:
                agents.append(agent)

            #   PARSING FOR STATUS AND ADDING TICKET TO DICTIONARY
            if status not in tickets_per_status:
                tickets_per_status[status] = 0
            tickets_per_status[status] += 1

            # PARSING FOR PRIORITY
            if priority not in tickets_per_priority:
                tickets_per_priority[priority] = 0
            tickets_per_priority[priority] += 1

            #   COLLECTING INFO ON CLOSED TICKETS
            if status == "closed":
                #   CREATING DATETIME OBJECTS
                dt_created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                dt_closed_at = datetime.strptime(closed_at, '%Y-%m-%d %H:%M:%S')
                worked_time = dt_closed_at - dt_created_at
                worked_time_stringified = str(worked_time)
                closed_tickets.append(
                    {
                        "Ticket ID": ticket_id, 
                        "Created at:": dt_created_at,
                        "Closed at:": dt_closed_at,
                        "Worked time:": worked_time_stringified
                    }
                )
                total_work_time += worked_time
        Average_Resolution_Time = str(total_work_time / len(closed_tickets))


        print(f'''\nTicket Report for "{csv_path}":
              
                Total tickets: {line_counter}

                Tickets by status:
                    Open: {tickets_per_status['open']}
                    Pending: {(tickets_per_status['pending'])}
                    Closed: {(tickets_per_status['closed'])} 
              ''')
    for agent in agents:
        print(f"{agent}'s tickets: {tickets_per_agent[agent]}")
    print(f"\nAverage Resolution Time: {Average_Resolution_Time}\n")

def main():

    #   CREATE THE PARSER
    parser = argparse.ArgumentParser(
        description="Allows the user to choose a source file"
    )

    #   ADD ARGUMENT
    parser.add_argument(
        "source",
        nargs="?",
        default="ChatGPT/CSV_ticket_report/tickets.csv",
        help="Source log file (default: tickets.csv)"
    )

    #   ADD OPTIONAL ARGUMENT
    parser.add_argument(
        "-a", "--agent",
        nargs="?",
        default=None,
        help="Allows you to filter by Agent name"
        )
    
    #   PARSE ARGUMENTS
    args = parser.parse_args()

    #   CALL FUNCTION
    try:
        report = ticket_report(args.source)
    except FileNotFoundError:
        print(f"Unable to find the source-file ('{args.source}').", file=sys.stderr)
        sys.exit(1)
            
            

# ticket_report("ChatGPT/CSV_ticket_report/tickets.csv")

if __name__ == "__main__":
    main()