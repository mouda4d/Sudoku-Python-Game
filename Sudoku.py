import pygame
import numpy as np
import random
import time

# Initialize Pygame and font system
pygame.font.init()

# Constants
WINDOW_SIZE = 500  # Size of the game window
GRID_SIZE = 9  # Size of the Sudoku grid (9x9)
CELL_SIZE = WINDOW_SIZE // GRID_SIZE  # Size of each cell in the grid

# Define colors
BACKGROUND_COLOR = (50, 245, 50)  # Background color
HIGHLIGHT_COLOR = (255, 0, 0)  # Color for highlighting selected cell
FILLED_CELL_COLOR = (200, 250, 255)  # Color for filled cells
TEXT_COLOR = (0, 0, 0)  # Color for text
ERROR_COLOR = (255, 69, 58)  # Color for error messages
SOLVED_COLOR = (0, 0, 255)  # Color for solved message
TUTORIAL_COLOR = (240, 240, 240)  # Background color for tutorial screen
BUTTON_COLOR = (200, 200, 200)  # Color for buttons
BUTTON_HOVER_COLOR = (255, 0, 0)  # Color for hovered buttons

# Initialize game variables
selected_x, selected_y = 0, 0  # Coordinates of the selected cell
current_value = 0  # Current value of the selected cell
puzzle_grid = None  # The current Sudoku puzzle
puzzle_solution = None  # The solution to the current puzzle
auto_solving = False  # Flag for auto-solving mode
solved_displayed = False  # Flag to check if solved message is displayed

# Define fonts
font_large = pygame.font.SysFont("chiller", 50)  # Large font for numbers
font_small = pygame.font.SysFont("8-bit-operator.ttf", 20)  # Small font for messages

def init_window():
    """Initialize the Pygame window"""
    global window
    window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))  # Set window size
    pygame.display.set_caption("Sudoku by Mouda, press S to cheat  ^__^")  # Set window caption

def get_cell_coordinates(position):
    """Get the coordinates of the selected cell based on mouse position"""
    global selected_x, selected_y
    selected_x = position[0] // CELL_SIZE  # Calculate x coordinate of the cell
    selected_y = position[1] // CELL_SIZE  # Calculate y coordinate of the cell

def draw_highlight():
    """Draw a highlight around the selected cell"""
    pygame.draw.rect(window, HIGHLIGHT_COLOR, (selected_x * CELL_SIZE, selected_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def render_grid():
    """Render the Sudoku grid"""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if puzzle_grid[row][col] != 0:  # If the cell is filled
                pygame.draw.rect(window, FILLED_CELL_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE + 1, CELL_SIZE + 1))
                text = font_large.render(str(puzzle_grid[row][col]), True, TEXT_COLOR)  # Render the number
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))  # Center the number
                window.blit(text, text_rect.topleft)  # Draw the number
    for line in range(GRID_SIZE + 1):
        thickness = 3 if line % 3 == 0 else 1  # Thicker lines for subgrids
        pygame.draw.line(window, TEXT_COLOR, (0, line * CELL_SIZE), (WINDOW_SIZE, line * CELL_SIZE), thickness)  # Draw horizontal lines
        pygame.draw.line(window, TEXT_COLOR, (line * CELL_SIZE, 0), (line * CELL_SIZE, WINDOW_SIZE), thickness)  # Draw vertical lines

def display_number(number):
    """Display a number in the selected cell"""
    text = font_large.render(str(number), True, TEXT_COLOR)  # Render the number
    text_rect = text.get_rect(center=(selected_x * CELL_SIZE + CELL_SIZE // 2, selected_y * CELL_SIZE + CELL_SIZE // 2))  # Center the number
    window.blit(text, text_rect.topleft)  # Draw the number

def show_error_message(message):
    """Show an error message"""
    text = font_small.render(message, True, ERROR_COLOR)  # Render the error message
    window.blit(text, (20, WINDOW_SIZE - 30))  # Draw the error message

def show_solved_window():
    """Show the solved puzzle message"""
    solved_window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))  # Create a new window for the message
    pygame.display.set_caption("Puzzle Solved!")  # Set window caption
    solved_window.fill(BACKGROUND_COLOR)  # Fill the background color
    text = font_large.render("Puzzle Solved!", True, SOLVED_COLOR)  # Render the solved message
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))  # Center the message
    solved_window.blit(text, text_rect.topleft)  # Draw the message
    pygame.display.update()  # Update the display
    pygame.time.wait(3000)  # Wait for 3 seconds
    pygame.display.quit()  # Quit the display
    init_window()  # Reinitialize the main window

