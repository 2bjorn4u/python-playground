from datetime import datetime
tickets_datetimed = []
tickets = [
    {
        'Ticket ID': '14072043', 
        'Created at': '2025-12-01 08:22:37', 
        'Closed at': '2025-12-01 10:31:20'
        },
    {
        'Ticket ID': '14073945', 
        'Created at': '2025-11-30 14:05:01', 
        'Closed at': '2025-12-01 09:04:55'
        }
]

for ticket in tickets:
    created_at = ticket['Created at']
    closed_at = ticket['Closed at']
    dt_created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
    dt_closed_at = datetime.strptime(closed_at, '%Y-%m-%d %H:%M:%S')
    worked_time = dt_closed_at - dt_created_at
    print(worked_time)
    print(worked_time / len(tickets))
    ticket['Created at'] = dt_created_at
    ticket['Closed at'] = dt_closed_at

print(tickets)