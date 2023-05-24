import numpy as np
import pandas as pd
import requests

from bs4 import BeautifulSoup

# Get page data:
r = requests.get("https://www.stsci.edu/jwst/science-execution/approved-programs/general-observers/cycle-2-go")

# Soup-ify the webpage data:
soup = BeautifulSoup(r.content, features="lxml")

# Extract tables for all proposals on the Exoplanets & Disks category (scraping of tables courtesy of Sean Lockwood at STScI; 
# modified to only get the first table --- the one for Exoplanets and Disks):
tables = []
for table in soup.findAll("table"):
    if table.findParent("table") is None:
        tables.append(pd.read_html(str(table))[0])
    break
df = pd.concat(tables)

# Now, using this table, scrape targets using the program information. We save all the data in a dictionary; for each target, we save all the 
# observations for it:
target_info = {}
for program_id in df['ID']:

    print('Scraping '+str(program_id)+'...')
    r_pid = requests.get("https://www.stsci.edu/cgi-bin/get-visit-status?id="+str(program_id)+"&markupFormat=html&observatory=JWST&pi=1")
    pid_soup = BeautifulSoup(r_pid.content, features="lxml")

    # Extract target info if availalbe (theory proposal will fail, so skip them):
    try:
        tables = []
        for table in pid_soup.findAll("table"):
            if table.findParent("table") is None:
                tables.append(pd.read_html(str(table))[0])
        pid_df = pd.concat(tables)

        # Save also info from the current PID:
        current_pid = df['ID'] == program_id
        program_title = df[current_pid]['Program Title'].values[0]
        program_pi = df[current_pid]['PI & Co-PIs'].values[0]

        # Iterate through targets; save info to dictionary:
        for i in range(1, len(pid_df)):

            # Extract information for current program/targets:
            target_name, instrument, hours = pid_df[3][i], pid_df[4][i], pid_df[5][i] 

            # Create dict for target if not create already:
            if target_name not in target_info.keys():
                target_info[target_name] = {}
                target_info[target_name]['Templates'] = np.array([])
                target_info[target_name]['Hours'] = np.array([])
                target_info[target_name]['PIDs'] = np.array([])
                target_info[target_name]['PIs'] = np.array([])
                target_info[target_name]['Titles'] = np.array([])

            # Save info for target:
            target_info[target_name]['Templates'] = np.append(target_info[target_name]['Templates'], instrument)
            target_info[target_name]['Hours'] = np.append(target_info[target_name]['Hours'], hours)
            target_info[target_name]['PIDs'] = np.append(target_info[target_name]['PIDs'], program_id)
            target_info[target_name]['Titles'] = np.append(target_info[target_name]['Titles'], program_title)
            target_info[target_name]['PIs'] = np.append(target_info[target_name]['PIs'], program_pi)
    except:
        print('Program ID',program_id,'target extraction failed. Probably theory proposal.')

# Now print all the info in comma-separated machine readable form:
fout = open('targets_cycle2.csv', 'w')
# Write headers out:
fout.write('Target Name, Instrument Mode, Hours on Mode, Program ID, Program PIs, Program Title\n')
for target in target_info.keys():
    all_data = target_info[target]
    for i in range(len(all_data['Templates'])):
        print(target)
        out_string = target+','
        for info in ['Templates', 'Hours', 'PIDs', 'PIs', 'Titles']:
            # replace commas by spaces in saved strings:
            out_string += str(all_data[info][i]).replace(',',' ')+','
        out_string = out_string[:-1]
        out_string += '\n'
        fout.write(out_string)
fout.close()
