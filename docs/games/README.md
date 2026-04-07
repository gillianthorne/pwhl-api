# GAMES API

## ENDPOINTS
- [`GET /games`](#get-games)
- [`GET /games/{game_id}`](#get-gamesgame_id)
## GET /games
Retrieve a list of games with optional filters.

### QUERY PARAMETERS
|Name   |Type   |Description   |
|-------|-------|--------------|
|season |string |Eight character string representing the season year. i.e. 00002024 or 20252026.|
|season_type |int |1=preseason, 2=regular, 3=playoffs|
|team |int |The integer value representing each team.|

### EXAMPLES
All 2025 playoff games:

```
GET /games?season=20242025&season_type=3
```

All games played in the 2024 season, including both preseason and playoffs

```
GET /games?season=00002024
```

---

## GET /games/{game_id}

Retrieve full details for a single game.

### RESPONSE 

```json
{
	"game_id": int,
	"date": date,
	"timeline": list of event objects
}
```

## EVENT STRUCTURE
All events follow this format except shootouts:

```json
{
	"type": str,
	"id": int,
	"period": str,
	"time": time,
	"data": {}
}
```

## GOALIE_CHANGE

```json
"data": {
	"goalie": int,
	"entering": bool
}

## FACEOFF

```json
"data": {
	"home_player": int,
	"visiting_player": int,
	"home_win": bool,
	"coordinates": {
		"x_location": int,
		"y_location": int
	}
}
```

## GOAL

```json
"data": {
	"scorer": str,
	"assists": [
		{
			"player": int,
			"type": "primary" or "secondary"
		}
	],
	"plus": [
		{
			"player": int,
		}
	],
	"minus": [
		{
			"player": int,
		}
	],
	"strength": {
		"powerplay": bool,
		"shorthanded": bool,
		"emptynet": bool,
		"insurance": bool,
		"gamewinning": bool
	},
	"coordinates": {
		"x_location": int,
		"y_location": int
	}
}
```

## SHOT

```json
"data": {
	"shooter": int,
	"goalie": int,
	"goal": bool,
	"type": str,
	"quality": str,
	"coordinates": {
		"x_location": int,
		"y_location": int
	}
}
```

## BLOCKED_SHOT

```json
"data": {
	"shooter": int,
	"blocker": int,
	"goalie": int,
	"type": str,
	"quality": str,
	"coordinates": {
		"x_location": int,
		"y_location": int
	}
}
```	

## HIT

```json
"data": {
	"player":  int,
	"on_player": int,
	"coordinates": {
		"x_location": int,
		"y_location": int
	}
}
```

## PENALTY
Note: powerplay is broken on some games early on because the data I scraped it from was wonky. If you want to check if it is a powerplay, please compare times to the previous penalty. 

```json
"data" {
	"taken_by": int,
	"served_by": int,
	"length": int,
	"type": str,
	"bench": bool,
	"powerplay": bool
}
```

## PENALTY_SHOT

```json
"data" {
	"shooter": int,
	"goalie": int,
	"goal": bool
}
```

## SHOOTOUT

```json
{
	"type": "shootout",
	"rounds": {
		round (int): [
			{
				"shooter": int,
				"goalie": int,
				"goal": bool,
				"gamewinninggoal": bool
			}
		]
	}
}
	
