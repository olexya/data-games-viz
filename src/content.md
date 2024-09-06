# Data Games Viz
An application to understand statistics of [Steam](https://store.steampowered.com)

# Organisation

The main page consists of one screen with several interactive elements.

## Filter Panels
The first section contains two filter panels:
* Platforms: Select from a list of available platforms (impacting all elements except the second line)
* Years: Choose from a range of years to view statistics for (also impacting all elements except the second line)

## General Data
The second line displays general data values, which remain unchanged by the filter panels.

### Tab Panel
The main content area is divided into three tabs:
#### Games

* Element 1: Number of games with filters (platforms and years)
* Element 2: Top 3 most rated games, filtered by platforms and year
* Element 3: Number and average price of games by year, filtered by platform

#### Categories

* Element 1: Number of categories with filters (platforms and years)
* Element 2: Top 3 most games in each category, filtered by platforms and year
* Element 3: Number of categories created by year, filtered by platform

#### Platforms

* Element 1: List of available platforms
* Element 2: Interactive graph showing relationships between Single-Player and Multi-player categories across all platforms

### Game Details Table
The table displays information about specific games. The search bar is impacted by the filter panels and allows for searching by game name, platform, or year.

On clicking an element in the table, a new tab opens on the left of the search bar, displaying detailed information about the selected game.

Let me know if this meets your requirements!