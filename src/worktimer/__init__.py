from datetime import date
import json
import time
from pathlib import Path
import typer

app = typer.Typer()

home_dir = Path.home()
data_dir = home_dir / ".local" /"share" / "worktimer"
data_dir.mkdir(parents=True, exist_ok=True)
file_path = data_dir / "saved_times.json"

def create_file_if_not_exists():
    if not file_path.exists():
        with open(file_path, "w") as f:
            json.dump({"is_running": False}, f)

create_file_if_not_exists()

@app.command()
def start():
    """
    Start the work timer.
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    if data.get("is_running"):
        print("Timer is already running.")
        return

    data["is_running"] = True

    today = f"{date.today()}"

    if today not in data:
        data[today] = []

    data[today].append({"start_time": time.time(), "stop_time": None})

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


@app.command()
def stop():
    """
    Stop the work timer.
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    if not data.get("is_running"):
        print("Timer is not running.")
        return

    if data.get("is_running"):
        data["is_running"] = False

    today = f"{date.today()}"

    for t in data.get(today, []):
        if t["stop_time"] is None:
            t["stop_time"] = time.time()

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

            break

@app.command()
def today():
    """
    Show the total time worked today.
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    today = f"{date.today()}"
    total_time = 0

    sessions = data.get(today, [])
    for session in sessions:
        if session["stop_time"] is not None:
            total_time += session["stop_time"] - session["start_time"]

        print(f"Start: {time.ctime(session['start_time'])}, Stop: {time.ctime(session['stop_time']) if session['stop_time'] else 'Running'}")

    hours, remainder = divmod(total_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Total time worked today: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    

def main() -> None:
    app()

if __name__ == "__main__":
    main()