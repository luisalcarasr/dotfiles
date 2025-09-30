from libqtile.layout.verticaltile import VerticalTile as BaseVerticalTile

class VerticalTile(BaseVerticalTile):
    def configure(self, window, screen_rect):
        if self.clients and window in self.clients:
            n = len(self.clients)
            index = self.clients.index(window)

            # border
            if n > 1:
                border_width = self.border_width
            else:
                border_width = self.single_border_width

            # margin
            if n == 1 and self.single_margin is not None:
                margin = self.single_margin
            else:
                m = self.margin
                margin = [m, m, m if index == n - 1 else 0, m]

            if window.has_focus:
                border_color = self.border_focus
            else:
                border_color = self.border_normal

            # width
            if n > 1:
                width = screen_rect.width - self.border_width * 2
            else:
                width = screen_rect.width

            # height
            if n > 1:
                main_area_height = int(screen_rect.height * self.ratio)
                sec_area_height = screen_rect.height - main_area_height

                main_pane_height = main_area_height - border_width * 2
                sec_pane_height = sec_area_height // (n - 1) - border_width * 2
                normal_pane_height = (screen_rect.height // n) - (border_width * 2)

                if self.maximized:
                    if window is self.maximized:
                        height = main_pane_height
                    else:
                        height = sec_pane_height
                else:
                    height = normal_pane_height
            else:
                height = screen_rect.height

            # y
            y = screen_rect.y

            if n > 1:
                if self.maximized:
                    y += (index * sec_pane_height) + (border_width * 2 * index)
                else:
                    y += (index * normal_pane_height) + (border_width * 2 * index)

                if self.maximized and window is not self.maximized:
                    if index > self.clients.index(self.maximized):
                        y = y - sec_pane_height + main_pane_height

            window.place(
                screen_rect.x, y, width, height, border_width, border_color, margin=margin
            )
            window.unhide()
        else:
            window.hide()
