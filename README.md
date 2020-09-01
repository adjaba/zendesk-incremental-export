Python command line tool to view Zendesk tickets created between two times (inclusive) using the incremental export API. 

To run: 
```python zendesk.py <username> <API key> <Zendesk subdomain>```

By default, it launches a website that shows tickets created from Dec 15, 2019 12:00:00 UTC to Jan 10, 2020 12:00:00 UTC.

Files:
- zendesk.py - Python script and Flask backend
- templates/index.html - HTML/CSS/Bootstrap frontend
- populate.py - To populate the Zendesk subdomain with data for testing
