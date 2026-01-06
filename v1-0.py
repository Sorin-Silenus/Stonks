# --- Import Libraries --- #
# ------------------------ #
# using python version 3.12.8
import argparse
import yfinance as yf
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==== yfinance rate-limit and caching wrappers (inserted by assistant) ====
# These wrappers aim to reduce burstiness and add gentle retries so terminal runs
# behave like PyCharm runs without changing your call sites or logic.

import time as _yl_time
import random as _yl_rand
import threading as _yl_threading
import requests as _yl_requests

try:
    import yfinance as _yl_yf
except Exception:
    _yl_yf = None

# Shared HTTP session
_YL_SESSION = _yl_requests.Session()

# Ticker to be reserached
# TODO: make this user input
ticker_symbol = "VYM"
ticker = yf.Ticker(ticker_symbol)
info = ticker.info
historical_data = ticker.history(period="1mo").reset_index()

#  --- GUI Application --- #
# ------------------------ #

root = tk.Tk()
root.title(f"{ticker_symbol} Stock Data")
root.geometry("800x600")
root.configure(bg="black")

# Header Frame (Stock name and info)
header_frame = tk.Frame(root, pady=10, bg = "white") # create header frame
header_frame.pack(fill="x") # stretch header frame across the window
# Stock name label inside header frame
stock_name_label = tk.Label(
    header_frame,
    text=ticker_symbol,
    font=("Arial", 20, "bold"),
    bg="lightgray",
    fg="white"
)
stock_name_label.pack()

# --- Graph Logic ---

# Graph Frame (Hold the graph of the stock of the month)
graph_frame = tk.Frame(root, pady=10, bg="black")
graph_frame.pack(fill="both", expand=True)

# Create the Figure and Axis
# 'facecolor' sets the background of the plot area
fig, ax = plt.subplots(figsize=(6, 4), dpi=100, facecolor='black')

# --- Calculate Performance ---
# Get the first and last closing prices from historical_data
start_price = historical_data['Close'].iloc[0]
end_price = historical_data['Close'].iloc[-1]

# Determine color: Green if price increased, else red
if end_price >= start_price:
    stock_color = "#00ff00" # Green
else:
    stock_color = "#ff3333" # Red

# Plot the data
ax.plot(historical_data['Date'], historical_data['Close'], color=stock_color, linewidth=2)

# 3. Styling
ax.set_facecolor('black') # Interior plot color
ax.tick_params(axis='x', colors='white') # Date labels color
ax.tick_params(axis='y', colors='white') # Price labels color
ax.set_ylabel("Price ($)", color='white')
ax.grid(color='gray', linestyle='--', alpha=0.3)
fig.autofmt_xdate() # Rotates dates for readability

# --- Integrate with Tkinter ---
# Put the graph inside graph_frame
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_draw = canvas.get_tk_widget()
canvas_draw.pack(fill="both", expand=True)



# Start the window
root.mainloop()
