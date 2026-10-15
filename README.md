# Edu Revolution — Attendance Percentage Calculator

A simple, modern desktop GUI that helps students calculate attendance and plan how many classes they need to attend to reach a target percentage.

## Features

- Calculates current attendance percentage.
- Shows whether you meet your target attendance.
- Calculates the minimum consecutive classes needed to reach a target.
- If you are already at or above target, estimates how many upcoming classes you can miss while staying at the target.
- Input validation and helpful error messages.
- Dark-themed interface with a progress bar.
- Uses Python's built-in Tkinter library — no third-party packages required.

## Preview

The app opens in a desktop window with input fields for subject, target percentage, total classes held, and classes attended.

## Requirements

- Python 3.9 or newer recommended.
- Tkinter (usually included with Python on Windows and macOS; on some Linux distributions, install the `python3-tk` package).

## Run locally

1. Install Python from [python.org](https://www.python.org/downloads/) if it is not installed.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python attendance_calculator.py
   ```

   On some systems, use `python3 attendance_calculator.py`.

## How to use

1. Enter the subject name.
2. Set your target attendance percentage (for example, `75`).
3. Enter the total number of classes held.
4. Enter the number of classes you attended.
5. Click **Calculate Attendance**.

### Example

If 40 classes have been held and you attended 28:

- Attendance = 28 / 40 × 100 = **70%**
- With a target of 75%, you need to attend the next **8 classes consecutively** to reach 75%.

The calculator assumes each future class has equal weight and does not account for different subject credit rules, cancelled classes, or institution-specific attendance policies. Confirm official attendance requirements with your institution.

## GitHub upload

Create a new repository on GitHub, then run these commands inside this project folder:

```bash
git init
git add .
git commit -m "Add Edu Revolution attendance calculator"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/attendance-percentage-calculator.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username and use the repository URL GitHub provides.

## Project structure

```text
edu-revolution-attendance-calculator/
├── attendance_calculator.py
├── README.md
├── LICENSE
└── .gitignore
```

## License

MIT — see [LICENSE](LICENSE).
