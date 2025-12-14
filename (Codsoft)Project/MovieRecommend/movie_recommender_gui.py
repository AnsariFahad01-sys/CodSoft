import tkinter as tk
from tkinter import ttk, messagebox
import math

# ====== Sample movie database ======
movies = [
    {"id": 1, "title": "The Matrix",               "genres": ["Action", "Sci-Fi"]},
    {"id": 2, "title": "Inception",                "genres": ["Action", "Sci-Fi", "Thriller"]},
    {"id": 3, "title": "Titanic",                  "genres": ["Romance", "Drama"]},
    {"id": 4, "title": "The Notebook",             "genres": ["Romance", "Drama"]},
    {"id": 5, "title": "John Wick",                "genres": ["Action", "Thriller"]},
    {"id": 6, "title": "Interstellar",             "genres": ["Sci-Fi", "Drama"]},
    {"id": 7, "title": "Avengers: Endgame",        "genres": ["Action", "Sci-Fi", "Adventure"]},
    {"id": 8, "title": "La La Land",               "genres": ["Romance", "Drama", "Music"]},
    {"id": 9, "title": "The Conjuring",            "genres": ["Horror", "Thriller"]},
    {"id": 10,"title": "The Shawshank Redemption", "genres": ["Drama"]},
]

title_to_movie = {m["title"]: m for m in movies}

# ====== Collaborative filtering: sample user rating data ======
# Ratings out of 5
sample_ratings = {
    "User1": {
        "The Matrix": 5, "Inception": 4, "Titanic": 1, "John Wick": 5,
        "Interstellar": 5, "Avengers: Endgame": 4
    },
    "User2": {
        "Titanic": 5, "The Notebook": 4, "La La Land": 5, "The Shawshank Redemption": 5
    },
    "User3": {
        "The Matrix": 4, "Inception": 5, "Avengers: Endgame": 5, "The Conjuring": 3
    },
    "User4": {
        "John Wick": 4, "The Conjuring": 4, "Inception": 4, "Interstellar": 4
    },
}


# ====== Content-based recommendation logic ======
def score_movie_content(movie, liked_genres):
    movie_genres = set(movie["genres"])
    return len(movie_genres.intersection(liked_genres))


def recommend_movies_content(liked_genres, top_n=5):
    scored = []
    for movie in movies:
        s = score_movie_content(movie, liked_genres)
        if s > 0:
            scored.append((movie, s))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]


# ====== Collaborative filtering logic (user-based) ======
def cosine_similarity(r1, r2):
    """Compute cosine similarity between two rating dicts keyed by movie title."""
    common = set(r1.keys()).intersection(r2.keys())
    if not common:
        return 0.0
    num = sum(r1[m] * r2[m] for m in common)
    sum1 = math.sqrt(sum(r1[m] ** 2 for m in common))
    sum2 = math.sqrt(sum(r2[m] ** 2 for m in common))
    if sum1 == 0 or sum2 == 0:
        return 0.0
    return num / (sum1 * sum2)


def recommend_movies_collab(user_ratings, top_n=5):
    """Simple user-based collaborative filtering."""
    # Compute similarity of current user to every sample user
    sims = {}
    for uname, ur in sample_ratings.items():
        sim = cosine_similarity(user_ratings, ur)
        if sim > 0:
            sims[uname] = sim

    if not sims:
        return []

    # Predict rating for each movie user hasn't rated
    totals = {}
    sim_sums = {}

    for uname, sim in sims.items():
        for movie_title, rating in sample_ratings[uname].items():
            if movie_title in user_ratings:
                continue  # skip if already rated by user
            totals.setdefault(movie_title, 0.0)
            sim_sums.setdefault(movie_title, 0.0)
            totals[movie_title] += sim * rating
            sim_sums[movie_title] += sim

    predictions = []
    for movie_title in totals:
        if sim_sums[movie_title] > 0:
            pred_rating = totals[movie_title] / sim_sums[movie_title]
            if movie_title in title_to_movie:
                predictions.append((title_to_movie[movie_title], pred_rating))

    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:top_n]


