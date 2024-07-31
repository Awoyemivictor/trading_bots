import time
import customtkinter as ctk
from threading import Thread
import bot_logic


class ArbitrageBotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Arbitrage Bot")
        self.geometry("400x300")
        
        # Start Button
        self.start_button = ctk.CTkButton(self, text="Start Bot", command=self.start_bot)
        self.start_button.pack(pady=20)
        
        # Stop Button
        self.stop_button = ctk.CTkButton(self, text="Stop Bot", command=self.stop_bot)
        self.stop_button.pack(pady=20)
        
        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Status: Ready", width=120, height=25)
        self.status_label.pack(pady=20)
        
        # Variable to control the bot loop
        self.bot_running = False
        
    
    def start_bot(self):
        self.status_label.configure(text="Status: Running")
        self.bot_running = True
        self.bot_thread = Thread(target=self.run_bot)
        self.bot_thread.start()
        
    
    def stop_bot(self):
        self.status_label.configure(text="Status: Stopped")
        self.bot_running = False
        if self.bot_thread.is_alive():
            self.bot_thread.join()
            
    
    def run_bot(self):
        """Run the arbitrage checking in a loop."""
        symbol = 'BTCUSDT'  # Ensure the ticker is correct for both platforms
        while self.bot_running:
            try:
                # Insert call to your bot logic here
                message = bot_logic.check_artbitrage_opportunity(symbol)
                self.update_status(message)            
            except Exception as e:
                self.update_status(f"Error: {str(e)}")
            finally:
                time.sleep(60) # Sleep to respect API call limits and manage the update freequency
                
    
    def update_status(self, message):
        """Thread-safe update of the status label."""
        if self.winfo_exists(): # Check if the window still exists
            self.status_label.configure(text=message)
            

if __name__ == "__main__":
    app = ArbitrageBotGUI()
    app.mainloop()