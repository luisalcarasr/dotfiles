from kittens.tui.handler import result_handler


def main(args):
    pass


@result_handler(no_ui=True)
def handle_result(args, answer, target_window_id, boss):
    tab = boss.active_tab
    w = boss.active_window
    if not tab or not w:
        return

    # Get the OS window size (the full kitty window, not individual panes)
    from kitty.fast_data_types import get_os_window_size
    os_window_size = get_os_window_size(w.os_window_id)
    if not os_window_size:
        return
    pixel_width = os_window_size['width']
    pixel_height = os_window_size['height']
    # +1 because the new window hasn't been created yet
    num_windows = len(tab.windows) + 1

    if pixel_width > pixel_height:
        # Landscape: fat (top/bottom) for 2 panes, grid for 3+
        target = 'fat' if num_windows <= 2 else 'grid'
    else:
        # Portrait: always stack one below the other
        target = 'vertical'

    if tab.current_layout.name != target:
        tab.goto_layout(target)
