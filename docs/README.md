# PWHL API DOCUMENTATION
Welcome to my PWHL API! I created this out of data I scraped directly from the PWHL website. I found it very difficult to navigate and parse through their data, so I decided I wanted to make my own API to hopefully provide easier data access to everyone else.

This API provides detailed data about games, players,teams, and in-game events. The end goal is to provide an access point for basically anything you can hope for. If you have any suggestions for future additions, feel free to email me at pwhl-project@gmail.com and I will consider it!

---

## DOCUMENTATION STRUCTURE
- [Games](./games/README.md)
- [Players](./players/README.md)
- [Teams](./teams/README.md)
- [Standings](./standings/README.md)

---

## BASEURL
To be revealed once ready

---

## OVERVIEW

### GAMES
- Retrieve a detailed timeline of game data, with the ability to filter on a game's events to access any specific event such as goals.
- Retrieve a list of all games, with the ability to filter by season, year, teams, or any combination thereof. 

### PLAYERS
- Retrive a player's profile, with the ability to filter by season or year.
- Retrieve a list of all events belonging to a player such as goals, assists, or faceoffs. Events such as hits will be able to be filtered by if the player was hit or the one hitting. 

### TEAMS
- Retrieve a team's roster for any given season.
- Retrieve a team's stats for any given season.

### STANDINGS
- Retrieve the most up-to-date standings for the leauge.
- Retrieve previous year standings.

---

## DESIGN PHILOSOPHY
- RESTful structure
- Rich end-level data
- Optimized for visualization
- Delivery of as much data as possible in an intuitive format

---

# FOLDER STRUCTURE
```
docs/
│
├── README.md
├── games/
│   └── README.md
│   └── known_issues.md
├── players/
│   └── README.md
│   └── known_issues.md
├── teams/
│   └── README.md
│   └── known_issues.md
```
	
