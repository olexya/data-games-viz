# Steam Stat
An application to understand statistique of [Steam](https://store.steampowered.com)

The application using [dbt](https://www.getdbt.com), [Evidence](https://evidence.dev) and [PostgreSQL](postgresql.org/)
## Installation
command git
architecture des composants
Using Docker Desktop ton installer this app.
```sh
42sh> docker-compose up -d
```
## Viewing
Open in browser [localhost:3000](localhost:3000)
AND enjoy !
## ContentÍ
This app contains one page, the main page.

The first element is filter Platforms and Years. He impact all element of the pages except the second line.

The second line contains different general data value.

The next element is a tab panel for three data :
- Games

Element 1 : Number games with filters

Element 2 : Top 3 more rated games, the filters platforms and year impact this

Element 3 : Number and average price of games by year, he is impact by filter platforms
- Categories

Element 1 : Number categories with filters

Element 2 : Top 3 most games categories, the filters platforms and year impact this

Element 3 : Number of categories created by year, he is impact by filter platforms
- Platforms

Element 1 : Number platforms

Element 2 : This graph show link between categories Single-Player and Multi-player and all of platforms.
The last element is an table to view more info for a specific games. The search table is impact by filter et and search. And on clic on an element a new tab open on the left of search table et show detail of the games.
## Credit
The application using [dbt](https://www.getdbt.com), [Evidence](https://evidence.dev) and [PostgreSQL](postgresql.org/)
