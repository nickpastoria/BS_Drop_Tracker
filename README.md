# BS_Drop_Tracker
A tool for tracking drops from combat kills in Brighter Shores in order to perform statistical analysis of the drops
- Note: This program (at least at the moment) does not perform any statistical analysis and is still in **very early development**
  - As a result I'm going to try to make logs you take now work later on when more features are added, but beware old logs may become obsolete when a database is set up.

# Requirements
- This application requires python 3 to run.
  - Python can be downloaded from here: https://www.python.org/downloads/
 
# Inteded Use
- Clone/download the repo from github to your device
- Launch **app.pyw**
- Load your existing csv, or start from scratch with an empty project
- The application keeps track of entries you type into each dropdown category.
  - This means you only need to write new items into the dropdown menu once. Once the kill is logged it remembers it.
  - It also will fill the dropdown menus on load

## Saving
- This application does not have autosave yet. So please remember to export your kills after logging to a csv file.
  
## Enemy Drops
- When an enemy doesn't drop anything the item category will default to "None"
- If the enemy has an item drop with an amount I simply write "Drop x(amount"
  - So for the Toad drop I would write **Squishy Toad's Eye x4** since it always drops in sets of four