def show_tutorial():
    """Show the tutorial screen"""
    tutorial_window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))  # Create a new window for the tutorial
    tutorial_running = True  # Flag to keep the tutorial running
    while tutorial_running:
        tutorial_window.fill(TUTORIAL_COLOR)  # Fill the background color
        tutorial_text = [
            "Welcome to Sudoku!",
            "How to Play:",
            "1. Click on a cell to select it.",
            "2. Press number keys (1-9) to fill in the cell.",
            "3. The game will check if your move is valid.",
            "4. Press 'R' to generate a new puzzle.",
            "5. Press 'S' to solve the puzzle automatically.",
            "6. You can close this tutorial by pressing any key or clicking 'Close' below.",
            "",
            "Press any key or click 'Close' to start the game."
        ]

        y = 20  # Starting y position for the text
        for line in tutorial_text:
            text = font_small.render(line, True, TEXT_COLOR)  # Render each line of the tutorial
            tutorial_window.blit(text, (20, y))  # Draw each line of the tutorial
            y += 30  # Increment y position for the next line

        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        button_rect = pygame.Rect(WINDOW_SIZE - 120, WINDOW_SIZE - 50, 100, 40)  # Define the button rectangle
        if button_rect.collidepoint(mouse_x, mouse_y):  # Change color if mouse is over the button
            pygame.draw.rect(tutorial_window, BUTTON_HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(tutorial_window, BUTTON_COLOR, button_rect)
        button_text = font_small.render("Close", True, TEXT_COLOR)  # Render the button text
        button_text_rect = button_text.get_rect(center=button_rect.center)  # Center the button text
        tutorial_window.blit(button_text, button_text_rect.topleft)  # Draw the button text

        pygame.display.update()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user quits
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If the user clicks the button
                if button_rect.collidepoint(event.pos):
                    tutorial_running = False
            elif event.type == pygame.KEYDOWN:  # If the user presses any key
                tutorial_running = False

    pygame.display.quit()  # Quit the display
    init_window()  # Reinitialize the main window

def is_valid_move(grid, row, col, num):
    """Check if a move is valid"""
    if num in grid[row]:  # Check row
        return False
    if num in [grid[r][col] for r in range(GRID_SIZE)]:  # Check column
        return False
    sub_grid_row = (row // 3) * 3  # Calculate the starting row of the subgrid
    sub_grid_col = (col // 3) * 3  # Calculate the starting column of the subgrid
    for r in range(sub_grid_row, sub_grid_row + 3):
        for c in range(sub_grid_col, sub_grid_col + 3):
            if grid[r][c] == num:  # Check subgrid
                return False
    return True

def solve_sudoku(grid):
    """Solve the Sudoku puzzle"""
    def get_candidates(row, col):
        """Get the possible candidates for a cell"""
        candidates = set(range(1, GRID_SIZE + 1))
        candidates -= set(grid[row])  # Remove numbers already in the row
        candidates -= {grid[r][col] for r in range(GRID_SIZE)}  # Remove numbers already in the column
        sub_grid_row = (row // 3) * 3  # Calculate the starting row of the subgrid
        sub_grid_col = (col // 3) * 3  # Calculate the starting column of the subgrid
        candidates -= {grid[r][c] for r in range(sub_grid_row, sub_grid_row + 3)
                                    for c in range(sub_grid_col, sub_grid_col + 3)}  # Remove numbers already in the subgrid
        return candidates

    def select_cell():
        """Select the cell with the fewest candidates"""
        min_candidates = GRID_SIZE + 1
        best_cell = None
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:  # If the cell is empty
                    candidates = get_candidates(row, col)  # Get candidates
                    if len(candidates) < min_candidates:  # Update the best cell
                        min_candidates = len(candidates)
                        best_cell = (row, col)
        return best_cell

    empty = select_cell()  # Select the next cell to fill
    if not empty:
        return True  # If no empty cells, puzzle is solved

    row, col = empty
    candidates = get_candidates(row, col)  # Get candidates for the cell
    for num in candidates:
        grid[row][col] = num  # Try a candidate
        window.fill(BACKGROUND_COLOR)
        render_grid()
        draw_highlight()
        pygame.display.update()
        pygame.time.delay(50)  # Delay for visualization

        if solve_sudoku(grid):
            return True  # If puzzle is solved, return True

        grid[row][col] = 0  # Backtrack
        window.fill(BACKGROUND_COLOR)
        render_grid()
        draw_highlight()
        pygame.display.update()
        pygame.time.delay(50)  # Delay for visualization

    return False  # If no solution, return False

def generate_full_grid():
    """Generate a fully solved Sudoku grid"""
    def fill_grid(grid):
        """Recursively fill the grid"""
        def is_valid(row, col, num):
            return is_valid_move(grid, row, col, num)  # Check if move is valid

        def find_empty_cell():
            """Find an empty cell"""
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if grid[row][col] == 0:
                        return row, col
            return None

        empty_cell = find_empty_cell()  # Find the next empty cell
        if not empty_cell:
            return True  # If no empty cells, grid is filled

        row, col = empty_cell
        numbers = list(range(1, GRID_SIZE + 1))
        random.shuffle(numbers)  # Shuffle numbers for randomness
        for num in numbers:
            if is_valid(row, col, num):  # Try a number
                grid[row][col] = num
                if fill_grid(grid):
                    return True  # If grid is filled, return True
                grid[row][col] = 0  # Backtrack

        return False  # If no solution, return False

    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]  # Create an empty grid
    fill_grid(grid)  # Fill the grid
    return grid

def generate_puzzle(solution, num_clues=20):
    """Generate a Sudoku puzzle from a solution"""
    puzzle = [row[:] for row in solution]  # Copy the solution
    cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]  # Get all cell positions
    random.shuffle(cells)  # Shuffle cell positions
    for r, c in cells[num_clues:]:
        puzzle[r][c] = 0  # Remove numbers to create the puzzle
    return puzzle

def restart_game():
    """Restart the game with a new puzzle"""
    global puzzle_grid, puzzle_solution, auto_solving, solved_displayed
    puzzle_solution = generate_full_grid()  # Generate a new solution
    puzzle_grid = generate_puzzle(puzzle_solution)  # Generate a new puzzle
    auto_solving = False  # Reset auto-solving flag
    solved_displayed = False  # Reset the solved displayed flag

def main():
    """Main game loop"""
    global puzzle_grid, puzzle_solution, auto_solving, solved_displayed

    # Show tutorial before starting the game
    show_tutorial()

    # Initialize game state
    restart_game()

    running = True  # Flag to keep the game running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user quits
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # If the user presses ESC
                    running = False
                elif event.key == pygame.K_s:  # If the user presses S
                    auto_solving = not auto_solving  # Toggle auto-solving mode
                    if auto_solving:
                        if solve_sudoku(puzzle_grid) and not solved_displayed:  # If puzzle is solved and not displayed
                            solved_displayed = True  # Set solved displayed flag
                            show_solved_window()  # Show solved message
                        else:
                            show_error_message("Cannot solve puzzle.")  # Show error message
                elif event.key == pygame.K_r:  # If the user presses R
                    restart_game()  # Restart the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # Get mouse position
                get_cell_coordinates(pos)  # Get selected cell coordinates
                if auto_solving:
                    if solve_sudoku(puzzle_grid) and not solved_displayed:  # If puzzle is solved and not displayed
                        solved_displayed = True  # Set solved displayed flag
                        show_solved_window()  # Show solved message
                    else:
                        show_error_message("Cannot solve puzzle.")  # Show error message

        if auto_solving:
            if solve_sudoku(puzzle_grid) and not solved_displayed:  # If puzzle is solved and not displayed
                solved_displayed = True  # Set solved displayed flag
                show_solved_window()  # Show solved message
            else:
                show_error_message("Cannot solve puzzle.")  # Show error message

        window.fill(BACKGROUND_COLOR)  # Fill the background color
        render_grid()  # Render the grid
        draw_highlight()  # Draw the highlight
        pygame.display.update()  # Update the display

if __name__ == "__main__":
    init_window()  # Initialize the window
    main()  # Start the main game loop
