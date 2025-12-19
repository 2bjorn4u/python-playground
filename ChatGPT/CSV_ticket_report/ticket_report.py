# Importing required Modules
import argparse,sys,csv
from datetime import datetime,timedelta
from collections import Counter
DATE_TIME = '%Y-%m-%d %H:%M:%S'

def format_timedelta(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    days, remaining_seconds_d = divmod(total_seconds, 86400)
    hours, remaining_seconds_h = divmod(remaining_seconds_d, 3600)
    minutes, seconds = divmod(remaining_seconds_h, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"


# Defining core function
def ticket_report(csv_path: str, agent_filter: str | None=None):
    if agent_filter:
        agent_filter = agent_filter.strip()

    # Opening CSV file using DictReader
    with open(csv_path, "r", newline="", encoding="utf-8") as src:
        data = csv.DictReader(src)

        # Declaring essential variables
        ticket_count = 0
        tickets_per_agent = Counter()
        tickets_per_status = Counter()
        tickets_per_priority = Counter()
        closed_counter =0
        total_work_time = timedelta()

        # Processing Dictionary Data
        for line in data:

            agent = (line.get("agent") or "Unknown").strip()

            # Skip if filter is set but doesn’t match
            if agent_filter and agent != agent_filter:
                continue

            # Counting total number of tickets
            ticket_count += 1

            # Getting dictionary values from DictReader CSV
            ticket_id = line.get("ticket_id", "Unknown Ticket ID")
            status = (line.get("status") or "Unknown Status").strip().lower()
            priority = (line.get("priority") or "Unknown Priority").strip()
            created_at = line.get("created_at")
            closed_at = line.get("closed_at")
            
            # Parsing for Agents, Status, Priority
            tickets_per_agent[agent] += 1
            tickets_per_status[status] += 1
            tickets_per_priority[priority] += 1

            # Gathering Closed Tickets Metrics
            
            if status == "closed":
                # Converting Date/Time data to Datetime objects
                try:
                    dt_created_at = datetime.strptime(created_at, DATE_TIME)
                    dt_closed_at = datetime.strptime(closed_at, DATE_TIME)
                    worked_time = dt_closed_at - dt_created_at
                    closed_counter +=1
                    total_work_time += worked_time
                except (ValueError, TypeError) as e:
                    # Gracefully skipping bad CSV row

                    print(f"\n⚠️ Skipping ticket {ticket_id}: invalid date format ({e})")
                    continue

        # Calculating MTTR
        if closed_counter:
            avg_time = total_work_time / closed_counter
            average_resolution_time = format_timedelta(avg_time)
        else:
            average_resolution_time = "N/A"

        # Returning General Report
        if not agent_filter:

            return{
                "total_tickets": ticket_count,
                "tickets_per_agent": tickets_per_agent,
                "tickets_per_status": tickets_per_status,
                "tickets_per_priority": tickets_per_priority,
                "average_resolution_time": average_resolution_time
            }
        
        # Returning Agent-specific Report
        else:
            if agent_filter in tickets_per_agent:
                return {
                    "agent": agent_filter,
                    "ticket count": tickets_per_agent[agent_filter],
                    "average resolution time": average_resolution_time
                    }
            else:
                return {"error": f'There is either no Agent {agent_filter}, '
                      'or no tickets were assigned to that agent.'}


def main():

    # Creating the Parser
    parser = argparse.ArgumentParser(
        description="Allows the user to choose a source file"
    )

    # Adding required Arguments
    parser.add_argument(
        "source",
        nargs="?",
        default="tickets.csv",
        help="Source log file (default: tickets.csv)"
    )

    # Adding optional Arguments
    parser.add_argument(
        "-a", "--agent",
        default=None,
        help="Allows you to filter by Agent name"
        )
    
    # Parsing Arguments
    args = parser.parse_args()

    # Calling the function
    try:
        report = ticket_report(args.source,args.agent)
        # Unknown Agent filter
        if "error" in report:
            print(report["error"])

        # Known Agent filter
        elif args.agent:
            print(f"Agent: {report['agent']}")
            print(f"Number of assigned tickets: {report['ticket count']}")
            print(f"Mean Time to Resolution: {report['average resolution time']}")

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

if __name__ == "__main__":
    main()