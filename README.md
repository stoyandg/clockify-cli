# Clockify CLI Time Tracker

A simple command-line tool for tracking time and submitting entries to Clockify.

## Features

- Start and stop a timer via the terminal
- Select a Clockify project to associate the time entry
- Automatically submit time entries to Clockify

## Requirements

- `Python 3.x`
- `python-dotenv`
- `requests`
- `Clockify API key` (set in `.env` file)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/stoyandg/clockify-cli.git
   cd clockify-cli-public
2. **Install dependencies**:
```bash

pip install -r requirements.txt

```
3. **Setup the `.env` file**:
```plaintext
CLOCKIFY_API_KEY=your_clockify_api_key
```
## Usage

- Start the timer:
```bash
python3 main.py --start
```
- Stop the timer and submit the time entry:
```bash
python3 main.py --stop
```

## License

This project is licensed under the GPL-3.0 License. See the `LICENSE` file for more details.
