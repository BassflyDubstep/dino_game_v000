import arcade

def draw_filled_bordered_lbwh_rect(l, b, w, h, fill_color, border_color, border_width = 1):
    arcade.draw_lbwh_rectangle_filled(l, b, w, h, fill_color)
    arcade.draw_lbwh_rectangle_outline(l, b, w, h, border_color, border_width)

class SidePanel(arcade.Section):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # XY Screen relative points are for converting the local SECTION coords over to the global WINDOW coords.
        self.screen_ll_x, self.screen_ll_y = self.get_xy_screen_relative(0, 0)
        self.screen_ur_x, self.screen_ur_y = self.get_xy_screen_relative(self.width, self.height)
        print(f'Panel Screen LL: ({self.screen_ll_x}, {self.screen_ll_y}); UR: ({self.screen_ur_x}, {self.screen_ur_y})')

        # XY Section relative points are for converting the global WINDOW coords over to the local SECTION coords.
        self.section_ll_x, self.section_ll_y = self.get_xy_section_relative(self.left, self.bottom)
        self.section_ur_x, self.section_ur_y = self.get_xy_section_relative(self.right, self.top)
        print(f'Panel Section LL: ({self.section_ll_x}, {self.section_ll_y}); UR: ({self.section_ur_x}, {self.section_ur_y})')
        self.setup()

    def setup(self):
        pass

    def on_draw(self):
        draw_filled_bordered_lbwh_rect(self.left, self.bottom, self.width, self.height, 
                                       arcade.color.LIGHT_GRAY, arcade.color.WHITE)

class ActionArea(arcade.Section):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # XY Screen relative points are for converting the local SECTION coords over to the global WINDOW coords.
        self.screen_ll_x, self.screen_ll_y = self.get_xy_screen_relative(0, 0)
        self.screen_ur_x, self.screen_ur_y = self.get_xy_screen_relative(self.width, self.height)
        print(f'Game Area LL: ({self.screen_ll_x}, {self.screen_ll_y}); UR: ({self.screen_ur_x}, {self.screen_ur_y})')

        # XY Section relative points are for converting the global WINDOW coords over to the local SECTION coords.
        self.section_ll_x, self.section_ll_y = self.get_xy_section_relative(self.left, self.bottom)
        self.section_ur_x, self.section_ur_y = self.get_xy_section_relative(self.right, self.top)
        print(f'Game Area Section LL: ({self.section_ll_x}, {self.section_ll_y}); UR: ({self.section_ur_x}, {self.section_ur_y})')
        self.setup()

    def setup(self):
        self.circle = arcade.SpriteCircle(25, arcade.color.CYAN)
        self.circle.center_x, self.circle.center_y = self.get_xy_screen_relative(self.width // 2, self.height // 2)
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.circle)

    def on_draw(self):
        draw_filled_bordered_lbwh_rect(self.left, self.bottom, self.width, self.height, 
                                       arcade.color.BLACK, arcade.color.RED)
        
        # The check to see if objects are off-screen needs to happen on the draw, NOT on the update.
        # Also, successive "if" statements are needed to prevent the ball from "floating" at the corners
        # (as can happen if this is converted to a typical "if-elif" block).
        if self.circle.center_x < self.screen_ll_x:
            self.circle.center_x = self.screen_ll_x
        if self.circle.center_y < self.screen_ll_y:
            self.circle.center_y = self.screen_ll_y
        if self.circle.center_x > self.screen_ur_x:
            self.circle.center_x = self.screen_ur_x
        if self.circle.center_y > self.screen_ur_y:
            self.circle.center_y = self.screen_ur_y

        self.sprite_list.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol in [arcade.key.UP, arcade.key.W]:
            self.circle.change_y = 10
        elif symbol in [arcade.key.DOWN, arcade.key.S]:
            self.circle.change_y = -10
        elif symbol in [arcade.key.LEFT, arcade.key.A]:
            self.circle.change_x = -10
        elif symbol in [arcade.key.RIGHT, arcade.key.D]:
            self.circle.change_x = 10
    
    def on_key_release(self, symbol, modifiers):
        if symbol in [arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S]:
            self.circle.change_y = 0
        elif symbol in [arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D]:
            self.circle.change_x = 0

    def on_update(self, delta_time: float):
        self.sprite_list.update()





class MainView(arcade.View):

    def __init__(self):
        super().__init__()
        print(f'Window Dims: {self.width}x{self.height}')
        self.side_panel = SidePanel(0, 0, self.width * 0.2, self.height, prevent_dispatch={True}, accept_keyboard_keys = False)
        self.action_area = ActionArea(self.width * 0.2, 0, self.width * 0.8, self.height, 
                                      accept_keyboard_keys=True)
        self.sm = arcade.SectionManager(self)
        self.sm.add_section(self.action_area)
        self.sm.add_section(self.side_panel)
    
    def on_draw(self):
        self.clear()

    def on_update(self, delta_time: float):
        pass

    def on_show_view(self):
        self.sm.enable()

    def on_hide_view(self):
        self.sm.hide()

    def on_show(self):
        arcade.set_background_color(arcade.color.ASH_GREY)

class MainWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

def main():
    window = MainWindow(900, 600, "Dino Game - Panels Test")
    main_view = MainView()
    arcade.set_background_color(arcade.color.ASH_GREY)
    window.show_view(MainView())
    arcade.run()

if __name__ == "__main__":
    main()