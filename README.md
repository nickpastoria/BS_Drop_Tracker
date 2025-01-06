# BS_Drop_Tracker
A tool for tracking drops from combat kills in Brighter Shores in order to perform statistical analysis of the drops
- Note: This program (at least at the moment) does not perform any statistical analysis and is still in **very early development**
  - As a result I'm going to try to make logs you take now work later on when more features are added, but beware old logs may become obsolete when a database is set up.

# Requirements
- This application requires python 3 to run.
  - Python can be downloaded from here: https://www.python.org/downloads/

# Included Files
- app.pyw
  - This is the main python application
- drop_file.csv
  - This is a my sample drop file I'm providing
  - Since there isn't a place to give credit for kills yet I ask that you use your own file after getting the feel for how the application works
 
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

# Contributing
- This section will cover contribution requirements for code contributors
- Code editing is very simple with python. In order to edit all you need to do is open app.pyw in any text editor of your choosing.
  
## Mission Statement
- The goal of this program is to make tracking kill data as easy as possible
- Thus the focus of the application is foremost on useability and file compatibility

## New Data Requirements
- New data columns can be added, but they need to be opt-in and the default option needs to be empty data. This is so that data sifting libraries like pandas can filter properly.
- Take tracking dropped weapon stats and level
  - Some people may want to track this. Others may not.
  - We want people tracking all the data (eg. weapon drop and ranks) along with the more detailed data to be able to be used in rarity calculation
  - However if someone chooses not to opt-in to the more fine grained data collection their data must be empty in those columns so it can easily be filtered out as "Null" or "Not Tracked" rathan than "None" which is a tracked nothing.
