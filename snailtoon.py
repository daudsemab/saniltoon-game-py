import arcade

# Set how many rows and columns we will have
ROW_COUNT = 8
COLUMN_COUNT = 8

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 80
HEIGHT = 80

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

VERTICAL_PIXEL = (HEIGHT // 2) * 2 + MARGIN  # Center to Center Horizontal Distance
HORIZONTAL_PIXEL = (WIDTH // 2) * 2 + MARGIN  # Center to Center Vertical Distance

# Sprite Size
SPRITE_SCALING_PLAYER = 0.15

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN + 250
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "SNAILTOON"


# create variable which store the string, if any player won or game over
game_status = None


class GameView(arcade.View):
    turn = True

    def __init__(self):
        """
        Set up the application.
        """

        super().__init__()

        # Create a 2 dimensional array. A two-dimensional array is simply a list of lists.
        self.grid = [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

        # Player List
        self.player_list = None
        self.splash_list = None

        # Players boxes - Covered Area
        self.player1_map = []
        self.player2_map = []

        # Score
        self.p1_score, self.p2_score = None, None

        # Player Sprites
        self.player_sprite = None
        self.player2_sprite = None
        arcade.set_background_color(arcade.color.DARK_TERRA_COTTA)

        self.column = None
        self.row = None
        # Row-Column wise position of Player2
        self.column2 = None
        self.row2 = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Score
        self.p1_score, self.p2_score = 0, 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.splash_list = arcade.SpriteList()

        # --------- Set up the player
        # Character image
        p1_img = "./images/snailtoon-1.png"
        p2_img = "./images/snailtoon-2.png"
        # Players Sprite Creation
        self.player_sprite = arcade.Sprite(p1_img, SPRITE_SCALING_PLAYER)
        self.player2_sprite = arcade.Sprite(p2_img, SPRITE_SCALING_PLAYER)

        # Player-1 Initial Position
        self.player_sprite.center_x = (WIDTH // 2) + MARGIN
        self.player_sprite.center_y = (HEIGHT // 2) + MARGIN

        # Player-2 Initial Position
        # splash.center_x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
        # splash.center_y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
        self.player2_sprite.center_x = (MARGIN + WIDTH) * (COLUMN_COUNT - 1) + MARGIN + WIDTH // 2
        self.player2_sprite.center_y = (MARGIN + HEIGHT) * (ROW_COUNT - 1) + MARGIN + HEIGHT // 2
        # self.player2_sprite.center_x = SCREEN_WIDTH - ((WIDTH // 2) + MARGIN)
        # self.player2_sprite.center_y = SCREEN_HEIGHT - ((HEIGHT // 2) + MARGIN)

        # Adding Players to the players sprite list
        self.player_list.append(self.player_sprite)
        self.player_list.append(self.player2_sprite)

        # Row-Column wise position of Player1
        self.column = int(self.player_sprite.center_x // (WIDTH + MARGIN))
        self.row = int(self.player_sprite.center_y // (HEIGHT + MARGIN))
        # Row-Column wise position of Player2
        self.column2 = int(self.player2_sprite.center_x // (WIDTH + MARGIN))
        self.row2 = int(self.player2_sprite.center_y // (HEIGHT + MARGIN))

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw Text Scores
        x = (MARGIN + WIDTH) * COLUMN_COUNT + MARGIN + WIDTH // 2
        y = (MARGIN + HEIGHT) * ROW_COUNT + MARGIN + HEIGHT // 2
        arcade.draw_text(f'SNAILTOON', x, y * 0.88, arcade.color.RED_DEVIL, 20, 50, "left", font_name="Kenney Blocks")
        arcade.draw_text(f'P1-SCORE: {self.p1_score}', x + HORIZONTAL_PIXEL // 4, VERTICAL_PIXEL,
                         arcade.color.WHITE_SMOKE, 12, 50, "left", font_name="Kenney Future")
        arcade.draw_text(f'P2-SCORE: {self.p2_score}', x + HORIZONTAL_PIXEL // 4, VERTICAL_PIXEL // 2,
                         arcade.color.WHITE_SMOKE, 12, 50, "left", font_name="Kenney Future")

        # Draw the grid
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Figure out what color to draw the box
                color = arcade.color.WHITE_SMOKE

                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                # Draw the box
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

        # --------- Set up the splashes
        # importing local images using absolute path
        splash1 = "./images/splash1.png"
        splash2 = "./images/splash2.png"

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Figure out what splash to draw in the cell
                if self.grid[row][column] == 1:
                    # create a new splash
                    splash = arcade.Sprite(splash1, 0.15)
                    # Do the math to figure out where to draw splash
                    splash.center_x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                    splash.center_y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                    self.splash_list.append(splash)
                elif self.grid[row][column] == 2:
                    # create a new splash
                    splash = arcade.Sprite(splash2, 0.15)
                    # Do the math to figure out where to draw splash
                    splash.center_x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                    splash.center_y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                    self.splash_list.append(splash)

        self.splash_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player
        self.player_list.update()
        self.splash_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Player1 position
        column = int(self.player_sprite.center_x // (WIDTH + MARGIN))
        row = int(self.player_sprite.center_y // (HEIGHT + MARGIN))
        # Player2 position
        column2 = int(self.player2_sprite.center_x // (WIDTH + MARGIN))
        row2 = int(self.player2_sprite.center_y // (HEIGHT + MARGIN))

        # if player1 turn
        if self.turn:
            if key == arcade.key.UP:
                # if screen include position and didn't map by anyone previously
                not_mapped_by2 = (self.grid[row + 1][column] != 2 and (row + 1, column) != (row2, column2))
                if row < ROW_COUNT - 1 and not_mapped_by2:
                    self.plus_p1_score(row, column)
                    if self.grid[row + 1][column] == 1:
                        # if it is mapped, then slip
                        while self.grid[row + 1][column] == 1:
                            try:
                                # step UP
                                self.player_sprite.center_y += VERTICAL_PIXEL
                                # change row
                                row += 1
                                # Check if index go out of range
                                # test = self.grid[row + 1][column]
                            except IndexError:
                                break
                    else:
                        # shift sprite to the new center
                        self.player_sprite.center_y += VERTICAL_PIXEL
                        # change row
                        row += 1

                    # change turn
                    self.change_turn()
            elif key == arcade.key.DOWN:
                # if screen include position and didn't map by anyone previously
                not_mapped_by2 = (self.grid[row - 1][column] != 2 and (row - 1, column) != (row2, column2))
                if row > 0 and not_mapped_by2:
                    self.plus_p1_score(row, column)
                    if self.grid[row - 1][column] == 1:
                        # if it is mapped, then slip
                        while self.grid[row - 1][column] == 1:
                            try:
                                # step DOWN
                                self.player_sprite.center_y -= VERTICAL_PIXEL
                                # change row
                                row -= 1
                                # Check if index go out of range
                                # test = self.grid[row - 1][column]
                                if row - 1 < 0:
                                    break
                            except IndexError:
                                break
                    else:
                        # shift sprite to the new center
                        self.player_sprite.center_y -= VERTICAL_PIXEL
                        # change row
                        row -= 1

                    # change turn
                    self.change_turn()
            elif key == arcade.key.LEFT:
                # if screen include position and didn't map by anyone previously
                not_mapped_by2 = (self.grid[row][column - 1] != 2 and (row, column - 1) != (row2, column2))
                if column > 0 and not_mapped_by2:
                    self.plus_p1_score(row, column)
                    if self.grid[row][column - 1] == 1:
                        # if it is mapped, then slip
                        while self.grid[row][column - 1] == 1:
                            try:
                                # change column
                                column -= 1
                                # step LEFT
                                self.player_sprite.center_x -= HORIZONTAL_PIXEL
                                # Check if index go out of range
                                # test = self.grid[row][column - 1]
                                if column - 1 < 0:
                                    break
                            except IndexError:
                                break
                    else:
                        # shift sprite to the new center
                        self.player_sprite.center_x -= HORIZONTAL_PIXEL
                        # change column
                        column -= 1

                    # change turn
                    self.change_turn()
            elif key == arcade.key.RIGHT:
                # if screen include position and didn't map by anyone previously
                not_mapped_by2 = (self.grid[row][column + 1] != 2 and (row, column + 1) != (row2, column2))
                if column < COLUMN_COUNT - 1 and not_mapped_by2:
                    self.plus_p1_score(row, column)
                    if self.grid[row][column + 1] == 1:
                        # if it is mapped, then slip
                        while self.grid[row][column + 1] == 1:
                            try:
                                # change column
                                column += 1
                                # step RIGHT
                                self.player_sprite.center_x += HORIZONTAL_PIXEL
                                # Check if index go out of range
                                # test = self.grid[row][column + 1]
                            except IndexError:
                                break
                    else:
                        # shift sprite to the new center
                        self.player_sprite.center_x += HORIZONTAL_PIXEL
                        # change column
                        column += 1

                    # change turn
                    self.change_turn()

        # if player2 turn
        else:
            if key == arcade.key.UP:
                # if screen include position and didn't map by anyone previously
                not_mapped_by1 = (self.grid[row2 + 1][column2] != 1 and (row2 + 1, column2) != (row, column))
                if row2 < ROW_COUNT - 1 and not_mapped_by1:
                    self.plus_p2_score(row2, column2)
                    if self.grid[row2 + 1][column2] == 2:
                        # if it is mapped, then slip
                        while self.grid[row2 + 1][column2] == 2:
                            try:
                                # step UP
                                self.player2_sprite.center_y += VERTICAL_PIXEL
                                # change row
                                row2 += 1
                                # Check if index go out of range
                                # test = self.grid[row2 + 1][column2]
                            except IndexError:
                                break
                    else:
                        # shift sprite to the new center
                        self.player2_sprite.center_y += VERTICAL_PIXEL
                        # change row
                        row2 += 1

                    # change turn
                    self.change_turn()
            elif key == arcade.key.DOWN:
                # if screen include position and didn't map by anyone previously
                not_mapped_by1 = (self.grid[row2 - 1][column2] != 1 and (row2 - 1, column2) != (row, column))
                if row2 > 0 and not_mapped_by1:
                    self.plus_p2_score(row2, column2)
                    if self.grid[row2 - 1][column2] == 2:
                        # if it is mapped, then slip
                        while self.grid[row2 - 1][column2] == 2:
                            try:
                                # step UP
                                self.player2_sprite.center_y -= VERTICAL_PIXEL
                                # change row
                                row2 -= 1
                                # Check if index go out of range
                                # test = self.grid[row2 - 1][column2]
                                if row2 - 1 < 0:
                                    break
                            except IndexError:
                                break
                    else:
                        # shift sprite to the new center
                        self.player2_sprite.center_y -= VERTICAL_PIXEL
                        # change row
                        row2 -= 1

                    # change turn
                    self.change_turn()
            elif key == arcade.key.LEFT:
                # if screen include position and didn't map by anyone previously
                not_mapped_by1 = (self.grid[row2][column2 - 1] != 1 and (row2, column2 - 1) != (row, column))
                if column2 > 0 and not_mapped_by1:
                    self.plus_p2_score(row2, column2)
                    if self.grid[row2][column2 - 1] == 2:
                        # if it is mapped, then slip
                        while self.grid[row2][column2 - 1] == 2:
                            try:
                                # change column
                                column2 -= 1
                                # step LEFT
                                self.player2_sprite.center_x -= HORIZONTAL_PIXEL
                                # Check if index go out of range
                                # test = self.grid[row2][column2 - 1]
                                if column2 - 1 < 0:
                                    break
                            except IndexError:
                                break
                    else:
                        # shift sprite to the new center
                        self.player2_sprite.center_x -= HORIZONTAL_PIXEL
                        # change column
                        column2 -= 1

                    # change turn
                    self.change_turn()
            elif key == arcade.key.RIGHT:
                # if screen include position and didn't map by anyone previously
                not_mapped_by1 = (self.grid[row2][column2 + 1] != 1 and (row2, column2 + 1) != (row, column))
                if column2 < COLUMN_COUNT - 1 and not_mapped_by1:
                    self.plus_p2_score(row2, column2)
                    if self.grid[row2][column2 + 1] == 2:
                        # if it is mapped, then slip
                        while self.grid[row2][column2 + 1] == 2:
                            try:
                                # change column
                                column2 += 1
                                # step RIGHT
                                self.player2_sprite.center_x += HORIZONTAL_PIXEL
                                # Check if index go out of range
                                # test = self.grid[row2][column2 + 1]
                            except IndexError:
                                break
                    else:
                        # shift sprite to the new center
                        self.player2_sprite.center_x += HORIZONTAL_PIXEL
                        # change column
                        column2 += 1

                    # change turn
                    self.change_turn()

        print(f'SNAIL-1 Score: {self.p1_score}')
        print(f'SNAIL-2 Score: {self.p2_score}')

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # global variable which store game decision i.e., player-1 won or match draw etc
        global game_status

        # If a player releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

        for row in self.grid:
            if 0 in row:
                break
        else:
            if self.p1_score > self.p2_score:
                game_status = "PLAYER-1 WON!"
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)
            elif self.p2_score > self.p1_score:
                game_status = "PLAYER-2 WON!"
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)
            else:
                game_status = "MATCH DRAW"
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)

    def plus_p1_score(self, row, column):
        # if the cell is not mapped by anyone
        if self.grid[row][column] == 0:
            # cell is mapped by player1
            self.grid[row][column] = 1
            self.player1_map.append((row, column))
            # increment score
            self.p1_score += 1

    def plus_p2_score(self, row2, column2):
        # if the cell is not mapped by anyone
        if self.grid[row2][column2] == 0:
            # cell is mapped by player2
            self.grid[row2][column2] = 2
            self.player2_map.append((row2, column2))
            # increment score
            self.p2_score += 1

    def change_turn(self):
        if self.turn:
            self.turn = False
        else:
            self.turn = True


class InstructionView(arcade.View):

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.DARK_TERRA_COTTA)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("SNAILTOON", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center", font_name="Kenney Future")

        arcade.draw_text("Click to Play!", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center", font_name="Kenney Future")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameOverView(arcade.View):

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.DARK_TERRA_COTTA)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("GAME OVER", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center", font_name="Kenney Future")
        # Uncomment the code below to implement the Game Status - Win, Lose, Draw
        arcade.draw_text(game_status, self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center", font_name="Kenney Future")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        restart_view = InstructionView()
        self.window.show_view(restart_view)


def main():
    """ Main Function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
