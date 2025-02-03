import datetime

class Match:
    def __init__(self, team1_name, team2_name, games_per_set=6, total_sets=3):
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.games_per_set = games_per_set
        self.total_sets = total_sets  # e.g., 3 means best-of-3 (first to 2 sets)
        self.start_time = datetime.datetime.now()

        # Track sets won by each team.
        self.sets_won = {team1_name: 0, team2_name: 0}

        # Track games (in the current set) won by each team.
        self.games_won = {team1_name: 0, team2_name: 0}

        # Points (in the current game) for each team.
        self.points = {team1_name: 0, team2_name: 0}

        # Game mode can be:
        # "regular" – standard game with tennis point names,
        # "tiebreak" – when the set score reaches games_per_set-games_per_set,
        # "super_tiebreak" – used if sets are split (for best-of-3).
        self.game_mode = "regular"

        # Flag to indicate if the match is over.
        self.match_over = False
        self.winner = None

        # Record finished set scores as tuples (team1_games, team2_games)
        self.set_history = []

        # Record every point event.
        self.point_history = []

        # New: track who won the last closed game and set.
        self.last_game_winner = None
        self.last_set_winner = None

        # Flag so that a finished match is added only once to history.
        self.added_to_history = False

    def add_point(self, team):
        if self.match_over:
            return
        if team not in [self.team1_name, self.team2_name]:
            return

        if self.game_mode == "regular":
            self._add_point_regular(team)
        elif self.game_mode == "tiebreak":
            self._add_point_tiebreak(team)
        elif self.game_mode == "super_tiebreak":
            self._add_point_super_tiebreak(team)
        self._check_game_over()
        
        # Log the point event.
        event = {
            "time": self.get_match_time(),
            "scoring_team": team,
            "current_game_score": self.get_current_game_score(),
            "current_set_score": self.games_won.copy(),
            "current_match_score": self.sets_won.copy()
        }
        self.point_history.append(event)

    def _add_point_regular(self, team):
        self.points[team] += 1

    def _add_point_tiebreak(self, team):
        self.points[team] += 1

    def _add_point_super_tiebreak(self, team):
        self.points[team] += 1

    def _check_game_over(self):
        if self.game_mode == "regular":
            pts1 = self.points[self.team1_name]
            pts2 = self.points[self.team2_name]
            if (pts1 >= 4 or pts2 >= 4):
                if pts1 >= 4 and pts1 - pts2 >= 1 and pts2 < 3:
                    self._game_won(self.team1_name)
                elif pts2 >= 4 and pts2 - pts1 >= 1 and pts1 < 3:
                    self._game_won(self.team2_name)
                elif pts1 >= 3 and pts2 >= 3 and pts1 != pts2:
                    winner = self.team1_name if pts1 > pts2 else self.team2_name
                    self._game_won(winner)
        elif self.game_mode == "tiebreak":
            pts1 = self.points[self.team1_name]
            pts2 = self.points[self.team2_name]
            if (pts1 >= 7 or pts2 >= 7) and abs(pts1 - pts2) >= 2:
                winner = self.team1_name if pts1 > pts2 else self.team2_name
                self._game_won(winner, is_tiebreak=True)
        elif self.game_mode == "super_tiebreak":
            pts1 = self.points[self.team1_name]
            pts2 = self.points[self.team2_name]
            if (pts1 >= 10 or pts2 >= 10) and abs(pts1 - pts2) >= 2:
                winner = self.team1_name if pts1 > pts2 else self.team2_name
                self._match_won(winner)

    def _game_won(self, winner, is_tiebreak=False):
        if is_tiebreak:
            # In a tie-break, the winner closes the set.
            self.points = {self.team1_name: 0, self.team2_name: 0}
            self.games_won = {self.team1_name: 0, self.team2_name: 0}
            self._set_won(winner)
            self.game_mode = "regular"
        else:
            # Record last closed game winner.
            self.last_game_winner = winner
            self.games_won[winner] += 1
            self.points = {self.team1_name: 0, self.team2_name: 0}
            self._check_set_over()

    def _check_set_over(self):
        pts1 = self.games_won[self.team1_name]
        pts2 = self.games_won[self.team2_name]
        if (pts1 >= self.games_per_set or pts2 >= self.games_per_set):
            if abs(pts1 - pts2) >= 2:
                winner = self.team1_name if pts1 > pts2 else self.team2_name
                self._set_won(winner)
            elif pts1 == pts2 and pts1 == self.games_per_set:
                self.game_mode = "tiebreak"

    def _set_won(self, winner):
        # Record the finished set score.
        self.set_history.append((
            self.games_won[self.team1_name],
            self.games_won[self.team2_name]
        ))
        self.last_set_winner = winner
        self.sets_won[winner] += 1
        self.games_won = {self.team1_name: 0, self.team2_name: 0}
        self.points = {self.team1_name: 0, self.team2_name: 0}
        
        if self.total_sets == 3:
            if self.sets_won[winner] == 2:
                self._match_won(winner)
            else:
                if (self.sets_won[self.team1_name] == 1 and 
                    self.sets_won[self.team2_name] == 1):
                    self.game_mode = "super_tiebreak"
        else:
            needed = self.total_sets // 2 + 1
            if self.sets_won[winner] == needed:
                self._match_won(winner)

    def _match_won(self, winner):
        self.match_over = True
        self.winner = winner

    def get_current_game_score(self):
        if self.game_mode == "regular":
            score_map = {0: "0", 1: "15", 2: "30", 3: "40"}
            pts1 = self.points[self.team1_name]
            pts2 = self.points[self.team2_name]
            return {
                self.team1_name: score_map.get(pts1, pts1),
                self.team2_name: score_map.get(pts2, pts2)
            }
        else:
            return {
                self.team1_name: self.points[self.team1_name],
                self.team2_name: self.points[self.team2_name]
            }

    def get_set_score(self):
        return {"sets": self.sets_won, "games": self.games_won}

    def get_match_time(self):
        elapsed = datetime.datetime.now() - self.start_time
        return str(elapsed).split(".")[0]

    def reset(self):
        self.__init__(self.team1_name, self.team2_name, self.games_per_set, self.total_sets)