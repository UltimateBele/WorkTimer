**Intro**

This project is for tracking your (work) time and automatically putting them into a PDF for each day in a month.

**Requirements**

uv needs to be installed

**Setup**

After cloning the repo, enter this into the terminal:

```bash
uv sync
```

**Using the app**

To start the timer enter:

```bash
uv run worktimer start
or
worktimer start
```

To stop the timer enter:

```bash
uv run worktimer stop
or
worktimer stop
```

To show the working time of a specific day enter:

```bash
uv run worktimer print-worktime [year-month-day]
or
worktimer print-worktime [year-month-day]
```

To show the current working time of today enter:

```bash
uv run worktimer print-today
or
worktimer print-today
```

To show the total working time of a specific month enter:

```bash
uv run worktimer print_total_worktime_month [year-month]
or
worktimer print_total_worktime_month [year-month]
```

To export it into a PDF enter:

```bash
uv run worktimer export
or
worktimer export
```
