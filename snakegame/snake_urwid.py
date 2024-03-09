import random
import urwid

class SnakeGame(urwid.Frame):
    def __init__(self):
        self.snake = [
            [10, 10],
            [10, 9],
            [10, 8]
        ]
        self.food = None
        self.direction = (0, 1)
        self.update_screen()

    def update_screen(self):
        self.body = urwid.SimpleFocusListWalker(self.draw_snake())
        self.original_widget = urwid.Filler(urwid.Pile(self.body), 'top')
        self.pack(self.original_widget)

    def draw_snake(self):
        result = []

        snake_pile = urwid.Pile()
        for part in self.snake:
            snake_pile.contents.append((urwid.Text(u'█'), snake_pile.options()))

        result.append(snake_pile)

        if self.food:
            food_pile = urwid.Pile([(urwid.Text(u'π'), food_pile.options())])
            result.append(food_pile)

        return result

    def keypress(self, size, key):
        if key == 'up':
            self.direction = (0, -1)
        elif key == 'down':
            self.direction = (0, 1)
        elif key == 'left':
            self.direction = (-1, 0)
        elif key == 'right':
            self.direction = (1, 0)

    def game_over(self):
        quitter = urwid.Button('Quit', on_press=self.quit)
        self.original_widget = urwid.Filler(urwid.Pile([quitter]), 'center')
        self.pack(self.original_widget)

    def move_snake(self):
        head = self.snake[0]
        new_head = [head[0] + self.direction[0], head[1] + self.direction[1]]
        self.snake.insert(0, new_head)

        if self.food and new_head == self.food:
            self.food = None
        else:
            tail = self.snake.pop()

        if not self.food:
            self.food = [
                random.randint(1, sh-2),
                random.randint(1, sw-2)
            ]

        if (new_head in self.snake or
                new_head[0] in [0, sh-1] or
                new_head[1] in [0, sw-1]):
            self.game_over()
            return False

        self.update_screen()
        return True

    def main(self):
        top = urwid.Overlay(self, urwid.SolidFill(u'\N{MEDIUM SHADE}'))
        urwid.MainLoop(top, palette=[('body', 'black', 'white')],
                       unhandled_input=self.keypress).run()

    def quit(self, button):
        raise urwid.ExitMainLoop()


if __name__ == '__main__':
    sh, sw = 50, 100
    snake_game = SnakeGame()
    snake_game.main()
