import customtkinter as ctk
import json
import subprocess
import sys
from datetime import datetime
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

class SearchEntry(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.query_label = ctk.CTkLabel(self, text="Search Query:")
        self.query_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.query = ctk.CTkEntry(self, width=400, placeholder_text="Enter search query...")
        self.query.grid(row=0, column=1, columnspan=3, padx=5, pady=2, sticky='ew')
        
        # Allow the query entry to expand when the window does
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
        self.posts_label = ctk.CTkLabel(self, text="Scroll Posts:")
        self.posts_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')
        self.scroll_posts = ctk.CTkEntry(self, width=100, placeholder_text="1")
        self.scroll_posts.grid(row=1, column=1, padx=5, pady=2, sticky='w')
        
        self.comments_label = ctk.CTkLabel(self, text="Scroll Comments:")
        self.comments_label.grid(row=1, column=2, padx=5, pady=2, sticky='w')
        self.scroll_comments = ctk.CTkEntry(self, width=100, placeholder_text="1")
        self.scroll_comments.grid(row=1, column=3, padx=5, pady=2, sticky='w')

        self.delete_btn = ctk.CTkButton(self, text="×", width=40, command=self.remove_search)
        self.delete_btn.grid(row=0, column=4, rowspan=2, padx=5, pady=2)

    def remove_search(self):
        self.destroy()

    def get_data(self):
        # Convert scroll values to integers with default value of 1
        try:
            scroll_posts = int(self.scroll_posts.get())
        except (ValueError, TypeError):
            scroll_posts = 1
            
        try:
            scroll_comments = int(self.scroll_comments.get())
        except (ValueError, TypeError):
            scroll_comments = 1
            
        return {
            "query": self.query.get(),
            "scroll_posts": scroll_posts,  # Store as integer
            "scroll_comments": scroll_comments  # Store as integer
        }

class CustomLogger:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.original_stdout = sys.stdout

    def write(self, text):
        self.text_widget.configure(state='normal')
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.text_widget.insert('end', f'[{timestamp}] {text}')
        self.text_widget.see('end')
        self.text_widget.configure(state='disabled')
        self.original_stdout.write(text)

    def flush(self):
        self.original_stdout.flush()

class ScraperGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Twitter Scraper Configuration")
        self.geometry("900x800")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)  

        # Credentials frame
        self.cred_frame = ctk.CTkFrame(self)
        self.cred_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        cred_title = ctk.CTkLabel(self.cred_frame, text="Credentials", font=ctk.CTkFont(size=16, weight="bold"))
        cred_title.pack(pady=5)

        self.email = ctk.CTkEntry(self.cred_frame, width=400, placeholder_text="Email")
        self.email.pack(padx=20, pady=5)

        self.username = ctk.CTkEntry(self.cred_frame, width=400, placeholder_text="Username")
        self.username.pack(padx=20, pady=5)

        self.password = ctk.CTkEntry(self.cred_frame, width=400, placeholder_text="Password", show="*")
        self.password.pack(padx=20, pady=5)

        cred_title2 = ctk.CTkLabel(self.cred_frame, text="Account 2 Credentials", font=ctk.CTkFont(size=16, weight="bold"))
        cred_title2.pack(pady=5)

        self.email2 = ctk.CTkEntry(self.cred_frame, width=400, placeholder_text="Email (Account 2)")
        self.email2.pack(padx=20, pady=5)

        self.username2 = ctk.CTkEntry(self.cred_frame, width=400, placeholder_text="Username (Account 2)")
        self.username2.pack(padx=20, pady=5)

        self.password2 = ctk.CTkEntry(self.cred_frame, width=400, placeholder_text="Password (Account 2)", show="*")
        self.password2.pack(padx=20, pady=5)

        # Searches frame
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        search_title = ctk.CTkLabel(self.search_frame, text="Searches", font=ctk.CTkFont(size=16, weight="bold"))
        search_title.pack(pady=5)

        self.searches_container = ScrollableFrame(self.search_frame, height=250)  
        self.searches_container.pack(fill="x", padx=10, expand=True)

        self.add_search_btn = ctk.CTkButton(
            self.search_frame, 
            text="Add Search", 
            command=self.add_search
        )
        self.add_search_btn.pack(pady=10)

        # Buttons frame
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.save_btn = ctk.CTkButton(
            self.btn_frame, 
            text="Save Configuration",
            command=self.save_config
        )
        self.save_btn.pack(side="left", padx=10)
        
        self.main_btn = ctk.CTkButton(
            self.btn_frame, 
            text="Execute main.py",
            command=lambda: self.execute_script("main.py")
        )
        self.main_btn.pack(side="left", padx=10)
        
        self.users_btn = ctk.CTkButton(
            self.btn_frame, 
            text="Execute usuarios.py",
            command=lambda: self.execute_script("usuarios.py")
        )
        self.users_btn.pack(side="left", padx=10)

        # Log frame
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=3, column=0, padx=20, pady=(10,20), sticky="nsew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)  
        
        log_title = ctk.CTkLabel(self.log_frame, text="Logs", font=ctk.CTkFont(size=16, weight="bold"))
        log_title.grid(row=0, column=0, pady=5)

        self.log_text = ctk.CTkTextbox(self.log_frame) 
        self.log_text.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        # Setup custom logger to capture output
        sys.stdout = CustomLogger(self.log_text)

        # Initialize searches list
        self.busquedas = []
        self.load_config()

    def add_search(self):
        search_entry = SearchEntry(self.searches_container)
        search_entry.pack(fill="x", pady=2)
        return search_entry

    def load_config(self):
        try:
            with open("config.json", "r", encoding="utf-8") as file:
                config = json.load(file)
                
                self.email.insert(0, config.get("mail", ""))
                self.username.insert(0, config.get("username", ""))
                self.password.insert(0, config.get("password", ""))

                self.email2.insert(0, config.get("mail2", ""))
                self.username2.insert(0, config.get("username2", ""))
                self.password2.insert(0, config.get("password2", ""))
                
                for busqueda in config.get("busquedas", []):
                    entry = self.add_search()
                    entry.query.insert(0, busqueda.get("query", ""))
                    
                    # Handle numeric values, ensuring they're displayed as strings in the entry fields
                    entry.scroll_posts.insert(0, str(busqueda.get("scroll_posts", 1)))
                    entry.scroll_comments.insert(0, str(busqueda.get("scroll_comments", 1)))
                
                self.busquedas = config.get("busquedas", [])
                print("Configuration loaded successfully.")
        except FileNotFoundError:
            print("No configuration file found. Starting with empty configuration.")
        except json.JSONDecodeError:
            print("Error parsing configuration file. Starting with empty configuration.")

    def save_config(self):
        config = {
            "username": self.username.get(),
            "mail": self.email.get(),
            "password": self.password.get(),
            "username2": self.username2.get(),
            "mail2": self.email2.get(),
            "password2": self.password2.get(),
            "busquedas": [search.get_data() for search in self.searches_container.winfo_children()]
        }
        
        with open("config.json", "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)
        
        print("Configuration saved successfully.")

    def execute_script(self, script_name):
        def run():
            try:
                print(f"Executing {script_name}...")
                subprocess.run([sys.executable, script_name], check=True)
                print(f"Finished executing {script_name}.")
            except subprocess.CalledProcessError as e:
                print(f"Error executing {script_name}: {e}")
            except FileNotFoundError:
                print(f"File not found: {script_name}")
        
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    app = ScraperGUI()
    app.mainloop()
