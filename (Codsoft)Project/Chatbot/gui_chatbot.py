import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

def get_bot_response(user_input: str) -> str:
    text = user_input.lower().strip()

    if text in ["bye", "exit", "quit", "goodbye"]:
        return "Goodbye! It was nice talking to you. 👋"

    if any(word in text for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hello! 😊 How can I help you today?"

    if "how are you" in text:
        return "I'm just a bunch of Python code, but I'm feeling awesome! 😄 What about you?"

    if "your name" in text or "who are you" in text:
        return "I'm a simple rule-based chatbot built using Python and Tkinter."

    if "who created you" in text or "your creator" in text:
        return "I was created by a Python programmer as a mini chatbot project."

    if "time" in text:
        now = datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    if "date" in text or "today's date" in text:
        today = datetime.now().strftime("%d-%m-%Y")
        return f"Today's date is {today}."

    if "weather" in text:
        return "I can't fetch live weather yet, but I hope it's a pleasant day where you are! ☀️"

    if "thank you" in text or "thanks" in text:
        return "You're welcome! 😊 Happy to help."

    if "sorry" in text:
        return "It's okay, no worries at all. 💙"

    if "study" in text or "exam" in text or "exams" in text:
        return (
            "Stay consistent with your studies 📚. "
            "Make a timetable, revise daily, and take short breaks. You've got this! 💪"
        )

    if "programming" in text or "coding" in text or "python" in text:
        return (
            "Programming is fun! 🧑‍💻 Start with basics like variables, loops, and functions. "
            "Practice small projects like calculators, to-do apps, or chatbots like me!"
        )

    if "joke" in text:
        return "Why do programmers prefer dark mode? Because light attracts bugs! 🐞😂"

    if "help" in text:
        return (
            "Sure! I can chat about:\n"
            "- My name / who I am 🤖\n"
            "- Time and date ⏰📅\n"
            "- Study & exams 📚\n"
            "- Programming & coding 🧑‍💻\n"
            "- Jokes 😂\n"
            "Just type what you want to talk about!"
        )

    return (
        "I'm not sure how to respond to that yet. 🤔\n"
        "Try asking me about the time, date, studies, coding, or say 'help' to see options."
    )

def send_message(event=None):
    user_msg = user_input.get().strip()
    if not user_msg:
        return

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {user_msg}\n", "user")

    bot_msg = get_bot_response(user_msg)
    chat_area.insert(tk.END, f"Bot: {bot_msg}\n\n", "bot")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

    user_input.set("")

    if user_msg.lower().strip() in ["bye", "exit", "quit", "goodbye"]:
        root.after(1200, root.destroy)

root = tk.Tk()
root.title("Rule-Based Chatbot")
root.geometry("650x500")
root.minsize(450, 350)

root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

header = tk.Label(
    root,
    text="💬 Simple Rule-Based Chatbot",
    font=("Segoe UI", 14, "bold"),
    bg="#2c3e50",
    fg="white",
    pady=8
)
header.grid(row=0, column=0, sticky="ew")

chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    state=tk.DISABLED,
    font=("Segoe UI", 10)
)
chat_area.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

chat_area.tag_config("user", foreground="#0b63ce", font=("Segoe UI", 10, "bold"))
chat_area.tag_config("bot", foreground="#2c3e50", font=("Segoe UI", 10))
chat_area.tag_config("system", foreground="#7f8c8d", font=("Segoe UI", 9, "italic"))

input_frame = tk.Frame(root)
input_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

input_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=0)

user_input = tk.StringVar()
entry = tk.Entry(
    input_frame,
    textvariable=user_input,
    font=("Segoe UI", 10)
)
entry.grid(row=0, column=0, sticky="ew", ipady=4)
entry.bind("<Return>", send_message)

send_button = tk.Button(
    input_frame,
    text="Send",
    command=send_message,
    font=("Segoe UI", 10, "bold"),
    bg="#0b63ce",
    fg="white",
    padx=12,
    pady=4
)
send_button.grid(row=0, column=1, padx=(5, 0))

chat_area.config(state=tk.NORMAL)
chat_area.insert(
    tk.END,
    "Bot: Hello! I am your GUI chatbot. Type 'help' to see what I can do, or 'bye' to quit.\n\n",
    "bot"
)
chat_area.config(state=tk.DISABLED)

entry.focus()
root.mainloop()
