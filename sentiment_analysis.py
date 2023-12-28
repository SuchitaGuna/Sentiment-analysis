import tkinter as tk
from tkinter import messagebox, filedialog, Menu
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import movie_reviews

nltk.download('vader_lexicon')
nltk.download('movie_reviews')

def analyze_sentiment():
    global sia
    sia = SentimentIntensityAnalyzer()
    input_text = text.get('1.0', tk.END)
    sentiment_value = analyze_movie_reviews(input_text)
    result = "Sentiment Analysis Result: " + sentiment_value
    messagebox.showinfo('Sentiment Analysis Result', result)

def analyze_movie_reviews(text):
    words = nltk.word_tokenize(text)
    relevant_words = [word.lower() for word in words]

    if not relevant_words:
        return '⭐️⭐️ Okay'  # Neutral sentiment for no relevant words

    # Check for specific negative phrases
    negative_phrases = ['not good', 'not great', 'not enjoyable', 'not loved it', 'hated it', 'did not like it', 'hate', 'terrible']
    has_negative_phrase = any(phrase in text.lower() for phrase in negative_phrases)

    # Calculate the ratio of positive and negative words
    positive_words = [word for word in relevant_words if sia.polarity_scores(word)['compound'] > 0]
    negative_words = [word for word in relevant_words if sia.polarity_scores(word)['compound'] < 0]
    positive_ratio = len(positive_words) / len(relevant_words)
    negative_ratio = len(negative_words) / len(relevant_words)

    # Adjusted thresholds
    positive_threshold = 0.1
    negative_threshold = 0.1

    if has_negative_phrase or (positive_ratio > positive_threshold and negative_ratio > negative_threshold):
        return '⭐️ Not Good' if negative_ratio > 0.2 else \
               '⭐️ Terrible' if 'hated it' or 'terrible' in text.lower() else \
               '⭐️⭐️ Okay'
    elif 0.4 <= positive_ratio <= 0.6:  # Neutral if positive and negative ratios are balanced
        return '⭐️⭐️ Okay'
    else:
        return '⭐️⭐️⭐️⭐️⭐️ Loved It' if positive_ratio > 0.2 else \
               '⭐️⭐️⭐️⭐️ Great' if positive_ratio > 0.1 else \
               '⭐️⭐️⭐️ Good' if negative_ratio > 0.1 else \
               '⭐️⭐️ Okay'

def open_file():
    file_path = filedialog.askopenfilename(title='Open Text File', filetypes=[('Text Files', '*.txt')])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text.delete('1.0', tk.END)
            text.insert(tk.END, content)

def save_text():
    text_content = text.get('1.0', tk.END)
    file = filedialog.asksaveasfile(mode='w')
    if file:
        file.write(text_content)
        file.close()

def exit_program():
    answer = messagebox.askyesno('Exit', 'Do you want to exit the application?')
    if answer:
        window.destroy()

def about_us():
    messagebox.showinfo('About Us', 'This application is created for sentimental analysis using the Movie Reviews dataset.')

window = tk.Tk()
window.title('Sentimental Analysis App')

# Add widgets
text = tk.Text(window, wrap='word', height=10, width=40)
text.pack(expand=True, fill='both', padx=10, pady=10)

button = tk.Button(window, text='Analyze Sentiment', command=analyze_sentiment)
button.pack()

menubar = Menu(window)

# Add File Menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Open', command=open_file)
filemenu.add_command(label='Save', command=save_text)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=exit_program)
menubar.add_cascade(label='File', menu=filemenu)

# Add Help Menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label='About', command=about_us)
menubar.add_cascade(label='Help', menu=helpmenu)

window.config(menu=menubar)

# Start the main loop
window.mainloop()
