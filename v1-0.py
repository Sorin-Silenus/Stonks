# --- Import Libraries --- #
# ------------------------ #
# using python version 3.12.8
import argparse
import yfinance as yf
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Fetch Stock Data --- #
# ------------------------ #
# TODO: make this user input

def show_ticker_input():
    input_frame = tk.Frame(root, bg="black")
    input_frame.pack(fill="both", expand=True)

    title = tk.Label(
        input_frame,
        text="Enter Stock Ticker",
        font=("Arial", 22, "bold"),
        bg="black",
        fg="white"
    )
    title.pack(pady=30)

    ticker_entry = tk.Entry(
        input_frame,
        font=("Arial", 18),
        justify="center"
    )
    ticker_entry.pack(pady=10)

    ticker_entry.focus()

    # --- Error label (initially hidden) ---
    error_label = tk.Label(
        input_frame,
        text="",
        font=("Arial", 12),
        fg="red",
        bg="black"
    )
    error_label.pack(pady=5)

    def submit():
        symbol = ticker_entry.get().strip().upper()
        if not symbol:
            return

        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1mo")

        if hist.empty:
            error_label.config(text="Invalid ticker symbol")
            return

        # Valid ticker → clear error and move on
        error_label.config(text="")
        input_frame.destroy()
        load_stock_app(symbol)

    submit_btn = tk.Button(
        input_frame,
        text="Load Stock",
        font=("Arial", 14),
        command=submit
    )
    submit_btn.pack(pady=20)

    root.bind("<Return>", lambda e: submit())


def load_stock_app(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    historical_data = ticker.history(period="1mo").reset_index()

    if historical_data.empty:
        tk.Label(root, text="Invalid ticker", fg="red", bg="black").pack()
        return

    root.title(f"{ticker_symbol} Stock Data")

    # --- Header ---
    header_frame = tk.Frame(root, pady=10, bg="black")
    header_frame.pack(fill="x")

    stock_name_label = tk.Label(
        header_frame,
        text=ticker_symbol,
        font=("Arial", 20, "bold"),
        bg="black",
        fg="#00ffcc"
    )
    stock_name_label.pack()

    # --- Graph Frame ---
    graph_frame = tk.Frame(root, pady=10, bg="black")
    graph_frame.pack(fill="both", expand=True)

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100, facecolor='black')

    start_price, end_price = historical_data['Close'].iloc[[0, -1]]
    stock_color = "#00ff00" if end_price >= start_price else "#ff3333"

    ax.plot(
        historical_data['Date'],
        historical_data['Close'],
        color=stock_color,
        linewidth=2
    )

    ax.set_facecolor('black')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_ylabel("Price ($)", color='white')
    ax.grid(color='gray', linestyle='--', alpha=0.3)
    fig.autofmt_xdate()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()

#  --- GUI Application --- #
# ------------------------ #

root = tk.Tk()
root.geometry("800x600")
root.configure(bg="black")
show_ticker_input()
# start the window
root.mainloop()
