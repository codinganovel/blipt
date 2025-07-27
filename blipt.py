#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime
from typing import List, Optional

# Try to import optional dependencies
try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False
    print("⚠️  pyperclip not found - clipboard features disabled")

# ANSI color codes - work on all modern terminals
class Colors:
    """ANSI color codes for terminal styling."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Color palette
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    
    # Background colors
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"


def colored(text: str, color: str = "", style: str = "") -> str:
    """Return colored text with optional styling."""
    return f"{style}{color}{text}{Colors.RESET}"


def print_colored(text: str, color: str = "", style: str = "") -> None:
    """Print colored text with optional styling."""
    print(colored(text, color, style))


class Scratchpad:
    """A fast, disposable scratchpad for your terminal."""
    
    def __init__(self, history_file: str = "Scratchmd.md", max_notes: int = 100):
        self.notes: List[str] = []
        self.history_file = history_file
        self.max_notes = max_notes
        self.unsaved_notes: List[str] = []
        self.init_history()
    
    def init_history(self) -> None:
        """Ensure history file exists."""
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w", encoding="utf-8") as f:
                f.write("# Scratchpad History\n\n")
    
    def log_to_history(self, text: str) -> None:
        """Append to history file with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(f"- [{timestamp}] {text}\n")
        except IOError as e:
            self.show_error(f"Failed to write to history: {e}")
    
    def show_status(self, message: str, duration: float = 1.0) -> None:
        """Show a status message briefly."""
        print_colored(f"✓ {message}", Colors.CYAN)
        time.sleep(duration)
    
    def show_error(self, message: str, duration: float = 1.5) -> None:
        """Show an error message briefly."""
        print_colored(f"❌ {message}", Colors.RED)
        time.sleep(duration)
    
    def redraw(self) -> None:
        """Redraw the screen with current notes and improved UI."""
        os.system("cls" if os.name == "nt" else "clear")
        
        # Header with box drawing
        print_colored("┌─────────────────────────────────────────────────────────────┐", Colors.CYAN)
        print_colored("│                      📝 SCRATCHPAD                         │", Colors.BLUE, Colors.BOLD)
        print_colored("└─────────────────────────────────────────────────────────────┘", Colors.CYAN)
        print()
        
        # Notes display
        if not self.notes:
            print_colored("   📭 No notes yet. Type 'add <text>' to start!", Colors.CYAN, Colors.DIM)
        else:
            for i, note in enumerate(self.notes, 1):
                # For multiline notes, show only the first line
                first_line = note.split('\n')[0]
                
                # Truncate long notes for display but show full content is available
                if len(first_line) > 70:
                    display_note = first_line[:67] + "..."
                    truncated_indicator = " 📄+"
                else:
                    display_note = first_line
                    truncated_indicator = " 📄+" if '\n' in note else " 📄"
                
                # Alternate colors for better readability
                color = Colors.WHITE if i % 2 == 1 else Colors.CYAN
                print_colored(f"   {i:2d}.{truncated_indicator} {display_note}", color)
        
        print()
        
        # Status line
        note_count = len(self.notes)
        max_display = f"({note_count}/{self.max_notes})"
        clipboard_status = "📋 Clipboard: ON" if HAS_CLIPBOARD else "📋 Clipboard: OFF"
        
        print_colored("─" * 63, Colors.CYAN)
        print_colored(f"📊 Notes {max_display} | {clipboard_status}", Colors.BLUE, Colors.BOLD)
        print_colored("─" * 63, Colors.CYAN)
        
        # Commands help
        print_colored("💡 Commands:", Colors.BLUE, Colors.BOLD)
        commands = [
            "add <text>", "copy <n>", "copy all", 
            "delete <n>", "delete all", "search <term>", "exit"
        ]
        print_colored(f"   {' | '.join(commands)}", Colors.CYAN, Colors.DIM)
        print_colored("─" * 63, Colors.CYAN)
    
    def get_user_input(self) -> str:
        """Get user input with a nice prompt."""
        try:
            prompt = colored("📝 > ", Colors.CYAN, Colors.BOLD)
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print_colored("\n👋 Goodbye!", Colors.CYAN)
            return "exit"
    
    def safe_clipboard_copy(self, text: str) -> bool:
        """Safely copy to clipboard with fallback."""
        if not HAS_CLIPBOARD:
            self.show_error("Clipboard not available - install pyperclip")
            print(f"📋 Text content: {text}")
            return False
        
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            self.show_error(f"Copy failed: {e}")
            print(f"📋 Text content: {text}")
            return False
    
    def handle_add(self, text: str) -> None:
        """Add a new note to the scratchpad."""
        if not text:
            self.show_error("Cannot add empty text")
            return
        
        # Limit number of notes to prevent memory bloat
        if len(self.notes) >= self.max_notes:
            self.notes.pop(0)  # Remove oldest
            self.show_status(f"Removed oldest note (limit: {self.max_notes})", 0.5)
        
        self.notes.append(text)
        self.log_to_history(text)
        self.show_status(f"Added note #{len(self.notes)}", 0.5)
    
    def handle_copy(self, index: int) -> None:
        """Copy note at specified index to clipboard."""
        if index < 1 or index > len(self.notes):
            self.show_error("Invalid note number")
            return
        
        note_text = self.notes[index - 1]
        if self.safe_clipboard_copy(note_text):
            self.show_status(f"Copied note #{index}")
    
    def handle_copy_all(self) -> None:
        """Copy all notes to clipboard."""
        if not self.notes:
            self.show_error("Nothing to copy")
            return
        
        all_text = "\n".join(f"{i+1}. {note}" for i, note in enumerate(self.notes))
        if self.safe_clipboard_copy(all_text):
            self.show_status(f"Copied all {len(self.notes)} notes")
    
    def handle_delete(self, index: int) -> None:
        """Delete note at specified index."""
        if index < 1 or index > len(self.notes):
            self.show_error("Invalid note number")
            return
        
        deleted_note = self.notes.pop(index - 1)
        # Show preview of deleted note (truncated)
        preview = deleted_note[:30] + "..." if len(deleted_note) > 30 else deleted_note
        self.show_status(f"Deleted: '{preview}'", 0.8)
    
    def handle_delete_all(self) -> None:
        """Clear all notes after confirmation."""
        if not self.notes:
            self.show_error("Nothing to delete")
            return
        
        count = len(self.notes)
        self.notes.clear()
        self.show_status(f"Deleted all {count} notes")
    
    def handle_search(self, query: str) -> None:
        """Search notes and display matches."""
        if not query:
            self.show_error("Please provide a search term")
            return
        
        matches = []
        for i, note in enumerate(self.notes):
            if query.lower() in note.lower():
                matches.append((i + 1, note))
        
        if not matches:
            self.show_error(f"No notes found containing '{query}'")
            return
        
        # Display search results temporarily
        os.system("cls" if os.name == "nt" else "clear")
        print_colored(f"🔍 Search results for '{query}':", Colors.BLUE, Colors.BOLD)
        print_colored("─" * 50, Colors.CYAN)
        
        for index, note in matches:
            # Highlight the search term (simple bracket highlight)
            highlighted = note.replace(query, f"[{query}]")
            print_colored(f"   {index:2d}. 📄 {highlighted}", Colors.CYAN)
        
        print_colored("─" * 50, Colors.CYAN)
        print_colored(f"Found {len(matches)} match(es). Press Enter to continue...", Colors.BLUE)
        input()
    
    def parse_command(self, command: str) -> tuple:
        """Parse command into action and arguments."""
        if not command:
            return None, []
        
        parts = command.split(None, 1)  # Split on first whitespace only
        action = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        return action, args
    
    def run(self) -> None:
        """Main application loop."""
        print_colored("🚀 Welcome to Scratchpad! Type 'exit' to quit.", Colors.BLUE, Colors.BOLD)
        time.sleep(1)
        
        while True:
            self.redraw()
            command = self.get_user_input()
            
            if command.lower() == "exit":
                break
            elif command.lower() == "copy all":
                self.handle_copy_all()
            elif command.lower() == "delete all":
                self.handle_delete_all()
            elif command.startswith("add "):
                text = command[4:].strip()
                self.handle_add(text)
            elif command.startswith("copy "):
                arg = command[5:].strip()
                if arg.isdigit():
                    self.handle_copy(int(arg))
                else:
                    self.show_error("Usage: copy <number>")
            elif command.startswith("delete "):
                arg = command[7:].strip()
                if arg.isdigit():
                    self.handle_delete(int(arg))
                else:
                    self.show_error("Usage: delete <number>")
            elif command.startswith("search "):
                query = command[7:].strip()
                self.handle_search(query)
            elif command.lower() in ["help", "?"]:
                self.show_help()
            elif command:
                self.show_error("Unknown command. Type 'help' for available commands")
            # Empty command just redraws
    
    def show_help(self) -> None:
        """Display help information."""
        os.system("cls" if os.name == "nt" else "clear")
        print_colored("📚 BLIPT HELP", Colors.BLUE, Colors.BOLD)
        print_colored("═" * 50, Colors.CYAN)
        
        help_text = [
            ("add <text>", "Add a new note to your scratchpad"),
            ("copy <n>", "Copy note number N to clipboard"),
            ("copy all", "Copy all notes to clipboard"),
            ("delete <n>", "Delete note number N"),
            ("delete all", "Delete all notes"),
            ("search <term>", "Search for notes containing term"),
            ("help", "Show this help message"),
            ("exit", "Exit the application"),
        ]
        
        for cmd, desc in help_text:
            print_colored(f"  {cmd:12} - {desc}", Colors.CYAN)
        
        print_colored("═" * 50, Colors.CYAN)
        print_colored("💡 Tips:", Colors.BLUE, Colors.BOLD)
        print_colored("  • Notes are auto-saved to Scratchmd.md", Colors.CYAN)
        print_colored("  • Long notes are truncated in display but fully copied", Colors.CYAN)
        print_colored(f"  • Maximum {self.max_notes} notes in memory", Colors.CYAN)
        
        print_colored("\nPress Enter to continue...", Colors.BLUE)
        input()


def main():
    """Entry point for the application."""
    try:
        scratchpad = Scratchpad()
        scratchpad.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()