

@dataclass(frozen=True)
class AppConfig:
    """Hold window settings in one place so they are easy to change."""

    title: str = "Quetza | Run"
    width: int = 900
    height: int = 600
    background: str = "#FFFFFF"

    def to_json(self) -> str:
        """Return the settings as JSON text without writing any file."""
        # PSEUDOCODE:
        #     Put the settings into a dictionary.
        #     Convert the dictionary into readable JSON text.
        #     Return that text to the code that requested it.
        settings = {
            "title": self.title,
            "width": self.width,
            "height": self.height,
            "background": self.background,
        }
        return json.dumps(settings, indent=4)


# ---------------------------------------------------------------------------
# APPLICATION CLASS — THE WINDOW AND ITS USER ACTIONS







# ---------------------------------------------------------------------------
# ACTIVE IMPORTS — THESE ARE USED BY THIS STARTER
# ---------------------------------------------------------------------------

# Tkinter creates desktop windows, buttons, labels, and other screen controls.
# We use it here to open the white window and respond to user actions.
import tkinter as tk

# Messagebox displays small windows containing information, warnings, or errors.
# We use it in the example action so a future button can show a message.
from tkinter import messagebox

# Dataclass creates common setup code for a class that mainly holds values.
# We use it to keep the application title, size, and background settings together.
from dataclasses import dataclass

# JSON converts Python values into a common text format and reads that format back.
# We use it in the settings example to produce text that could later be saved.
import json


# ---------------------------------------------------------------------------
# 2. OPTIONAL PYTHON STANDARD LIBRARY IMPORTS — NO PIP INSTALL NEEDED
# ---------------------------------------------------------------------------

# Ttk provides themed controls such as buttons, tables, and progress bars.
# Use it when you want more built-in control types or a different control style.
# from tkinter import ttk

# Filedialog opens the operating system's file selection and save windows.
# Use it when a user needs to choose an input file or an output location.
# from tkinter import filedialog

# Path represents file and folder locations as Python objects.
# Use it to build paths and read or write files without manually joining slashes.
# from pathlib import Path

# CSV reads and writes plain-text tables whose values are separated by commas.
# Use it to exchange simple rows of information with spreadsheet programs.
# import csv

# Datetime supplies tools for working with dates, times, and time differences.
# Use it to record when something happened or display a date in a report.
# from datetime import datetime, timedelta

# Logging records messages about what a program is doing and what went wrong.
# Use it to help investigate problems without scattering print calls everywhere.
# import logging

# OS provides access to operating system features such as environment variables.
# Use it when your application needs system settings supplied outside its code.
# import os

# Sys provides information about the running Python process and its arguments.
# Use it to read command-line arguments or identify the active Python interpreter.
# import sys

# SQLite3 lets Python work with a small database stored in a local file.
# Use it when your application needs searchable records without a database server.
# import sqlite3

# Re searches and matches text using patterns called regular expressions.
# Use it to check input formats or extract specific pieces from a larger string.
# import re

# Threading can run waiting-heavy work without blocking the main window.
# Use it for background tasks while keeping screen updates on the main GUI thread.
# import threading

# Queue safely passes items between different threads.
# Use it with background workers so the main GUI thread can receive their results.
# import queue

# Subprocess starts another program and can capture its output.
# Use it when your app needs a separate tool such as FFmpeg to perform a task.
# import subprocess

# Webbrowser opens a link in the user's default browser.
# Use it for a Help button or a link to your application's documentation.
# import webbrowser


# ---------------------------------------------------------------------------
# 3. OPTIONAL THIRD-PARTY IMPORTS — INSTALL ONLY WHAT YOUR FEATURE NEEDS
# ---------------------------------------------------------------------------

# Django is a framework for building websites with pages, accounts, and databases.
# Use it for a web application with its own Django project setup.
# Install: python -m pip install django
# import django
#
# Django project example, run separately in PowerShell:
#     python -m django startproject mysite
#     cd .\mysite
#     python manage.py migrate
#     python manage.py runserver
# This is a separate web project; importing Django does not create a website.

# Pandas works with tables of data and supports filtering, grouping, and summaries.
# Use it when your application needs to clean or analyze rows of information.
# Install: python -m pip install pandas
# import pandas as pd
#
# Example: table = pd.read_csv("input.csv")
# Some file formats, including Excel, need an additional supported package.

# NumPy works with arrays of numbers and performs many numerical operations quickly.
# Use it for calculations on many values or as part of scientific data processing.
# Install: python -m pip install numpy
# import numpy as np

# Requests sends HTTP requests to websites and web services.
# Use it when your application needs to get data from an API or send a request.
# Install: python -m pip install requests
# import requests
#
# In a GUI, run slow network calls in a worker and set a request timeout.
# Return results through a queue that the main thread checks with after().

# Pillow opens, edits, resizes, and saves common image formats.
# Use its Image tools for image processing and ImageTk for Tkinter image display.
# Install: python -m pip install Pillow
# from PIL import Image, ImageTk
#
# The package is installed as Pillow but imported through the name PIL.

# Openpyxl reads and writes Excel workbooks in the XLSX format.
# Use it when you need worksheets, cell values, formulas, or workbook formatting.
# Install: python -m pip install openpyxl
# import openpyxl

# Matplotlib creates charts such as line plots, bar charts, and scatter plots.
# Use it when a picture of your data is easier to understand than a table.
# Install: python -m pip install matplotlib
# import matplotlib.pyplot as plt

# PyInstaller packages a Python application with the files needed to run it.
# Use it when building a distributable app rather than during normal app startup.
# Install: python -m pip install pyinstaller
# import PyInstaller.__main__
#
# Usually you run PyInstaller in PowerShell instead of importing it in run.py:
#     python -m PyInstaller --onefile --windowed --name QuetzaRun run.py
#
# Build on Windows to produce a Windows executable.
# The executable will be placed in the dist folder.
# During debugging, omit --windowed if you want to see console output.
# Keep programmatic PyInstaller build code in a separate build file if needed.


# ---------------------------------------------------------------------------
# SETTINGS — CHANGE THESE VALUES FOR YOUR NEXT PROJECT
# ---------------------------------------------------------------------------
