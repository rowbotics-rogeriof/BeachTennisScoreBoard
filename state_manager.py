import pickle
import os

STATE_FILE = "match_state.pkl"
HISTORY_FILE = "match_history.pkl"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "rb") as f:
            state = pickle.load(f)
        return state
    return None

def save_state(state):
    with open(STATE_FILE, "wb") as f:
        pickle.dump(state, f)

def clear_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "rb") as f:
            history = pickle.load(f)
        return history
    return []

def add_to_history(match):
    history = load_history()
    team1_sets = match.sets_won.get(match.team1_name, 0)
    team2_sets = match.sets_won.get(match.team2_name, 0)
    # Build a string of the finished set scores.
    set_scores = ", ".join(f"{s1}-{s2}" for s1, s2 in match.set_history)
    score_str = f"{team1_sets}-{team2_sets} ({set_scores})"
    # Append tennis ball emoji to the winning team’s name.
    t1 = match.team1_name
    t2 = match.team2_name
    if match.winner == match.team1_name:
         t1 = f"{t1} 🎾"
    elif match.winner == match.team2_name:
         t2 = f"{t2} 🎾"
    entry = {
         "date": match.start_time.strftime("%Y-%m-%d %H:%M:%S"),
         "team1": t1,
         "team2": t2,
         "score": score_str,
         "duration": match.get_match_time(),
         "point_history": match.point_history  # full timeline of point events.
    }
    history.append(entry)
    with open(HISTORY_FILE, "wb") as f:
         pickle.dump(history, f)