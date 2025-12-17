#   IMPORTING REQUIRED MODULES
import argparse,sys,csv
from datetime import datetime,timedelta
from collections import Counter

def format_timedelta(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    days, remaining_seconds_d = divmod(total_seconds, 86400)
    hours, remainding_seconds_h = divmod(remaining_seconds_d, 3600)
    minutes, seconds = divmod(remainding_seconds_h, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"


#   DEFINING CORE FUNCTIONALITY
def ticket_report(csv_path: str, agent_filter: str | None=None):

    #   OPENING CSV FILE USING CSV DICTREADER
    with open(csv_path, "r", newline='') as src:
        data = csv.DictReader(src)     

        #   TICKET TOTAL COUNT AND SPLIT INTO DICTIONARIES
        line_counter = 0
        tickets_per_agent = Counter()
        tickets_per_status = Counter()
        tickets_per_priority = Counter()
        closed_tickets = []
        total_work_time = timedelta()

        #   PROCESSING OF DICTIONARY DATA
        for line in data:

            agent = line.get("agent", "Unknown")

            # Skip if filter is set but doesn’t match
            if agent_filter is not None and agent != agent_filter:
                continue

            #   COUNTING TOTAL NUMBER OF TICKETS
            line_counter += 1

            #   DECLARING VARIABLES FROM DICTIONARIES
            ticket_id = line.get("ticket_id", "Unknown Ticket ID")
            status = line.get("status", "Unknown Status")
            priority = line.get("priority", "Unknown Priority")
            created_at = line["created_at"]
            closed_at = line["closed_at"]
            
            #   PARSING FOR AGENTS
            tickets_per_agent[agent] += 1

            #   PARSING FOR STATUS AND ADDING TICKET TO DICTIONARY
            tickets_per_status[status] += 1

            # PARSING FOR PRIORITY
            tickets_per_priority[priority] += 1

            #   COLLECTING INFO ON CLOSED TICKETS
            DATE_TIME = '%Y-%m-%d %H:%M:%S'
            if status == "closed":
                #   CREATING DATETIME OBJECTS
                try:
                    dt_created_at = datetime.strptime(created_at, DATE_TIME)
                    dt_closed_at = datetime.strptime(closed_at, DATE_TIME)
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
                except (ValueError, TypeError) as e:
                    # Gracefully skip bad CSV row

                     print(f"\n⚠️ Skipping ticket {ticket_id}: invalid date format ({e})")
                     continue


        if closed_tickets:
            avg_time = total_work_time / len(closed_tickets)
            Average_Resolution_Time = format_timedelta(avg_time)
        else:
            Average_Resolution_Time = "N/A"


        if agent_filter is None:

            return{
                "total_tickets": line_counter,
                "tickets_per_agent": tickets_per_agent,
                "tickets_per_status": tickets_per_status,
                "tickets_per_priority": tickets_per_priority,
                "average_resolution_time": Average_Resolution_Time
            }
        
        #     print(f'''\nTicket Report for {csv_path}:
        #         \nTotal tickets: \t\t{line_counter}
        #         \nTickets by Status:\n''')
            
        #     for status, count in tickets_per_status.items():
        #         print(f'\t{status.capitalize()}: {count}')

        #     print('\nTickets per Agent:\n')
        #     for agent, count in tickets_per_agent.items():
        #         print(f'\t{agent}: {count}')

        #     print(f"\nAverage Resolution Time: {Average_Resolution_Time}\n")

        else:
            if agent_filter in tickets_per_agent:
                return {agent_filter: tickets_per_agent[agent_filter]}
            else:
                return {"error": f'There is either no Agent {agent_filter}, '
                      'or no tickets were assigned to that agent.'}

def main():

    #   CREATE THE PARSER
    parser = argparse.ArgumentParser(
        description="Allows the user to choose a source file"
    )

    #   ADD ARGUMENT
    parser.add_argument(
        "source",
        nargs="?",
        # default="ChatGPT/CSV_ticket_report/tickets.csv",
        default="tickets.csv",
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
        report = ticket_report(args.source,args.agent)
        # Unknown Agent filter
        if "error" in report:
            print(report["error"])
        # Known Agent filter
        elif args.agent:
            for agent, count in report.items():
                print(f"{agent.capitalize()}'s Ticket count is: {count}")
        # General Report
        else:
            print(f'''\nTicket Report for {args.source}:
                \nTotal tickets: \t\t{report["total_tickets"]}
                \nTickets by Status:\n''')
            
            for status, count in report["tickets_per_status"].items():
                print(f'\t{status.capitalize()}: {count}')

            print('\nTickets per Agent:\n')
            for agent, count in report["tickets_per_agent"].items():
                print(f'\t{agent}: {count}')

            print(f'\nAverage Resolution Time: {report["average_resolution_time"]}\n')

    except FileNotFoundError:
        print(f"Unable to find the source-file ('{args.source}').", file=sys.stderr)
        sys.exit(1)
            
            

# ticket_report("ChatGPT/CSV_ticket_report/tickets.csv")

if __name__ == "__main__":
    main()