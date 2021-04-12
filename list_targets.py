import pandas as pd
import requests

from bs4 import BeautifulSoup

# Get page data:
r = requests.get("https://www.stsci.edu/jwst/science-execution/approved-programs/cycle-1-go")

# Soup-ify the webpage data:
soup = BeautifulSoup(r.content)

# Extract tables for all proposals (scraping of tables courtesy of Sean Lockwood at STScI):
tables = []
for table in soup.findAll("table"):
    if table.findParent("table") is None:
        tables.append(pd.read_html(str(table))[0])
df = pd.concat(tables)

# Now, using this table, scrape targets using the program information webpage. Save target name and information in a dictionary:
pid_info = {}
for program_id in df['ID']:

    r_pid = requests.get("https://www.stsci.edu/cgi-bin/get-visit-status?id="+str(program_id)+"&markupFormat=html&observatory=JWST&pi=1")
    pid_soup = BeautifulSoup(r_pid.content)

    # Extract target info:
    tables = []
    for table in pid_soup.findAll("table"):
        if table.findParent("table") is None:
            tables.append(pd.read_html(str(table))[0])
    pid_df = pd.concat(tables)

    # Iterate through targets; save info to dictionary:
    pid_info[program_id] = {}
    for i in range(1, len(pid_df)):
        if pid_df[3][i] not in pid_info[program_id].keys():
            pid_info[program_id][pid_df[3][i]] = {}
            pid_info[program_id][pid_df[3][i]]['Templates'] = np.array([pid_df[4][i]])
            pid_info[program_id][pid_df[3][i]]['Hours'] = np.array([pid_df[5][i]])
        else:
            pid_info[program_id][pid_df[3][i]]['Template'] = np.append(pid_info[program_id][pid_df[3][i]]['Template'], pid_df[4][i])
            pid_info[program_id][pid_df[3][i]]['Hours'] = np.append(pid_info[program_id][pid_df[3][i]]['Hours'], pid_df[5][i])

# Now print all the info in comma-separated machine readable form:

