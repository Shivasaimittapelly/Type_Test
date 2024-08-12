import tkinter as tk
from tkinter import ttk
import random
import time

class TypingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Test")
        self.root.geometry("800x600")
        self.time_limit = 0
        self.start_time = 0
        self.is_running = False
        self.sentences = self.get_random_sentences()
        self.current_sentence_index = 0

        # Set background color
        self.root.configure(bg="#1E1E1E")

        # Fonts
        self.label_font = ("Helvetica", 14, "bold")
        self.text_font = ("Courier", 14)
        self.button_font = ("Helvetica", 12)

        # Time input label and entry
        self.time_label = tk.Label(root, text="Enter time (seconds):", font=self.label_font, bg="#1E1E1E", fg="#FFFFFF")
        self.time_label.pack(pady=10)
        self.time_entry = tk.Entry(root, font=self.text_font, width=10)
        self.time_entry.pack()
        self.time_entry.bind("<Return>", lambda event: self.start_test())  # Bind Enter key to start test

        # Sentence label
        self.sentence_label = tk.Label(root, text="", font=self.text_font, bg="#1E1E1E", fg="#FFFFFF", wraplength=700, justify="left")
        self.sentence_label.pack(pady=20)

        # Text area
        self.text_area = tk.Text(root, height=3, width=70, font=self.text_font, bg="#FFFFFF", fg="#000000")
        self.text_area.pack(pady=20)
        self.text_area.config(state=tk.DISABLED)  # Initially disabled
        self.text_area.bind("<KeyRelease>", self.check_typing)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=10)

        # Start button
        self.start_button = tk.Button(root, text="Start Test", font=self.button_font, command=self.start_test, bg="#4CAF50", fg="#FFFFFF")
        self.start_button.pack(side=tk.LEFT, padx=20)

        # Reset button
        self.reset_button = tk.Button(root, text="Reset", font=self.button_font, command=self.reset_test, bg="#F44336", fg="#FFFFFF")
        self.reset_button.pack(side=tk.RIGHT, padx=20)
        self.reset_button.config(state=tk.DISABLED)  # Initially disabled

        # Result label
        self.result_label = tk.Label(root, text="", font=self.label_font, bg="#1E1E1E", fg="#FFFFFF")
        self.result_label.pack(pady=20)

        # Real-time WPM label
        self.wpm_label = tk.Label(root, text="WPM: 0", font=self.label_font, bg="#1E1E1E", fg="#FFFFFF")
        self.wpm_label.pack()

    def get_random_sentences(self):
        sentences = [
            "The sun sets in the west and rises in the east.",
            "A quick brown fox jumps over the lazy dog.",
            "To be or not to be, that is the question.",
            "All that glitters is not gold.",
            "The only limit to our realization of tomorrow is our doubts of today.",
            "In the middle of difficulty lies opportunity.",
            "The journey of a thousand miles begins with a single step.",
            "It always seems impossible until it's done.",
            "Life is what happens when you're busy making other plans.",
            "The way to get started is to quit talking and begin doing.",
            "Don't watch the clock; do what it does. Keep going.",
            "Success is not the key to happiness. Happiness is the key to success.",
            "Action is the foundational key to all success.",
            "Your time is limited, so don't waste it living someone else's life.",
            "The best way to predict your future is to create it.",
            "The harder you work for something, the greater you'll feel when you achieve it.",
            "Don't stop when you're tired; stop when you're done.",
            "Dream bigger. Do bigger.",
            "Little things make big days.",
            "It's going to be hard, but hard does not mean impossible.",
            "Don't wait for opportunity. Create it.",
            "Sometimes later becomes never. Do it now.",
            "Great things never come from comfort zones.",
            "Dream it. Wish it. Do it.",
            "Success doesn't just find you. You have to go out and get it.",
            "The harder you work, the luckier you get.",
            "Do something today that your future self will thank you for.",
            "Push yourself, because no one else is going to do it for you.",
            "Don't be afraid to give up the good to go for the great.",
            "Great things take time."
        ]
        random.shuffle(sentences)
        return sentences[:random.randint(20, 30)]

    def start_test(self):
        try:
            self.time_limit = int(self.time_entry.get())
        except ValueError:
            self.result_label.config(text="Please enter a valid number.")
            return

        self.time_entry.config(state=tk.DISABLED)
        self.text_area.config(state=tk.NORMAL)  # Enable text area
        self.text_area.delete(1.0, tk.END)  # Clear text area
        self.text_area.focus_set()  # Focus on text area
        self.start_button.config(state=tk.DISABLED)  # Disable start button
        self.reset_button.config(state=tk.NORMAL)  # Enable reset button
        self.is_running = True

        # Start the timer
        self.start_time = time.time()
        self.progress["maximum"] = self.time_limit
        self.update_progress()
        self.root.after(self.time_limit * 1000, self.end_test)
        self.update_wpm()

        # Display the first sentence
        self.current_sentence_index = 0
        self.sentence_label.config(text=self.sentences[self.current_sentence_index])

    def check_typing(self, event):
        typed_text = self.text_area.get(1.0, tk.END).strip()
        correct_text = self.sentences[self.current_sentence_index]

        if typed_text == correct_text:
            self.text_area.delete(1.0, tk.END)
            self.current_sentence_index += 1

            if self.current_sentence_index < len(self.sentences):
                self.sentence_label.config(text=self.sentences[self.current_sentence_index])
            else:
                self.end_test()

    def update_progress(self):
        if not self.is_running:
            return
        elapsed_time = time.time() - self.start_time
        self.progress["value"] = elapsed_time
        if elapsed_time < self.time_limit:
            self.root.after(100, self.update_progress)

    def update_wpm(self):
        if not self.is_running:
            return
        typed_text = self.text_area.get(1.0, tk.END).strip()
        word_count = len(typed_text.split())
        time_spent = time.time() - self.start_time
        if time_spent > 0:
            wpm = word_count / (time_spent / 60)
            self.wpm_label.config(text=f"WPM: {wpm:.2f}")
        self.root.after(500, self.update_wpm)

    def end_test(self):
        self.is_running = False
        self.text_area.config(state=tk.DISABLED)  # Disable text area

        # Calculate WPM
        total_words = sum(len(sentence.split()) for sentence in self.sentences[:self.current_sentence_index])
        time_spent = time.time() - self.start_time
        wpm = total_words / (time_spent / 60)

        # Display result
        self.result_label.config(text=f"Time's up! You typed {total_words} words. Your speed is {wpm:.2f} WPM.")

        # Re-enable start button and time entry for another test
        self.start_button.config(state=tk.NORMAL)
        self.time_entry.config(state=tk.NORMAL)

    def reset_test(self):
        self.is_running = False
        self.text_area.config(state=tk.DISABLED)  # Disable text area
        self.text_area.delete(1.0, tk.END)  # Clear text area
        self.result_label.config(text="")
        self.wpm_label.config(text="WPM: 0")
        self.progress["value"] = 0
        self.time_entry.config(state=tk.NORMAL)  # Enable time entry
        self.start_button.config(state=tk.NORMAL)  # Enable start button
        self.reset_button.config(state=tk.DISABLED)  # Disable reset button
        self.sentences = self.get_random_sentences()  # Get new random sentences
        self.sentence_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTest(root)
    root.mainloop()
