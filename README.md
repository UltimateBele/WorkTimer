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
uv run worktimer today
or
worktimer print-worktime [date]
```

To show the current working time of today enter:

```bash
uv run worktimer today
or
worktimer print-today
```

To export it into a PDF enter:

```bash
uv run worktimer export
or
worktimer export
```
