from datetime import date
import json
import time
from pathlib import Path
import typer
from fpdf import FPDF

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

def get_data():
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def write_data(data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def get_sessions_for_date(data, date):
    return data.get(date, [])

def get_session_start_and_stop_times(session):
    """
    stop_time is None if the session is still running.
    """
    start_time = session["start_time"]
    stop_time = session["stop_time"]
    return start_time, stop_time

def get_session_time(session, count_running=True):
    start_time, stop_time = get_session_start_and_stop_times(session)
    if stop_time is not None:
        return stop_time - start_time
    elif count_running:
        return time.time() - start_time

    return 0.0

def get_sessions_time(sessions, count_running=True):
    total_time = 0.0
    for session in sessions:
        total_time += get_session_time(session, count_running)
    return total_time

def get_hours_minutes_seconds_from_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), int(seconds)

def print_session_time(session):
    start_time, stop_time = get_session_start_and_stop_times(session)
    session_time = get_session_time(session)

    session_hours, session_minutes, session_seconds = get_hours_minutes_seconds_from_seconds(session_time)

    print(f"Start: {time.ctime(start_time)}, Stop: {time.ctime(stop_time) if stop_time else 'Running'} - Duration: {int(session_hours)}h {int(session_minutes)}m {int(session_seconds)}s")

def print_sessions_time(sessions):
    for session in sessions:
        print_session_time(session)

def print_total_sessions_time(sessions):
    total_time = get_sessions_time(sessions)
    hours, minutes, seconds = get_hours_minutes_seconds_from_seconds(total_time)
    print(f"Total time worked: {int(hours)}h {int(minutes)}m {int(seconds)}s")

@app.command()
def print_worktime(date):
    """
    Show the work time for a specific date.
    """
    data = get_data()

    sessions = get_sessions_for_date(data, date)

    print_sessions_time(sessions)
    print_total_sessions_time(sessions)

@app.command()
def print_today():
    """
    Show the work time for today.
    """
    today = f"{date.today()}"
    print_worktime(today)

def is_timer_running(data):
    return data.get("is_running", False)

@app.command()
def start():
    """
    Start the work timer.
    """
    data = get_data()

    if is_timer_running(data):
        print("Timer is already running.")
        return

    data["is_running"] = True

    today = f"{date.today()}"

    if today not in data:
        data[today] = []

    data[today].append({"start_time": time.time(), "stop_time": None})

    write_data(data)


@app.command()
def stop():
    """
    Stop the work timer.
    """
    data = get_data()

    if not is_timer_running(data):
        print("Timer is not running.")
        return

    if data.get("is_running"):
        data["is_running"] = False

    today = f"{date.today()}"

    empty_stop_time = [t for t in data.get(today, []) if t["stop_time"] is None]
    if len(empty_stop_time) != 1:
        print("Something went wrong. There should be exactly one session with a None stop_time.")
        return

    empty_stop_time[0]["stop_time"] = time.time()

    write_data(data)

@app.command()
def export():
    """
    Export the work timer data to a PDF file.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica', size=12)


    data = get_data()
    today = f"{date.today()}"
    
    sessions_time = get_sessions_time(get_sessions_for_date(data, today))
    hours, minutes, seconds = get_hours_minutes_seconds_from_seconds(sessions_time)
    text = f"""
            Work Timer Data Export\n\n
            {hours}h {minutes}m {seconds}s worked today\n
        """
    pdf.cell(text=text, ln=True)
    pdf.output("hello_world.pdf")

def main() -> None:
    app()

if __name__ == "__main__":
    main()