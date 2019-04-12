# election_results
Web Scraper for http://www.electionguide.org/elections/

## Workflow

The workflow of the [script](elections.py) is simple and straightforward.

1. Get's the datetime of the execution
2. Check if there is a file with the same datetime execution
3. If not create the file
4. With request module we "open" the url and get all the results at once
5. We get the json data
6. Using argparse module we setting the parameters of what results we want
7. We save to a csv file
