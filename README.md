In order for us to more concretely understand your approach to coding and implementation, please complete the following implementation exercise. Please implement your solution as an executable program which can be run from a Linux or Mac command line and is written in Python, Scala, or Java.

Please implement an executable program that extracts from a Zendesk account (via the Zendesk API) select fields (specified below) of all tickets created between 15-12-2019 12:00 PM UTC (inclusive) and 10-01-2020 12:00PM UTC (exclusive). I

In particular, assume that you are given a subdomain, email address, and API token for a Zendesk account, as specified here. Create a program that outputs to a file (in a format of your choice) the id, subject, description, and created_at fields of each ticket created within the aforementioned time range; the output tickets should be sorted by increasing created_at time. In order to extract tickets from Zendesk, use Zendesk's incremental export API, and ensure that your implementation respects all applicable Zendesk rate limits (assuming the Team Zendesk plan).

Bonus: Build a UI functionality. Feel free to use the framework of your choice.
