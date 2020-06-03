# ProjectTimekeeper

An app that logs every task of a project in an external Excel file. A task comprises a start time, an end time, a description and a duration. Tasks are grouped by day.

This app was build with Python using tkinter as GUI.

## Executable

You can create an executable with _pyinstaller_

`
pip install pyinstaller
pyinstaller --onefile --noconsole main.py
mkdir ./dist/projects
`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details