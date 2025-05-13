import os

class KaomojiUI:
    def __init__(self):
        self.buttons = [["Attack", "Item"], ["Defend", "Run"]]
        self.rows = len(self.buttons)
        self.cols = len(self.buttons[0])
        self.selected_row = 0
        self.selected_col = 0
        self.running = True

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_menu(self):
        self.clear()
        print("\n🕹️  Choose an action:\n")
        for r in range(self.rows):
            row_display = []
            for c in range(self.cols):
                prefix = "웃" if (r == self.selected_row and c == self.selected_col) else "⬛"
                row_display.append(f"{prefix} {self.buttons[r][c]}")
            print("   ".join(row_display))
        print("\nUse W, A, S, D to move. Press E to select. Press Q to quit.")

    def update_selection(self, key):
        if key == "w" and self.selected_row > 0:
            self.selected_row -= 1
        elif key == "s" and self.selected_row < self.rows - 1:
            self.selected_row += 1
        elif key == "a" and self.selected_col > 0:
            self.selected_col -= 1
        elif key == "d" and self.selected_col < self.cols - 1:
            self.selected_col += 1
        elif key == "e":
            self.clear()
            print(f"\n✅ You selected: {self.buttons[self.selected_row][self.selected_col]}")
            input("\nPress Enter to return to the menu...")
        elif key == "q":
            self.running = False

    def run(self):
        while self.running:
            self.draw_menu()
            move = input(">").lower()
            self.update_selection(move)

KaomojiUI()