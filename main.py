import arcade

def MainView(arcade.View):

    def __init__(self):
        super().__init__()
    
    def on_draw(self):
        self.clear()

    def on_update(self, delta_time: float):

    def on_show(self):
        arcade.set_background_color(arcade.color.ASH_GREY)

def MainWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

def main():
    window = MainWindow(800, 600, "Dino Game")
    main_view = MainView()
    arcade.set_background_color(arcade.color.ASH_GREY)
    window.show_view(MainView())
    arcade.run()

if __name__ == "__main__":
    main()