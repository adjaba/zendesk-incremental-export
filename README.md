Python command line tool to view Zendesk tickets created between two times (start inclusive, end exclusive) using the incremental export API, also generates results.json in the directory it is run. Tickets are sorted by increasing created_at time.

To run:
`python zendesk.py <email address> <API key> <Zendesk subdomain>`

By default, it launches a website that shows tickets created from Dec 15, 2019 12:00:00 UTC (inclusive) to Jan 10, 2020 12:00:00 UTC (exclusive).

Files:

- zendesk.py - Python script and Flask backend
- templates/index.html - HTML/CSS/Bootstrap frontend
- populate.py - To batch populate (up to 100 tickets) the Zendesk subdomain with data for testing
