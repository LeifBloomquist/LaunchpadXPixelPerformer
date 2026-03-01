from colors import *

class Theme:
    def __init__(self, logo_color, playing_color, playing_off_color, cued_color, oneshot_color, filled_color, idle_color, arrow_colors, error_color):
        self.logo_color = logo_color
        self.playing_color = playing_color
        self.playing_off_color = playing_off_color
        self.cued_color = cued_color
        self.oneshot_color = oneshot_color
        self.filled_color = filled_color
        self.idle_color = idle_color
        self.arrow_colors = arrow_colors
        self.error_color = error_color
        
        # Defaults for all themes
        self.OFF = COLOR_BLACK
        self.session_default = COLOR_WHITE
        self.session_pressed = COLOR_DARKRED
        self.session_cleared = COLOR_RED
        self.stopped_color = COLOR_ORANGE
        self.bar_color = COLOR_YELLOW
        self.beat_color = COLOR_GREEN
        
def CurrentTheme():
    return all_themes[current_theme_index]

def NextTheme():
    global current_theme_index
    
    current_theme_index += 1
    if current_theme_index >= len(all_themes):
        current_theme_index = 0

current_theme_index = 0

theme_launchpad_s = Theme(logo_color=COLOR_GREEN,  playing_color=COLOR_ORANGE3, playing_off_color=COLOR_YELLOW4, cued_color=COLOR_REDORANGE, oneshot_color=COLOR_YELLOW1, filled_color=COLOR_GREEN1,   idle_color=COLOR_ORANGE,   arrow_colors=COLOR_GREY5,    error_color=COLOR_PINK)
theme_bloodred    = Theme(logo_color=COLOR_RED,    playing_color=COLOR_RED,     playing_off_color=COLOR_RED4,    cued_color=COLOR_RED,       oneshot_color=COLOR_RED4,    filled_color=COLOR_DARKRED,  idle_color=COLOR_ORANGE2,  arrow_colors=COLOR_RED3,     error_color=COLOR_PINK)
theme_unicorn     = Theme(logo_color=COLOR_PINK,   playing_color=COLOR_PINK,    playing_off_color=COLOR_PINK1,   cued_color=COLOR_PINK1,     oneshot_color=COLOR_BLUE1,   filled_color=COLOR_CYAN,     idle_color=COLOR_GREY1,    arrow_colors=COLOR_DARKBLUE, error_color=COLOR_RED)
theme_iceblue     = Theme(logo_color=COLOR_BLUE,   playing_color=COLOR_WHITE,   playing_off_color=COLOR_GREY5,   cued_color=COLOR_GREY1,     oneshot_color=COLOR_BLUE1,   filled_color=COLOR_DARKBLUE, idle_color=COLOR_DARKBLUE, arrow_colors=COLOR_GREY7,    error_color=COLOR_RED)

all_themes = ( theme_launchpad_s, theme_bloodred, theme_unicorn, theme_iceblue )
