import pygame
import numpy as np

# Initialize Pygame and font system
pygame.font.init()  # Initialize the Pygame font system to use fonts

# Set up display
WINDOW_SIZE = 500  # Define the size of the window
GRID_SIZE = 9      # Define the size of the Sudoku grid (9x9)
CELL_SIZE = WINDOW_SIZE // GRID_SIZE  # Calculate the size of each cell in the grid
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))  # Create the game window with the defined size
pygame.display.set_caption("Sudoku")  # Set the title of the window

# Define colors
BACKGROUND_COLOR = (240, 255, 240)  # Light green color for the background
HIGHLIGHT_COLOR = (255, 0, 0)       # Red color to highlight the selected cell
FILLED_CELL_COLOR = (220, 220, 255) # Light blue color for cells with numbers
TEXT_COLOR = (0, 0, 0)              # Black color for text
ERROR_COLOR = (255, 0, 0)           # Red color for error messages
SOLVED_COLOR = (0, 128, 0)          # Dark green color for the completion message
TUTORIAL_COLOR = (200, 200, 200)    # Light gray color for the tutorial screen
BUTTON_COLOR = (150, 150, 150)      # Gray color for the close button
BUTTON_HOVER_COLOR = (100, 100, 100) # Darker gray color for the close button when hovered

# Initialize game variables
selected_x, selected_y = 0, 0  # Coordinates of the currently selected cell
current_value = 0              # The number currently selected to place in a cell
puzzle_grid = None             # The Sudoku puzzle grid

# Define fonts
font_large = pygame.font.SysFont("arial", 40)  # Font for large text (numbers, completion message)
font_small = pygame.font.SysFont("arial", 20)  # Font for small text (error messages, tutorial text)

auto_solving = False  # Flag to determine if the puzzle is being solved automatically

def get_cell_coordinates(position):
    """Calculate and set the coordinates of the cell based on mouse position."""
    global selected_x, selected_y
    selected_x = position[0] // CELL_SIZE  # Calculate column index
    selected_y = position[1] // CELL_SIZE  # Calculate row index

