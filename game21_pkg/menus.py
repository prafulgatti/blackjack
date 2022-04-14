# container class to define coloring for the terminal menus
# I got this idea from https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    WHITEBG  = '\33[47m'

class style_bj(style):
    CWHITEBG = style.WHITEBG
    CBLACK  = style.BLACK+'♠    ♣   '
    CRED = style.RED+'   ♦    ♥ '
    BL= style.BLACK+style.BOLD+'   B L A C K J A C K    '


def blackjack_intro(wins,loss):
    print( "---------------------------------------------")
    print("|"+style.WHITEBG+ style_bj.CRED+ style_bj.BL+ style_bj.CBLACK + style.RESET+  "|")
    print("---------------------------------------------")
    print("|"+style.GREEN+"       WINS:",wins,style.RESET+"       |"+style.RED+"   LOSS:",loss,style.RESET,"        |")
    print("---------------------------------------------")
    return

def blackjack_outro(wins,loss):
    print( "---------------------------------------------")
    print("|"+style.WHITEBG+ style_bj.CRED+ style_bj.BL+ style_bj.CBLACK + style.RESET+  "|")
    print("---------------------------------------------")
    print("|"+style.GREEN+"       WINS:",wins,style.RESET+"       |"+style.RED+"   LOSS:",loss,style.RESET,"        |")
    print("---------------------------------------------")
    print("| 1. Play[P]  | 2. Stats[S]  | 3. Quit [Q]  |")
    print("---------------------------------------------")
    return

def blackjack_menu():
    print("---------------------------------------------")
    print("|"+style.WHITEBG+ style_bj.CRED+ style_bj.BL+ style_bj.CBLACK + style.RESET+  "|")
    print("---------------------------------------------")
    print("| 1. Hit [H]         |  2. Stand [S]        |")
    print("---------------------------------------------")
    print("|              3. Fold [F]                  |")
    print("---------------------------------------------")
    return

def blackjack_simulation():
    print("---------------------------------------------")
    print("|"+style.WHITEBG+ style_bj.CRED+ style_bj.BL+ style_bj.CBLACK + style.RESET+  "|")
    print("---------------------------------------------")
    print("| 1. Simulation [S]   |  2. Quit [Q]        |")
    print("---------------------------------------------")
    return 