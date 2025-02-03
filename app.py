import streamlit as st
from match import Match
import state_manager
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import datetime
from translations import get_translation

st.set_page_config(
    page_title="Beach Tennis Score Board",
    layout="centered",
    initial_sidebar_state="collapsed"  # Sidebar hidden by default.
)

# Sidebar: select language and page
lang = st.sidebar.selectbox("Select Language", ["pt", "en"], format_func=lambda x: "🇺🇸" if x == "en" else "🇧🇷")
page = st.sidebar.radio(get_translation(lang, "select_page"), (get_translation(lang, "score_board"), get_translation(lang, "score_track"), get_translation(lang, "match_analysis")))
auto_refresh = True if page == get_translation(lang, "score_board") else False

if auto_refresh:
    st_autorefresh(interval=1000, limit=1000, key="autorefresh")

if "show_new_game_form" not in st.session_state:
    st.session_state.show_new_game_form = False

match_state = state_manager.load_state()

if match_state is not None and match_state.match_over and not getattr(match_state, "added_to_history", False):
    state_manager.add_to_history(match_state)
    match_state.added_to_history = True
    state_manager.save_state(match_state)

# ---------------------------
# Score Track Page
# ---------------------------
if page == get_translation(lang, "score_track"):
    st.title(get_translation(lang, "title"))

    if match_state is None or match_state.match_over:
        st.info(get_translation(lang, "no_match_in_progress"))
        if not st.session_state.show_new_game_form:
            if st.button(get_translation(lang, "add_new_game")):
                st.session_state.show_new_game_form = True
        if st.session_state.show_new_game_form:
            with st.form("new_game_form"):
                team1_name = st.text_input(get_translation(lang, "team_1_name"), "Team A")
                team2_name = st.text_input(get_translation(lang, "team_2_name"), "Team B")
                games_per_set = st.number_input(get_translation(lang, "games_per_set"), min_value=1, value=6)
                total_sets = st.number_input(get_translation(lang, "total_sets"), min_value=1, value=1)
                submitted = st.form_submit_button(get_translation(lang, "start_match"))
                if submitted:
                    new_match = Match(team1_name, team2_name, games_per_set, total_sets)
                    state_manager.save_state(new_match)
                    st.success(get_translation(lang, "match_in_progress"))
                    st.session_state.show_new_game_form = False
                    st.rerun()
    else:
        st.success(get_translation(lang, "match_in_progress"))
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Sets", value=match_state.get_set_score()["sets"][match_state.team1_name])
            st.metric(label="Games", value=match_state.get_set_score()["games"][match_state.team1_name])
            st.metric(label="Points", value=match_state.get_current_game_score()[match_state.team1_name])
        with col2:
            st.metric(label="Sets", value=match_state.get_set_score()["sets"][match_state.team2_name])
            st.metric(label="Games", value=match_state.get_set_score()["games"][match_state.team2_name])
            st.metric(label="Points", value=match_state.get_current_game_score()[match_state.team2_name])
        
        st.write("### Add Point")
        col1, col2 = st.columns(2)
        if col1.button(match_state.team1_name):
            match_state.add_point(match_state.team1_name)
            state_manager.save_state(match_state)
            st.rerun()
        if col2.button(match_state.team2_name):
            match_state.add_point(match_state.team2_name)
            state_manager.save_state(match_state)
            st.rerun()
        
        if st.button(get_translation(lang, "reset_match")):
            st.session_state.confirm_reset = True
        if st.session_state.get("confirm_reset", False):
            st.warning(get_translation(lang, "confirm_reset"))
            col1, col2 = st.columns(2)
            if col1.button(get_translation(lang, "yes_reset")):
                state_manager.clear_state()
                st.session_state.confirm_reset = False
                st.rerun()
            if col2.button(get_translation(lang, "cancel")):
                st.session_state.confirm_reset = False
                st.rerun()