def draw_highlight():
    """Draw a highlight around the currently selected cell."""
    pygame.draw.rect(window, HIGHLIGHT_COLOR, (selected_x * CELL_SIZE, selected_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def render_grid():
    """Render the Sudoku grid and filled cells."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if puzzle_grid[row][col] != 0:  # Check if cell is filled
                pygame.draw.rect(window, FILLED_CELL_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE + 1, CELL_SIZE + 1))  # Draw filled cell background
                text = font_large.render(str(puzzle_grid[row][col]), True, TEXT_COLOR)  # Render the number
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))  # Center text in cell
                window.blit(text, text_rect.topleft)  # Draw number on the window
    # Draw grid lines
    for line in range(GRID_SIZE + 1):
        thickness = 3 if line % 3 == 0 else 1  # Thicker lines for the 3x3 sub-grid boundaries
        pygame.draw.line(window, TEXT_COLOR, (0, line * CELL_SIZE), (WINDOW_SIZE, line * CELL_SIZE), thickness)  # Draw horizontal lines
        pygame.draw.line(window, TEXT_COLOR, (line * CELL_SIZE, 0), (line * CELL_SIZE, WINDOW_SIZE), thickness)  # Draw vertical lines

def display_number(number):
    """Display the number at the selected cell."""
    text = font_large.render(str(number), True, TEXT_COLOR)  # Render the number
    text_rect = text.get_rect(center=(selected_x * CELL_SIZE + CELL_SIZE // 2, selected_y * CELL_SIZE + CELL_SIZE // 2))  # Center text in the cell
    window.blit(text, text_rect.topleft)  # Draw number on the window

def show_error_message(message):
    """Display an error message on the screen."""
    text = font_small.render(message, True, ERROR_COLOR)  # Render the error message
    window.blit(text, (20, WINDOW_SIZE - 30))  # Draw the message at the bottom left of the window

def is_valid_move(grid, row, col, num):
    """Check if placing num in the cell at (row, col) is valid according to Sudoku rules."""
    if num in grid[row]:  # Check if the number is already in the same row
        return False
    for r in range(GRID_SIZE):
        if grid[r][col] == num:  # Check if the number is already in the same column
            return False
    # Check 3x3 sub-grid
    sub_grid_row = (row // 3) * 3
    sub_grid_col = (col // 3) * 3
    for r in range(sub_grid_row, sub_grid_row + 3):
        for c in range(sub_grid_col, sub_grid_col + 3):
            if grid[r][c] == num:  # Check if the number is already in the 3x3 sub-grid
                return False
    return True

def solve_sudoku(grid):
    """Solve the Sudoku puzzle using a backtracking algorithm."""
    def get_candidates(row, col):
        """Get a set of possible candidates for the cell at (row, col)."""
        candidates = set(range(1, GRID_SIZE + 1))  # Possible numbers (1 to 9)
        candidates -= set(grid[row])  # Remove numbers already in the row
        candidates -= {grid[r][col] for r in range(GRID_SIZE)}  # Remove numbers already in the column
        # Remove numbers in the 3x3 sub-grid
        sub_grid_row = (row // 3) * 3
        sub_grid_col = (col // 3) * 3
        candidates -= {grid[r][c] for r in range(sub_grid_row, sub_grid_row + 3)
                                    for c in range(sub_grid_col, sub_grid_col + 3)}
        return candidates

    def select_cell():
        """Select the cell with the fewest candidates."""
        min_candidates = GRID_SIZE + 1  # Start with a number larger than the maximum possible candidates
        best_cell = None
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:  # Only consider empty cells
                    candidates = get_candidates(row, col)
                    if len(candidates) < min_candidates:  # Select cell with the fewest candidates
                        min_candidates = len(candidates)
                        best_cell = (row, col)
        return best_cell

    empty = select_cell()  # Get the next cell to fill
    if not empty:
        return True  # Puzzle solved if no empty cells are found

    row, col = empty
    candidates = get_candidates(row, col)
    for num in candidates:
        grid[row][col] = num
        window.fill(BACKGROUND_COLOR)  # Clear the window
        render_grid()  # Render the grid with the current number
        draw_highlight()  # Highlight the selected cell
        pygame.display.update()  # Update the display
        pygame.time.delay(50)  # Delay to make solving process visible

        if solve_sudoku(grid):  # Recursive call to continue solving
            return True

        grid[row][col] = 0  # Backtrack if the solution is not found
        window.fill(BACKGROUND_COLOR)  # Clear the window
        render_grid()  # Render the grid again without the last number
        draw_highlight()  # Highlight the selected cell
        pygame.display.update()  # Update the display
        pygame.time.delay(50)  # Delay to make backtracking visible

    return False

def display_completion_message():
    """Display a completion message when the puzzle is solved."""
    window.fill(BACKGROUND_COLOR)  # Ensure the message is visible by refreshing the background
    text = font_large.render("Puzzle Solved!", True, SOLVED_COLOR)  # Render the completion message
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))  # Center the message in the window
    window.blit(text, text_rect.topleft)  # Draw the message on the window
    pygame.display.update()  # Update the display
    pygame.time.wait(2000)  # Wait for 2 seconds to show the completion message

def generate_simple_puzzle():
    """Generate a simple Sudoku puzzle."""
    return [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],  # Puzzle rows with some cells filled and some empty
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

def show_tutorial():
    """Display a tutorial window explaining how to play the game."""
    tutorial_running = True
    while tutorial_running:
        window.fill(TUTORIAL_COLOR)  # Set a background color for the tutorial screen
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
        
        y = 20  # Start y position for tutorial text
        for line in tutorial_text:
            text = font_small.render(line, True, TEXT_COLOR)  # Render each line of the tutorial text
            window.blit(text, (20, y))  # Draw the text on the window
            y += 30  # Move y position for the next line

        # Close Button
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get the mouse position
        button_rect = pygame.Rect(WINDOW_SIZE - 120, WINDOW_SIZE - 50, 100, 40)  # Define the close button rectangle
        if button_rect.collidepoint(mouse_x, mouse_y):  # Check if mouse is hovering over the button
            pygame.draw.rect(window, BUTTON_HOVER_COLOR, button_rect)  # Draw button in hover color
        else:
            pygame.draw.rect(window, BUTTON_COLOR, button_rect)  # Draw button in default color
        button_text = font_small.render("Close", True, TEXT_COLOR)  # Render the button text
        button_text_rect = button_text.get_rect(center=button_rect.center)  # Center the text in the button
        window.blit(button_text, button_text_rect.topleft)  # Draw the button text on the button
        
        pygame.display.update()  # Update the display to show the tutorial window
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the user closes the window
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Check if the user clicks the mouse
                if button_rect.collidepoint(event.pos):  # Check if the click is on the close button
                    tutorial_running = False
            elif event.type == pygame.KEYDOWN:  # Check if a key is pressed
                tutorial_running = False

def main():
    """Main game loop."""
    global puzzle_grid, current_value, auto_solving
    show_tutorial()  # Show tutorial before starting the game
    puzzle_grid = generate_simple_puzzle()  # Generate the initial Sudoku puzzle
    running = True
    while running:
        window.fill(BACKGROUND_COLOR)  # Clear the window with the background color
        render_grid()  # Render the Sudoku grid
        draw_highlight()  # Highlight the selected cell
        pygame.display.update()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the user closes the window
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Check if the user clicks the mouse
                get_cell_coordinates(pygame.mouse.get_pos())  # Get cell coordinates based on mouse position
            elif event.type == pygame.KEYDOWN:  # Check if a key is pressed
                if event.key == pygame.K_r:  # Check if 'R' key is pressed
                    puzzle_grid = generate_simple_puzzle()  # Generate a new puzzle
                elif event.key == pygame.K_s:  # Check if 'S' key is pressed
                    if auto_solving:
                        auto_solving = False
                    else:
                        auto_solving = True
                        if solve_sudoku(puzzle_grid):  # Attempt to solve the puzzle
                            display_completion_message()  # Display completion message if solved
                            auto_solving = False
                elif event.key in range(pygame.K_1, pygame.K_9 + 1):  # Check if a number key (1-9) is pressed
                    num = event.key - pygame.K_0  # Convert key to corresponding number
                    if is_valid_move(puzzle_grid, selected_y, selected_x, num):  # Validate the move
                        puzzle_grid[selected_y][selected_x] = num  # Place the number in the selected cell
                        display_number(num)  # Display the number in the cell
                    else:
                        show_error_message("Invalid Move")  # Show error message if the move is invalid

    pygame.quit()  # Quit Pygame when the game loop ends

if __name__ == "__main__":
    main()  # Start the game
