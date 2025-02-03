# Beach Tennis Score Board

This project is a web application for tracking and analyzing beach tennis matches. It allows users to start new matches, track scores in real-time, and analyze match history.

## Features

- **Multilanguage Support**: The application supports both English (en) and Portuguese (pt).
- **Score Tracking**: Track the scores of ongoing matches, including points, games, and sets.
- **Score Board**: Display the current match status and scores in a visually appealing format.
- **Match Analysis**: Analyze the history of past matches, including point-by-point timelines.
- **Match History**: View the last three matches played.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/rowbotics-rogeriof/BeachTennisScoreBoard.git
    cd beach-tennis-score-board
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the application:
    ```sh
    streamlit run app.py
    ```

## Usage

### Starting a New Match

1. Open the application in your web browser.
2. Select the "Score Track" page from the sidebar.
3. If no match is in progress, click the "Add New Game" button.
4. Fill in the team names, games per set, and total sets, then click "Start Match".

### Tracking Scores

1. On the "Score Track" page, use the buttons to add points to each team.
2. The application will automatically update the scores and determine when games and sets are won.

### Viewing the Score Board

1. Select the "Score Board" page from the sidebar.
2. The current match status and scores will be displayed.

### Analyzing Match History

1. Select the "Match Analysis" page from the sidebar.
2. Choose a match from the dropdown to view its point-by-point timeline.
3. Download the timeline as a CSV file if needed.

## Multilanguage Support

The application supports English and Portuguese. You can switch between languages using the language selector in the sidebar.

## File Structure

- [app.py](http://_vscodecontentref_/1): Main application file.
- [match.py](http://_vscodecontentref_/2): Contains the [Match](http://_vscodecontentref_/3) class for managing match state.
- [state_manager.py](http://_vscodecontentref_/4): Functions for saving, loading, and clearing match state and history.
- [translations.py](http://_vscodecontentref_/5): Contains translations for supported languages.
- [match_state.pkl](http://_vscodecontentref_/6): Pickle file for storing the current match state.
- [match_history.pkl](http://_vscodecontentref_/7): Pickle file for storing match history.
- [readme.md](http://_vscodecontentref_/8): This README file.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.