# ---------------------------
# Score Board Page
# ---------------------------
elif page == get_translation(lang, "score_board"):
    st.title(get_translation(lang, "title"))
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.markdown(f"<div style='text-align: right; font-size: 18px; color: #555;'>{get_translation(lang, 'current_time')}{current_time}</div>", unsafe_allow_html=True)
    
    css = """
    <style>
    .scoreboard {
        background-color: #000;
        color: #fff;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin-bottom: 30px;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .header > .team-name {
        flex: 0 0 40%;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
    }
    .header > .match-time {
        flex: 0 0 20%;
        font-size: 1.5rem;
        text-align: center;
    }
    .scores {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
    }
    .score-block {
        background: #333;
        padding: 15px;
        border-radius: 10px;
        width: 30%;
    }
    .score-block .label {
        font-size: 1rem;
        color: #bbb;
    }
    .score-block .value {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .match-status {
        margin-top: 20px;
        font-size: 1.5rem;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    if match_state is not None:
        team1_sets = match_state.get_set_score()["sets"][match_state.team1_name]
        team2_sets = match_state.get_set_score()["sets"][match_state.team2_name]
        team1_games = match_state.get_set_score()["games"][match_state.team1_name]
        team2_games = match_state.get_set_score()["games"][match_state.team2_name]
        team1_points = match_state.get_current_game_score()[match_state.team1_name]
        team2_points = match_state.get_current_game_score()[match_state.team2_name]
        match_time = match_state.get_match_time() if not match_state.match_over else "-"
        match_status = get_translation(lang, "match_over") + match_state.winner if match_state.match_over else get_translation(lang, "match_in_progress_status")
        team1_name = match_state.team1_name
        team2_name = match_state.team2_name
        
        # Determine the last point scorer.
        if match_state.point_history:
            last_point_team = match_state.point_history[-1].get("scoring_team", None)
        else:
            last_point_team = None

        # Determine last closed game and set winners.
        last_game_winner = match_state.last_game_winner if hasattr(match_state, "last_game_winner") else None
        last_set_winner = match_state.last_set_winner if hasattr(match_state, "last_set_winner") else None

        # Wrap values in spans: use green (#0f0) if this team won the last closed game/set/point.
        team1_sets_html   = f'<span style="color: {"#0f0" if last_set_winner == team1_name else "#fff"};">{team1_sets}</span>'
        team2_sets_html   = f'<span style="color: {"#0f0" if last_set_winner == team2_name else "#fff"};">{team2_sets}</span>'

        team1_games_html  = f'<span style="color: {"#0f0" if last_game_winner == team1_name else "#fff"};">{team1_games}</span>'
        team2_games_html  = f'<span style="color: {"#0f0" if last_game_winner == team2_name else "#fff"};">{team2_games}</span>'

        team1_points_html = f'<span style="color: {"#0f0" if last_point_team == team1_name else "#fff"};">{team1_points}</span>'
        team2_points_html = f'<span style="color: {"#0f0" if last_point_team == team2_name else "#fff"};">{team2_points}</span>'
    else:
        team1_sets_html = team1_games_html = team1_points_html = "-"
        team2_sets_html = team2_games_html = team2_points_html = "-"
        match_time = "-"
        match_status = get_translation(lang, "waiting_for_next_match")
        team1_name = "-"
        team2_name = "-"

    scoreboard_html = f"""
    <div class="scoreboard">
      <div class="header">
        <div class="team-name">{team1_name}</div>
        <div class="match-time">{match_time}</div>
        <div class="team-name">{team2_name}</div>
      </div>
      <div class="scores">
        <div class="score-block">
          <div class="label">Sets</div>
          <div class="value">{team1_sets_html}</div>
          <div class="label">Games</div>
          <div class="value">{team1_games_html}</div>
          <div class="label">Points</div>
          <div class="value">{team1_points_html}</div>
        </div>
        <div class="score-block">
          <div class="label">Sets</div>
          <div class="value">{team2_sets_html}</div>
          <div class="label">Games</div>
          <div class="value">{team2_games_html}</div>
          <div class="label">Points</div>
          <div class="value">{team2_points_html}</div>
        </div>
      </div>
      <div class="match-status">{match_status}</div>
    </div>
    """
    st.markdown(scoreboard_html, unsafe_allow_html=True)
    
    st.write(f"### {get_translation(lang, 'last_3_matches')}")
    history = state_manager.load_history()
    if history:
        last3 = history[-3:][::-1]
        css_history = """
        <style>
        .match-history-table {
             width: 100%;
             border-collapse: collapse;
             margin: 20px 0;
             font-family: Arial, sans-serif;
             font-size: 16px;
             color: #333;
        }
        .match-history-table th, .match-history-table td {
             border: 1px solid #ddd;
             padding: 8px;
             text-align: center;
        }
        .match-history-table th {
             background-color: #000;
             color: #fff;
        }
        .match-history-table tr:nth-child(even) {
             background-color: #f2f2f2;
        }
        .match-history-table tr:hover {
             background-color: #ddd;
        }
        </style>
        """
        html_table = "<table class='match-history-table'>"
        html_table += "<thead><tr><th>Team 1</th><th>Team 2</th><th>Score</th><th>Duration</th></tr></thead><tbody>"
        for entry in last3:
             html_table += (
                 f"<tr>"
                 f"<td>{entry['team1']}</td>"
                 f"<td>{entry['team2']}</td>"
                 f"<td>{entry['score']}</td>"
                 f"<td>{entry['duration']}</td>"
                 f"</tr>"
             )
        html_table += "</tbody></table>"
        st.markdown(css_history + html_table, unsafe_allow_html=True)
    else:
        st.info(get_translation(lang, "no_match_history"))

# ---------------------------
# Match Analysis Page
# ---------------------------
elif page == get_translation(lang, "match_analysis"):
    st.title(get_translation(lang, "match_analysis_title"))
    history = state_manager.load_history()
    if not history:
         st.info(get_translation(lang, "no_match_history_analysis"))
    else:
         # Build a list of match labels for selection.
         match_options = [f"{entry['date']} - {entry['team1']} vs {entry['team2']}" for entry in history]
         selected_index = st.selectbox(get_translation(lang, "select_match"), options=list(range(len(history))), 
                                       format_func=lambda x: match_options[x])
         selected_match = history[selected_index]
         st.write(f"### {get_translation(lang, 'point_by_point_timeline')}")
         
         # Get the original team names (remove emoji if present).
         original_team1 = selected_match["team1"].replace(" 🎾", "")
         original_team2 = selected_match["team2"].replace(" 🎾", "")
         
         timeline = []
         for event in selected_match.get("point_history", []):
             # Format scores as "score1-score2"
             game_score = event.get("current_game_score", {})
             game_score_str = f"{game_score.get(original_team1, 0)}-{game_score.get(original_team2, 0)}"
             set_score = event.get("current_set_score", {})
             set_score_str = f"{set_score.get(original_team1, 0)}-{set_score.get(original_team2, 0)}"
             match_score = event.get("current_match_score", {})
             match_score_str = f"{match_score.get(original_team1, 0)}-{match_score.get(original_team2, 0)}"
             
             timeline.append({
                 "Game Time": event.get("time", ""),
                 "Team Scored": event.get("scoring_team", ""),
                 "Game Score": game_score_str,
                 "Set Score": set_score_str,
                 "Match Score": match_score_str
             })
         
         if timeline:
             df_timeline = pd.DataFrame(timeline)
             
             st.markdown(df_timeline.style.hide(axis="index").to_html(), unsafe_allow_html=True)
             
             # Download CSV option.
             csv = df_timeline.to_csv(index=False).encode('utf-8')
             st.download_button(
                 label=get_translation(lang, "download_csv"),
                 data=csv,
                 file_name="point_by_point_timeline.csv",
                 mime="text/csv",
                 key="download-csv"
             )
         else:
             st.info(get_translation(lang, "no_point_events"))