# Games API

Base path: `/games`

All endpoints are read-only and return JSON. Player references in all responses are integer IDs.

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/games/` | List all games with optional filters |
| GET | `/games/{game_id}` | Full play-by-play event timeline for a game |
| GET | `/games/{game_id}/summary` | Game summary with shots, goals, and penalties by period |

---

## GET `/games/`

Returns a list of games. All query parameters are optional; omitting them returns all games.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `team` | integer | No | Filter to games where this team ID was the home or visiting team. |
| `league_year` | string | No | Filter by season year as an eight character string, e.g. `"20252026"`. The inaugral season is `"00002024"`. |
| `season_type` | integer | No | Filter by season type ID (references the `season_descriptions` table). |

### Response

Returns an array of game objects.

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique game identifier. |
| `date` | string | Game date in `YYYY-MM-DD` format. |
| `home_team` | string | Full name of the home team. |
| `visiting_team` | string | Full name of the visiting team. |
| `season` | string | Season name (e.g. `"2025-2026 Regular Season"`). |
| `venue` | string | Arena name. |
| `start_time` | string | Game start time. |
| `end_time` | string | Game end time. |
| `duration` | string | Total game duration. |

### Example

```
GET /games/?team=6&league_year=20252026&season_type=1
```

```json
[
  {
    "id": 210,
    "date": "2025-11-21",
    "home_team": "Minnesota Frost",
    "visiting_team": "Toronto Sceptres",
    "season": "2025-26 Regular Season",
    "venue": "Xcel Energy Center",
    "start_time": "06:00:21",
    "end_time": "08:00:38",
    "duration": "02:00:17"
  },
]
```

---

## GET `/games/{game_id}`

Returns the full play-by-play timeline for a single game, sorted chronologically by period and time. Optionally filter events by type and/or player.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `game_id` | integer | Yes | The ID of the game to retrieve. |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `event_type` | string | No | Return only events of this type. See [Event Types](#event-types) below. |
| `player_id` | integer | No | Return only events in which this player was involved. |

When both `event_type` and `player_id` are supplied, both filters are applied (AND logic). If no events match, an error object is returned:

```json
{ "error": "no events found matching the given filters." }
```

### Response

When no filters are applied, the response is a top-level object:

| Field | Type | Description |
|-------|------|-------------|
| `game_data` | object | Core game metadata (see below). |
| `events` | array | Chronologically sorted list of event objects. |
| `shootout` | object | Present only when the game went to a shootout. Contains a `rounds` map. |

When filters are applied, the response is an array of matching event objects directly (no `game_data` wrapper).

#### `game_data` fields

| Field | Type | Description |
|-------|------|-------------|
| `game_id` | integer | Unique game identifier. |
| `date` | string | Game date. |
| `home_team` | string | Home team full name. |
| `home_team_goals` | integer | Goals scored by the home team. |
| `visiting_team` | string | Visiting team full name. |
| `visiting_team_goals` | integer | Goals scored by the visiting team. |
| `win_type` | string | How the game was decided: `"REG"`, `"OT"`, or `"SO"`. |
| `season` | string | Season name. |
| `venue` | string | Arena name. |
| `attendance` | integer | Announced attendance. |

---

### Event Types

| Event Type | Description |
|------------|-------------|
| `goal` | A goal scored, including scorer, assists, plus/minus players, strength flags, and coordinates. |
| `shot` | A shot on goal with shooter, goalie, shot type, quality rating, and coordinates. |
| `blocked_shot` | A shot that was blocked, with shooter, blocker, and goalie IDs. |
| `hit` | A body check, recording both the hitter and the player hit. |
| `penalty` | A penalty call with infraction type, duration, and who took/served it. |
| `penalty_shot` | A penalty shot attempt, recording shooter, goalie, and whether it was a goal. |
| `faceoff` | A faceoff, recording home and visiting player and which team won. |
| `goalie_change` | A goalie substitution, noting whether the goalie is entering or leaving. |

> **Note:** Shootout attempts do not appear in the `events` array. They are returned separately in the top-level `shootout` object.

---

### Event Object Structure

Every event in the `events` array shares a common envelope:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Event type identifier (see [Event Types](#event-types)). |
| `id` | integer | Unique event ID. |
| `period` | string | Period identifier: `"1"`, `"2"`, `"3"`, and subsequent OT periods continuing this pattern. |
| `time` | string | Elapsed time within the period (`MM:SS`). |
| `data` | object | Event-specific payload (see below). |

---

### Event `data` Schemas

#### `goal`

| Field | Type | Description |
|-------|------|-------------|
| `scorer` | integer | Player ID of the goal scorer. |
| `assists` | array | Array of `{ "player": int, "type": "primary"\|"secondary" }`. |
| `plus` | array | Array of `{ "player": int }` for players earning a plus. |
| `minus` | array | Array of `{ "player": int }` for players earning a minus. |
| `strength.powerplay` | boolean | `true` if a power-play goal. |
| `strength.shorthanded` | boolean | `true` if a shorthanded goal. |
| `strength.emptynet` | boolean | `true` if scored into an empty net. |
| `strength.insurance` | boolean | `true` if this is an insurance goal. |
| `strength.gamewinning` | boolean | `true` if this is the game-winning goal. |
| `coordinates.x_location` | integer | X coordinate on the ice surface. |
| `coordinates.y_location` | integer | Y coordinate on the ice surface. |

#### `shot`

| Field | Type | Description |
|-------|------|-------------|
| `shooter` | integer | Player ID of the shooter. |
| `goalie` | integer | Player ID of the goalie who faced the shot. |
| `goal` | boolean | `true` if the shot resulted in a goal. |
| `type` | string | Shot type (e.g. wrist, slap, snap). |
| `quality` | string | Scoring chance quality rating. |
| `coordinates.x_location` | integer | X coordinate of the shot. |
| `coordinates.y_location` | integer | Y coordinate of the shot. |

#### `blocked_shot`

| Field | Type | Description |
|-------|------|-------------|
| `shooter` | integer | Player ID of the shooter. |
| `blocker` | integer | Player ID of the player who blocked the shot. |
| `goalie` | integer | Player ID of the goalie. |
| `type` | string | Shot type. |
| `quality` | string | Scoring chance quality rating. |
| `coordinates.x_location` | integer | X coordinate. |
| `coordinates.y_location` | integer | Y coordinate. |

#### `hit`

| Field | Type | Description |
|-------|------|-------------|
| `player` | integer | Player ID of the player delivering the hit. |
| `on_player` | integer \| null | Player ID of the player receiving the hit, or `null` if not recorded. |
| `coordinates.x_location` | integer | X coordinate. |
| `coordinates.y_location` | integer | Y coordinate. |

#### `penalty`

| Field | Type | Description |
|-------|------|-------------|
| `taken_by` | integer | Player ID of the player who committed the infraction. |
| `served_by` | integer | Player ID of the player who served the penalty (may differ in situations such as game misconducts). |
| `length` | integer | Penalty duration in minutes. |
| `type` | string | Penalty description/infraction type. |
| `bench` | boolean | `true` if this is a bench penalty. |
| `powerplay` | boolean | `true` if the penalty resulted in a power play. |

#### `penalty_shot`

| Field | Type | Description |
|-------|------|-------------|
| `shooter` | integer | Player ID of the shooter. |
| `goalie` | integer | Player ID of the goalie. |
| `is_goal` | boolean | `true` if the penalty shot was converted into a goal. |

#### `faceoff`

| Field | Type | Description |
|-------|------|-------------|
| `home_player` | integer | Player ID of the home team's faceoff participant. |
| `visiting_player` | integer | Player ID of the visiting team's faceoff participant. |
| `home_win` | boolean | `true` if the home team won the faceoff. |
| `coordinates.x_location` | integer | X coordinate of the faceoff dot. |
| `coordinates.y_location` | integer | Y coordinate of the faceoff dot. |

#### `goalie_change`

| Field | Type | Description |
|-------|------|-------------|
| `goalie` | integer | Player ID of the goalie. |
| `entering` | boolean | `true` if the goalie is entering the game; `0` if leaving. |

---

### Shootout Object

When present, the top-level `shootout` key contains a `rounds` object keyed by round number (`1`, `2`, `3`, …). Each round is an array of attempt objects:

| Field | Type | Description |
|-------|------|-------------|
| `shooter` | integer | Player ID of the shooter. |
| `goalie` | integer | Player ID of the goalie. |
| `is_goal` | boolean | `true` if the attempt was successful. |
| `is_gamewinninggoal` | boolean | `true` if this attempt decided the shootout. |

---

### Examples

```
GET /games/299
GET /games/299?event_type=goal
GET /games/299?player_id=36
GET /games/299?event_type=shot&player_id=36
```

**Full game response:**
```json
{
  "game_data": {
    "game_id": 299,
    "date": "2026-03-27",
    "home_team": "Toronto Sceptres",
    "home_team_goals": 0,
    "visiting_team": "Boston Fleet",
    "visiting_team_goals": 4,
    "win_type": "REG",
    "season": "2025-26 Regular Season",
    "venue": "Coca-Cola Coliseum",
    "attendance": 8636
  },
  "events": [
	{
    "type": "goal",
    "id": 1472,
    "period": "2",
    "time": "14:32",
    "data": {
      "scorer": 36,
      "assists": [
        {
          "player": 15,
          "type": "primary"
        },
        {
          "player": 182,
          "type": "secondary"
        }
      ],
      "plus": [
        {
          "player": 8
        },
        {
          "player": 15
        },
        {
          "player": 36
        },
        {
          "player": 185
        },
        {
          "player": 255
        }
      ],
      "minus": [
        {
          "player": 26
        },
        {
          "player": 56
        },
        {
          "player": 63
        },
        {
          "player": 200
        },
        {
          "player": 313
        }
      ],
      "strength": {
        "powerplay": false,
        "shorthanded": false,
        "emptynet": false,
        "insurance": false,
        "gamewinning": false
      },
      "coordinates": {
        "x_location": 535,
        "y_location": 174
      }
    }
  }
  ]
}
```

---

## GET `/games/{game_id}/summary`

Returns a structured summary of the game including period-by-period breakdowns of shots, goals, and penalties. Player-to-team assignment is resolved using both current rosters and historical roster data at the time of the game.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `game_id` | integer | Yes | The ID of the game to summarize. |

### Response

| Field | Type | Description |
|-------|------|-------------|
| `game_id` | integer | Unique game identifier. |
| `date` | string | Game date. |
| `home_team` | string | Home team full name. |
| `home_team_goals` | integer | Goals scored by the home team. |
| `visiting_team` | string | Visiting team full name. |
| `visiting_team_goals` | integer | Goals scored by the visiting team. |
| `win_type` | string | How the game was decided: `"REG"`, `"OT"`, or `"SO"`. |
| `season` | string | Season name. |
| `venue` | string | Arena name. |
| `start_time` | string | Game start time. |
| `end_time` | string | Game end time. |
| `duration` | string | Total game duration. |
| `attendance` | integer | Announced attendance. |
| `data.shots` | object | Shot counts by period and total, split by home/visiting. |
| `data.goals` | object | Goal details grouped by period. |
| `data.penalties` | object | Penalty details grouped by period. |

#### `data.shots`

An object keyed by period (`"1"`, `"2"`, `"3"`, `"4"`, etc.) and `"total"`. Each value contains:

| Field | Type | Description |
|-------|------|-------------|
| `home` | integer | Shot count for the home team. |
| `visiting` | integer | Shot count for the visiting team. |

#### `data.goals`

An object keyed by period. Each value is an array of goal objects:

| Field | Type | Description |
|-------|------|-------------|
| `goal.time` | string | Time of the goal within the period (`MM:SS`). |
| `goal.scorer` | integer | Player ID of the goal scorer. |
| `goal.assists` | array | Array of `{ "player": int, "type": "primary"\|"secondary" }`, sorted by assist type. |
| `goal.strength.powerplay` | boolean | `true` if a power-play goal. |
| `goal.strength.shorthanded` | boolean | `true` if a shorthanded goal. |
| `goal.strength.emptynet` | boolean | `true` if scored into an empty net. |
| `goal.strength.insurance` | boolean | `true` if this is an insurance goal. |
| `goal.strength.gamewinning` | boolean | `true` if this is the game-winning goal. |

#### `data.penalties`

An object keyed by period. Each value is an array of penalty objects:

| Field | Type | Description |
|-------|------|-------------|
| `penalty.time` | string | Time of the penalty within the period (`MM:SS`). |
| `penalty.taken_by` | integer | Player ID of the penalized player. |
| `penalty.served_by` | integer | Player ID of the player who served the penalty. |
| `penalty.description` | string | Penalty infraction type. |
| `penalty.length` | integer | Penalty duration in minutes. |
| `penalty.powerplay` | boolean | `true` if the penalty resulted in a power play. |
| `penalty.bench` | boolean | `true` if this is a bench minor. |

### Example

```
GET /games/4821/summary
```

```json
{
  "game_id": 299,
  "date": "2026-03-27",
  "home_team": "Toronto Sceptres",
  "home_team_goals": 0,
  "visiting_team": "Boston Fleet",
  "visiting_team_goals": 4,
  "win_type": "REG",
  "season": "2025-26 Regular Season",
  "venue": "Coca-Cola Coliseum",
  "start_time": "06:07:00",
  "end_time": "08:25:00",
  "duration": "02:18:00",
  "attendance": 8636,
  "data": {
    "shots": {
      "1": {
        "home": 4,
        "visiting": 10
      },
      "2": {
        "home": 9,
        "visiting": 7
      },
      "3": {
        "home": 5,
        "visiting": 6
      },
      "total": {
        "home": 18,
        "visiting": 23
      }
    },
    "goals": {
      "1": {
        "home": 0,
        "visiting": 1
      },
      "2": {
        "home": 0,
        "visiting": 2
      },
      "3": {
        "home": 0,
        "visiting": 1
      },
      "total": {
        "home": 0,
        "visiting": 4
      }
    },
    "penalties": {
      "1": {
        "home": 1,
        "visiting": 1
      },
      "2": {
        "home": 0,
        "visiting": 0
      },
      "3": {
        "home": 2,
        "visiting": 1
      },
      "total": {
        "home": 3,
        "visiting": 2
      }
    }
  }
}
```

---

## Conventions

- **Player IDs** — All player references are integer IDs. Resolve names via the players endpoint.
- **Period values** — Periods are strings: `"1"`, `"2"`, `"3"` for regulation, `"4"` for overtime, increasing with each subsequent OT period in the postseason.
- **Boolean fields** — Boolean fields serialize as `true`/`false`.
- **`win_type`** — `"REG"` = regulation, `"OT"` = overtime, `"SO"` = shootout.
- **Shootout events** — Shootout attempts are excluded from the `events` timeline and returned in a separate top-level `shootout` object on the `/games/{game_id}` response.
- **Roster resolution** — The `/summary` endpoint resolves rosters using both `current_players` and `player_history`, so player-to-team assignment is accurate for previous games.

---
 
## GET `/games/{game_id}/stats/skater`
 
Returns per-player skater statistics for a single game. Goalies are excluded. Results are split by home and visiting team, and can optionally be filtered to a single team.
 
Player-to-team assignment is resolved using both current rosters and historical roster data at the time of the game.
 
### Path Parameters
 
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `game_id` | integer | Yes | The ID of the game to retrieve skater stats for. |
 
### Query Parameters
 
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `team` | integer | No | Filter results to a single team by team ID. When omitted, stats for both teams are returned. |
 
### Response
 
The shape of the response depends on whether a `team` filter is applied.
 
#### Without a `team` filter
 
| Field | Type | Description |
|-------|------|-------------|
| `home` | integer | Team ID of the home team. |
| `visiting` | integer | Team ID of the visiting team. |
| `stats.home` | object | Skater stats for the home team, keyed by player ID. |
| `stats.visiting` | object | Skater stats for the visiting team, keyed by player ID. |
 
#### With a `team` filter
 
When `team` matches the home team:
 
| Field | Type | Description |
|-------|------|-------------|
| `home` | integer | Team ID of the requested team. |
| `stats` | object | Skater stats for that team, keyed by player ID. |
 
When `team` matches the visiting team:
 
| Field | Type | Description |
|-------|------|-------------|
| `visiting` | integer | Team ID of the requested team. |
| `stats` | object | Skater stats for that team, keyed by player ID. |
 
---
 
### Player Stat Object
 
Each player ID key maps to an array containing a single stat object with the following fields:
 
| Field | Type | Description |
|-------|------|-------------|
| `toi` | string \| array | Time on ice in `HH:MM:SS` format, or an empty array `[]` if no TOI was recorded. |
| `shots` | integer | Shots on goal taken. |
| `goals` | integer | Goals scored. |
| `assists` | integer | Assists recorded (primary and secondary combined). |
| `penalties.number` | integer | Number of penalties taken. |
| `penalties.pim` | integer | Total penalty minutes. |
| `penalty_shots.taken` | integer | Number of penalty shots taken. |
| `penalty_shots.goal` | integer | Number of penalty shots converted into goals. |
| `hits` | integer | Hits delivered. |
| `blocked_shots` | integer | Shots blocked. |
| `faceoffs.taken` | integer | Faceoffs taken. |
| `faceoffs.won` | integer | Faceoffs won. |
| `shootout_attempts.attempt` | integer | Shootout attempts taken. |
| `shootout_attempts.goal` | integer | Shootout attempts converted into goals. |
 
> **Note on faceoffs:** When no `team` filter is supplied, each faceoff is counted for both participants (home and visiting), and the winner is determined per side. When a `team` filter is applied, only that team's players have their faceoff stats populated; the opposing players are not included in the response.
 
> **Note on `toi`:** Players who dressed but did not record any ice time will have `toi` returned as an empty array `[]` rather than a time string.
 
---
 
### Examples
 
```
GET /games/299/stats/skater
GET /games/299/stats/skater?team=6
```
 
**Response without a team filter:**
 
```json
{
  "home": 6,
  "visiting": 1,
  "stats": {
    "home": {
      "44": [
        {
          "toi": "00:20:52",
          "shots": 2,
          "goals": 0,
          "assists": 0,
          "penalties": {
            "number": 0,
            "pim": 0
          },
          "penalty_shots": {
            "taken": 0,
            "goal": 0
          },
          "hits": 1,
          "blocked_shots": 1,
          "faceoffs": {
            "taken": 0,
            "won": 0
          },
          "shootout_attempts": {
            "attempt": 0,
            "goal": 0
          }
        }
      ],
      "73": [
        {
          "toi": "00:19:18",
          "shots": 2,
          "goals": 0,
          "assists": 0,
          "penalties": {
            "number": 0,
            "pim": 0
          },
          "penalty_shots": {
            "taken": 0,
            "goal": 0
          },
          "hits": 0,
          "blocked_shots": 1,
          "faceoffs": {
            "taken": 20,
            "won": 10
          },
          "shootout_attempts": {
            "attempt": 0,
            "goal": 0
          }
        }
      ]
    },
    "visiting": {
      "97": [
        {
          "toi": "00:16:31",
          "shots": 4,
          "goals": 2,
          "assists": 0,
          "penalties": {
            "number": 0,
            "pim": 0
          },
          "penalty_shots": {
            "taken": 0,
            "goal": 0
          },
          "hits": 1,
          "blocked_shots": 0,
          "faceoffs": {
            "taken": 11,
            "won": 4
          },
          "shootout_attempts": {
            "attempt": 0,
            "goal": 0
          }
        }
      ]
    }
  }
}
```
 
**Response with a team filter (home team):**
 
```json
{
  "home": 6,
  "stats": {
    "44": [
      {
        "toi": "00:20:52",
        "shots": 2,
        "goals": 0,
        "assists": 0,
        "penalties": {
          "number": 0,
          "pim": 0
        },
        "penalty_shots": {
          "taken": 0,
          "goal": 0
        },
        "hits": 1,
        "blocked_shots": 1,
        "faceoffs": {
          "taken": 0,
          "won": 0
        },
        "shootout_attempts": {
          "attempt": 0,
          "goal": 0
        }
      }
    ]
  }
}
```
 
---
 
## Conventions
 
- **Player IDs** — All player keys are integer IDs serialized as strings (JSON object keys). Resolve names via the players endpoint.
- **Goalies** — Goalies are excluded from this endpoint regardless of the `team` filter. See the goalie stats endpoint for goalie-specific data.
- **Roster resolution** — Player-to-team assignment uses both `current_players` and `player_history`, so results are accurate for historical games.
- **`toi` format** — Time on ice is returned as `HH:MM:SS`. Players with no recorded ice time return `[]` instead.

