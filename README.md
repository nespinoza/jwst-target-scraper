# JWST Cycle 1 Target Scraper
-----------------------------

Are you wondering what exoplanet targets will be observed in different JWST Cycles? This code and list can help. 

Author: Nestor Espinoza (nespinoza@stsci.edu)

## What does this code do?

The `create_targets.py` python code simply does some data scraping from a given webapge of GO results at STScI's webpage ([e.g., the Cycle 1 webpage](https://www.stsci.edu/jwst/science-execution/approved-programs/cycle-1-go)) and extracts the names of the targets _as inputted by the GO proposers_ on the accepted GO proposals. Only the first table (i.e., the "Exoplanets and Disks") is currently exported by the code, but with simple modifications this can provide the same list for the other tables.

Results of all the exoplanets & disk targets are saved to a csv file.

## Limitations

- As stated above, the code simply reads the target names inputted by GO proposers. This poses two issues: (a) it is not optimal for doing straightforward automatic target searches, as proposers might have used the target names suggested by APT and not their common target names for the exoplanet community, (b) proposers might have chosen to write placehoder names for targets instead of "real" target names. An easy fix for this would be to read the public PDF files of the proposals instead of the web-formatted program information --- solutions to this are welcome!

- Whenever there is TA acquisitions on offset targets, the names of the target and the TA object are appended together. For instance, [proposal ID 2159](https://www.stsci.edu/jwst/science-execution/program-information?id=2159) lists both K2-141 and 23233859-0110575 as the target --- the former being the science target, the latter the TA target. The web-scrapping tool being used in the code (`BeautifulSoup`) simply merges those two, so the final target name on the `csv` file reads "K2-14123233859-0110575" (solutions to this are welcome!).

## Acknowledgements

I would like to thank Sean Lockwood at STScI for writing the awesome 10 lines of code that do the web-scraping with `BeautifulSoup`.
