# Application Runtime Tracker

This Python script tracks the runtime of a specified application, logging the duration the application is running over multiple sessions.

## Features

- Tracks the total runtime of a specified application.
- Supports continuation from previous sessions.
- Provides formatted runtime breakdown (hours, minutes, seconds).

## Requirements

- Python 3.12
- Check Requirements.txt

## Installation

1. Clone this repository or download the repository as a zip.
2. Ensure you have Python 3.12 installed on your system.
3. Install the required libraries:
    ```sh
    pip install -r Requirements.txt
    ```

## Usage

1. Run the script:
    ```sh
    python app_runtime_tracker.py
    ```

2. The script will prompt you to ensure that the target application is running. After a short delay, it will proceed.

3. If a previous session is detected, you will be prompted to continue from the previous session or start a new one:
    - **Continue**: The script will add time to the previous session's runtime.
    - **Reset**: The script will start a new tracking session.

4. If starting a new session, enter the exact name of the executable you want to track. For Windows, this should be the executable name (e.g., `Spotify.exe` for Spotify).

5. The script will display the tracked runtime in real-time. To stop tracking, close the tracked application.

6. After stopping, you will be prompted to save the data:
    - **Save**: The session's runtime will be added to the previous total runtime and saved.
    - **Discard**: The session's runtime will be discarded.

## Notes

- Ensure the application to be tracked is running before you start the script.
- The script saves runtime data in `data/app_time.txt`.
