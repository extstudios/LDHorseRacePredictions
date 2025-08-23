import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DB_FILE = 'race_data.csv'

# Load or create the database
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=['Game', 'Round', '1st', '2nd', '3rd', '4th'])
    df.to_csv(DB_FILE, index=False)
else:
    df = pd.read_csv(DB_FILE)

current_game = None
current_round = 1

# Mapping for racer names
RACER_NAMES = {1: 'Zergling', 2: 'Reaper', 3: 'Phoenix', 4: 'Hellion'}

# Enhanced predictor using all data
def recommend_next_bet(global_df):
    if global_df.empty or len(global_df) < 2:
        return most_frequent_first(global_df)

    global_df['Order'] = global_df[['1st', '2nd', '3rd', '4th']].astype(str).agg('-'.join, axis=1)
    last_order = global_df['Order'].iloc[-1]

    # Find prior matches of this order and what came after them
    matches = global_df[global_df['Order'] == last_order]
    indices = matches.index.tolist()
    next_1sts = []

    for i in indices:
        if i + 1 in global_df.index:
            next_1sts.append(global_df.loc[i + 1, '1st'])

    if next_1sts:
        return pd.Series(next_1sts).value_counts().idxmax()

    return most_frequent_first(global_df)

# Fallback: most frequent 1st-place finisher
def most_frequent_first(df):
    if '1st' not in df.columns or df['1st'].empty:
        return 1
    return int(df['1st'].value_counts().idxmax())

# Show heatmap
def plot_heatmap(df):
    if df.empty or '1st' not in df.columns:
        messagebox.showinfo("Heatmap", "Not enough data to generate heatmap.")
        return

    heatmap_data = df.pivot_table(index='Game', columns='1st', aggfunc='size', fill_value=0)
    if heatmap_data.empty:
        messagebox.showinfo("Heatmap", "No heatmap data available.")
        return

    heatmap_data.rename(columns=RACER_NAMES, inplace=True)

    plt.figure(figsize=(8, 6))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu")
    plt.title("1st Place Finishes Heatmap")
    plt.xlabel("Racer")
    plt.ylabel("Game")
    plt.tight_layout()
    plt.show()

# Show repeated patterns
def detect_patterns(df):
    if df.empty:
        return pd.DataFrame()
    df['Order'] = df[['1st', '2nd', '3rd', '4th']].astype(str).agg('-'.join, axis=1)
    summary = df.groupby(['Game', 'Order']).size().reset_index(name='Count')
    return summary[summary['Count'] > 1]

# Popup for analysis
def show_analysis():
    global df
    plot_heatmap(df)
    patterns = detect_patterns(df)
    if patterns.empty:
        messagebox.showinfo("Patterns", "No repeating patterns found.")
    else:
        top = tk.Toplevel()
        top.title("Frequent Race Order Patterns")
        tk.Label(top, text="Repeated Race Orders (Appeared More Than Once)").pack(pady=5)
        text = tk.Text(top, width=60, height=20)
        text.pack()
        text.insert(tk.END, patterns.to_string(index=False))
        text.config(state='disabled')

# Update recommendation label
def update_bet_label(frame):
    global df
    recommended = recommend_next_bet(df)
    racer_name = RACER_NAMES.get(recommended, f"Racer {recommended}")
    label = frame.nametowidget("bet_label")
    label.config(text=f"Recommended Bet: {racer_name}")

# Submit race
def submit_result(entries, root, frame):
    global df, current_game, current_round
    try:
        positions = [int(entry.get()) for entry in entries]
        if sorted(positions) != [1, 2, 3, 4]:
            raise ValueError("Positions must be 1 through 4 with no duplicates.")
        new_row = {
            'Game': current_game,
            'Round': current_round,
            '1st': positions[0],
            '2nd': positions[1],
            '3rd': positions[2],
            '4th': positions[3],
        }
        df.loc[len(df)] = new_row
        df.to_csv(DB_FILE, index=False)
        current_round += 1
        update_bet_label(frame)
        for entry in entries:
            entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Finish game
def finish_game(frame, root):
    global current_game, current_round
    current_game = None
    current_round = 1
    frame.destroy()
    show_main_menu(root)

# Input screen
def show_race_screen(root):
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)
    tk.Label(frame, text=f"Game {current_game} - Enter Race Result").pack(pady=5)

    entry_labels = ["1st", "2nd", "3rd", "4th"]
    entries = []
    for label in entry_labels:
        tk.Label(frame, text=label).pack()
        entry = tk.Entry(frame)
        entry.pack()
        entries.append(entry)

    tk.Button(frame, text="Submit Result", command=lambda: submit_result(entries, root, frame)).pack(pady=10)
    tk.Label(frame, name="bet_label", text="Recommended Bet: Calculating...").pack(pady=10)
    update_bet_label(frame)

    tk.Button(frame, text="View Analysis", command=show_analysis).pack(pady=5)
    tk.Button(frame, text="Finish Game", command=lambda: finish_game(frame, root)).pack(pady=10)

# Start game
def start_new_game(root, frame):
    global current_game, current_round, df
    if df.empty or 'Game' not in df.columns:
        current_game = 1
    else:
        try:
            current_game = int(df['Game'].max()) + 1
        except:
            current_game = 1
    current_round = 1
    frame.destroy()
    show_race_screen(root)

# Main menu
def show_main_menu(root):
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=20)

    next_game = 1
    if not df.empty and 'Game' in df.columns:
        try:
            next_game = int(df['Game'].max()) + 1
        except:
            pass

    tk.Label(frame, text=f"Next Game: {next_game}").pack(pady=5)
    tk.Button(frame, text="Start Game", command=lambda: start_new_game(root, frame)).pack(pady=10)

# Launch app
def main():
    root = tk.Tk()
    root.title("Race Betting Predictor")
    root.wm_attributes("-topmost", 1)  # Always on top
    show_main_menu(root)
    root.mainloop()

if __name__ == '__main__':
    main()