# ====== GUI Application ======
class MovieRecommenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Movie Recommendation System")
        self.root.geometry("900x550")
        self.root.configure(bg="#0b1020")  # dark background

        # Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#111827",
                        foreground="#e5e7eb",
                        fieldbackground="#111827",
                        rowheight=22)
        style.map("Treeview",
                  background=[("selected", "#10b981")])
        style.configure("TNotebook", background="#0b1020", borderwidth=0)
        style.configure("TNotebook.Tab",
                        background="#111827",
                        foreground="#e5e7eb",
                        padding=(10, 5))
        style.map("TNotebook.Tab",
                  background=[("selected", "#10b981")])

        # Title label
        title_label = tk.Label(
            root,
            text="🎬 Advanced Movie Recommendation System",
            bg="#0b1020",
            fg="#f9fafb",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(pady=10)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.content_frame = tk.Frame(self.notebook, bg="#0b1020")
        self.collab_frame = tk.Frame(self.notebook, bg="#0b1020")

        self.notebook.add(self.content_frame, text="Content-Based")
        self.notebook.add(self.collab_frame, text="Collaborative Filtering")

        # Keep last content-based results for search
        self.cb_results = []

        self.build_content_tab()
        self.build_collab_tab()

    # ====== Content-based tab ======
    def build_content_tab(self):
        frame = self.content_frame

        # Left: Genres + Top N + Buttons
        left = tk.Frame(frame, bg="#0b1020")
        left.pack(side="left", fill="y", padx=(10, 5), pady=10)

        tk.Label(
            left,
            text="Content-Based Filtering",
            bg="#0b1020",
            fg="#a5b4fc",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            left,
            text="Select genres you like:",
            bg="#0b1020",
            fg="#e5e7eb",
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        # Genres
        all_genres = set()
        for m in movies:
            all_genres.update(m["genres"])
        self.cb_genres = sorted(list(all_genres))
        self.cb_genre_vars = {}

        genre_frame = tk.Frame(left, bg="#0b1020")
        genre_frame.pack(anchor="w", pady=5)

        for idx, g in enumerate(self.cb_genres):
            var = tk.IntVar()
            cb = tk.Checkbutton(
                genre_frame,
                text=g,
                variable=var,
                bg="#0b1020",
                fg="#e5e7eb",
                selectcolor="#1f2937",
                activebackground="#0b1020",
                font=("Segoe UI", 9)
            )
            cb.grid(row=idx // 2, column=idx % 2, sticky="w", padx=2, pady=1)
            self.cb_genre_vars[g] = var

        # Top N dropdown
        top_frame = tk.Frame(left, bg="#0b1020")
        top_frame.pack(anchor="w", pady=(10, 3))

        tk.Label(
            top_frame,
            text="Top N results:",
            bg="#0b1020",
            fg="#e5e7eb",
            font=("Segoe UI", 9)
        ).grid(row=0, column=0, sticky="w")

        self.cb_top_n = ttk.Combobox(
            top_frame,
            values=["3", "5", "10"],
            state="readonly",
            width=5
        )
        self.cb_top_n.set("5")
        self.cb_top_n.grid(row=0, column=1, padx=5)

        # Buttons
        btn_frame = tk.Frame(left, bg="#0b1020")
        btn_frame.pack(anchor="w", pady=(10, 5))

        tk.Button(
            btn_frame,
            text="Get Recommendations",
            bg="#10b981",
            fg="#0b1020",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=8, pady=4,
            command=self.cb_get_recommendations
        ).grid(row=0, column=0, padx=3)

        tk.Button(
            btn_frame,
            text="Clear",
            bg="#374151",
            fg="#e5e7eb",
            font=("Segoe UI", 9),
            relief="flat",
            padx=8, pady=4,
            command=self.cb_clear
        ).grid(row=0, column=1, padx=3)

        # Search bar
        search_frame = tk.Frame(left, bg="#0b1020")
        search_frame.pack(anchor="w", pady=(15, 0))

        tk.Label(
            search_frame,
            text="Search in results:",
            bg="#0b1020",
            fg="#e5e7eb",
            font=("Segoe UI", 9)
        ).grid(row=0, column=0)

        self.cb_search_var = tk.StringVar()
        tk.Entry(
            search_frame,
            textvariable=self.cb_search_var,
            width=18,
            bg="#111827",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            relief="flat",
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            search_frame,
            text="Search",
            bg="#2563eb",
            fg="#e5e7eb",
            font=("Segoe UI", 9),
            relief="flat",
            padx=6, pady=2,
            command=self.cb_search
        ).grid(row=0, column=2)

        # Right: Table
        right = tk.Frame(frame, bg="#0b1020")
        right.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        columns = ("title", "genres", "score")
        self.cb_table = ttk.Treeview(right, columns=columns, show="headings")

        self.cb_table.heading("title", text="Movie Title")
        self.cb_table.heading("genres", text="Genres")
        self.cb_table.heading("score", text="Match Score")

        self.cb_table.column("title", width=220)
        self.cb_table.column("genres", width=250)
        self.cb_table.column("score", width=90, anchor="center")

        self.cb_table.pack(fill="both", expand=True)

    def cb_get_recommendations(self):
        liked_genres = {g for g, v in self.cb_genre_vars.items() if v.get() == 1}
        if not liked_genres:
            messagebox.showinfo("No genres", "Please select at least one genre.")
            return

        try:
            top_n = int(self.cb_top_n.get())
        except ValueError:
            top_n = 5

        self.cb_results = recommend_movies_content(liked_genres, top_n=top_n)
        self.cb_refresh_table(self.cb_results)

    def cb_refresh_table(self, results):
        for item in self.cb_table.get_children():
            self.cb_table.delete(item)

        for movie, score in results:
            self.cb_table.insert(
                "",
                tk.END,
                values=(movie["title"], ", ".join(movie["genres"]), score)
            )

    def cb_clear(self):
        for v in self.cb_genre_vars.values():
            v.set(0)
        self.cb_results = []
        for item in self.cb_table.get_children():
            self.cb_table.delete(item)
        self.cb_search_var.set("")

    def cb_search(self):
        query = self.cb_search_var.get().strip().lower()
        if not self.cb_results:
            return
        if not query:
            # show all
            self.cb_refresh_table(self.cb_results)
            return

        filtered = []
        for movie, score in self.cb_results:
            if query in movie["title"].lower():
                filtered.append((movie, score))
        self.cb_refresh_table(filtered)

    # ====== Collaborative Filtering tab ======
    def build_collab_tab(self):
        frame = self.collab_frame

        top = tk.Frame(frame, bg="#0b1020")
        top.pack(fill="x", padx=10, pady=10)

        tk.Label(
            top,
            text="Collaborative Filtering (User-Based)",
            bg="#0b1020",
            fg="#a5b4fc",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            top,
            text="Rate some movies (1–5), then click 'Recommend from Ratings'.",
            bg="#0b1020",
            fg="#e5e7eb",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(3, 0))

        # Middle: ratings input + top N
        mid = tk.Frame(frame, bg="#0b1020")
        mid.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Left: rating inputs
        rate_frame = tk.Frame(mid, bg="#0b1020")
        rate_frame.pack(side="left", fill="y")

        tk.Label(
            rate_frame,
            text="Your Ratings:",
            bg="#0b1020",
            fg="#e5e7eb",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        self.rating_vars = {}
        for idx, m in enumerate(movies, start=1):
            tk.Label(
                rate_frame,
                text=m["title"],
                bg="#0b1020",
                fg="#e5e7eb",
                font=("Segoe UI", 9)
            ).grid(row=idx, column=0, sticky="w", pady=1)

            var = tk.StringVar()
            cb = ttk.Combobox(
                rate_frame,
                textvariable=var,
                values=["", "1", "2", "3", "4", "5"],
                width=3,
                state="readonly"
            )
            cb.grid(row=idx, column=1, padx=5)
            self.rating_vars[m["title"]] = var

        # Right: recommendations table
        right = tk.Frame(mid, bg="#0b1020")
        right.pack(side="left", fill="both", expand=True, padx=(15, 0))

        # Top N dropdown + button
        ctrl = tk.Frame(right, bg="#0b1020")
        ctrl.pack(anchor="e", pady=(0, 5), fill="x")

        tk.Label(
            ctrl,
            text="Top N:",
            bg="#0b1020",
            fg="#e5e7eb",
            font=("Segoe UI", 9)
        ).pack(side="left", padx=(0, 5))

        self.collab_top_n = ttk.Combobox(
            ctrl,
            values=["3", "5", "10"],
            state="readonly",
            width=5
        )
        self.collab_top_n.set("5")
        self.collab_top_n.pack(side="left")

        tk.Button(
            ctrl,
            text="Recommend from Ratings",
            bg="#10b981",
            fg="#0b1020",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=8, pady=3,
            command=self.collab_get_recommendations
        ).pack(side="right", padx=(5, 0))

        # Table
        columns = ("title", "genres", "pred")
        self.collab_table = ttk.Treeview(right, columns=columns, show="headings")

        self.collab_table.heading("title", text="Movie Title")
        self.collab_table.heading("genres", text="Genres")
        self.collab_table.heading("pred", text="Predicted Rating")

        self.collab_table.column("title", width=230)
        self.collab_table.column("genres", width=260)
        self.collab_table.column("pred", width=120, anchor="center")

        self.collab_table.pack(fill="both", expand=True)

    def collab_get_recommendations(self):
        # Collect user ratings
        user_ratings = {}
        for title, var in self.rating_vars.items():
            val = var.get().strip()
            if val:
                try:
                    user_ratings[title] = int(val)
                except ValueError:
                    pass

        if not user_ratings:
            messagebox.showinfo("No ratings", "Please rate at least one movie (1–5).")
            return

        try:
            top_n = int(self.collab_top_n.get())
        except ValueError:
            top_n = 5

        results = recommend_movies_collab(user_ratings, top_n=top_n)

        for item in self.collab_table.get_children():
            self.collab_table.delete(item)

        if not results:
            messagebox.showinfo("No recommendations", "Not enough data to recommend. Try rating different movies.")
            return

        for movie, pred in results:
            self.collab_table.insert(
                "",
                tk.END,
                values=(
                    movie["title"],
                    ", ".join(movie["genres"]),
                    f"{pred:.2f}"
                )
            )


# ====== Run app ======
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRecommenderGUI(root)
    root.mainloop()
