import time 
import random 
import tkinter as tk 
from tkinter import messagebox 
import matplotlib.pyplot as plt 

easysentences = [ 
    "Hello World", 
    "I love programming", 
    "Health is Wealth", 
    "The quick brown fox", 
    "What a beautiful day it is", 
    "He has a red car" 
] 

mediumsentences = [ 
    "The quick brown fox jumps over the lazy dog", 
    "The rain in Spain falls mainly on the plain", 
    "Early to bed early to rise makes a man healthy, wealthy, and wise", 
    "The traffic on the highway moved slowly due to the heavy rain", 
    "He decided to take a walk through the quiet park after dinner", 
    "The colorful birds chirped happily as the sun rose above the hills" 
] 

hardsentences = [ 
    "She carefully packed the boxes, ensuring nothing would break during the move", 
    "Despite the challenging weather, they continued their journey with unwavering determination", 
    "The old lighthouse stood proudly against the crashing waves, a beacon of hope", 
    "After a long day of work, they gathered together for a relaxing evening of storytelling", 
    "He meticulously organized the documents, ensuring they were in perfect order for the meeting", 
    "The vibrant colors of the sunset painted the sky with a breathtaking masterpiece of light", 
    "She patiently listened to his problems, offering comfort and understanding without judgment" 
] 

def getsentence(difficulty): 
    if difficulty == 'easy': 
        return random.choice(easysentences) 
    elif difficulty == 'medium': 
        return random.choice(mediumsentences) 
    elif difficulty == 'hard': 
        return random.choice(hardsentences) 

def calculate_accuracy(original, typed): 
    original_words = original.split() 
    typed_words = typed.split() 
    correct = sum(o == t for o, t in zip(original_words, typed_words))  # Case-sensitive 
    total = len(original_words) 
    accuracy = (correct / total) * 100 if total > 0 else 0 
    errors = total - correct 
    return accuracy, errors, correct, total 

def calculate_wpm(start_time, end_time, typed_text): 
    time_taken = end_time - start_time 
    words = len(typed_text.split()) 
    wpm = (words / time_taken) * 60 if time_taken > 0 else 0 
    return wpm 

def calculate_wps(words, time_taken): 
    return words / time_taken if time_taken > 0 else 0 

def countdown(seconds, countdown_label): 
    countdown_label.config(text=f"Get ready... {seconds}") 
    if seconds > 0: 
        countdown_label.after(1000, countdown, seconds - 1, countdown_label) 
    else: 
        countdown_label.config(text="Go!") 

def show_graphs(wpm, wps, accuracy, correct, errors): 
    plt.figure(figsize=(10, 5)) 

    plt.subplot(1, 2, 1) 
    metrics = ['WPM', 'WPS', 'Accuracy'] 
    values = [wpm, wps, accuracy] 
    colors = ['skyblue', 'orange', 'green'] 
    plt.bar(metrics, values, color=colors) 
    plt.title('Typing Test Metrics') 
    plt.ylim(0, max(values) + 20) 
    for i, v in enumerate(values): 
        plt.text(i, v + 1, f"{v:.2f}", ha='center') 

    plt.subplot(1, 2, 2) 
    labels = ['Correct', 'Incorrect'] 
    data = [correct, errors] 
    colors = ['limegreen', 'red'] 
    plt.pie(data, labels=labels, autopct='%1.1f%%', colors=colors) 
    plt.title('Word Accuracy') 
    plt.tight_layout() 
    plt.show() 

def show_word_comparison(original, typed): 
    original_words = original.split() 
    typed_words = typed.split() 
    comparison = [] 
    for i, (o, t) in enumerate(zip(original_words, typed_words)): 
        if o == t: 
            comparison.append(f"[✓] {t}") 
        else: 
            comparison.append(f"[✗] {t} (expected: {o})") 

    if len(typed_words) > len(original_words): 
        extra = typed_words[len(original_words):] 
        comparison.extend([f"[✗] {word} (extra)" for word in extra]) 
    elif len(original_words) > len(typed_words): 
        missing = original_words[len(typed_words):] 
        comparison.extend([f"[✗] (missing: {word})" for word in missing]) 

    return comparison 

def start_test(difficulty, sentence_label, typed_text_var, start_button, end_button, results_label, countdown_label): 
    original_text = getsentence(difficulty) 
    sentence_label.config(text=original_text) 
    typed_text_var.set("")   
    countdown(3, countdown_label) 
    start_time = time.time() 

    def end_test(): 
        end_time = time.time() 
        typed_text_value = typed_text_var.get() 
        wpm = calculate_wpm(start_time, end_time, typed_text_value) 
        accuracy, errors, correct, total = calculate_accuracy(original_text, typed_text_value) 
        total_time_taken = end_time - start_time 
        results_label.config(text=f"Words per minute: {wpm:.2f}\nAccuracy: {accuracy:.2f}%\nErrors: {errors}/{total}\nTotal time taken: {total_time_taken:.2f} seconds") 
        comparison = show_word_comparison(original_text, typed_text_value) 
        results_label.config(text="\n".join(comparison) + "\n" + results_label.cget("text")) 
        show_graphs(wpm, calculate_wps(len(typed_text_value.split()), total_time_taken), accuracy, correct, errors) 
        end_button.config(state="disabled") 
        start_button.config(state="normal") 

    end_button.config(command=end_test) 
    start_button.config(state="disabled")   
    end_button.config(state="normal")   

def setup_gui(): 
    root = tk.Tk() 
    root.title("Typing Speed Test") 

    difficulty_frame = tk.Frame(root) 
    difficulty_frame.pack(pady=10) 
    tk.Label(difficulty_frame, text="Select Difficulty", font=("Arial", 12)).pack() 
    difficulty_var = tk.StringVar(value="easy") 

    easy_button = tk.Radiobutton(difficulty_frame, text="Easy", variable=difficulty_var, value="easy", font=("Arial", 12)) 
    medium_button = tk.Radiobutton(difficulty_frame, text="Medium", variable=difficulty_var, value="medium", font=("Arial", 12)) 
    hard_button = tk.Radiobutton(difficulty_frame, text="Hard", variable=difficulty_var, value="hard", font=("Arial", 12)) 
    easy_button.pack() 
    medium_button.pack() 
    hard_button.pack() 

    sentence_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400, justify="center") 
    sentence_label.pack(pady=20) 

    typed_text_var = tk.StringVar() 
    typed_entry = tk.Entry(root, textvariable=typed_text_var, font=("Arial", 14), width=40) 
    typed_entry.pack(pady=20) 

    countdown_label = tk.Label(root, text="Time: 00:00", font=("Arial", 12)) 
    countdown_label.pack(pady=10) 

    results_label = tk.Label(root, text="", font=("Arial", 12)) 
    results_label.pack(pady=20) 

    start_button = tk.Button(root, text="Start Test", font=("Arial", 12), command=lambda: start_test(difficulty_var.get(), sentence_label, typed_text_var, start_button, end_button, results_label, countdown_label)) 
    start_button.pack(pady=10) 

    end_button = tk.Button(root, text="End Test", font=("Arial", 12), state="disabled") 
    end_button.pack(pady=10) 

    root.mainloop() 

setup_gui() 
