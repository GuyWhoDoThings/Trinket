"""
$$$$$$$$\        $$\           $$\                  $$\
\__$$  __|       \__|          $$ |                 $$ |
   $$ | $$$$$$\  $$\ $$$$$$$\  $$ |  $$\  $$$$$$\ $$$$$$\
   $$ |$$  __$$\ $$ |$$  __$$\ $$ | $$  |$$  __$$\\_$$  _|
   $$ |$$ |  \__|$$ |$$ |  $$ |$$$$$$  / $$$$$$$$ | $$ |
   $$ |$$ |      $$ |$$ |  $$ |$$  _$$<  $$   ____| $$ |$$\
   $$ |$$ |      $$ |$$ |  $$ |$$ | \$$\ \$$$$$$$\  \$$$$  |
   \__|\__|      \__|\__|  \__|\__|  \__| \_______|  \____/

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
"""


class Color:

    ESCAPE = "\xc2\xa7"

    BLACK = ESCAPE + "0"
    DARK_BLUE = ESCAPE + "1"
    DARK_GREEN = ESCAPE + "2"
    DARK_AQUA = ESCAPE + "3"
    DARK_RED = ESCAPE + "4"
    DARK_PURPLE = ESCAPE + "5"
    GOLD = ESCAPE + "6"
    GRAY = ESCAPE + "7"
    DARK_GRAY = ESCAPE + "8"
    BLUE = ESCAPE + "9"
    GREEN = ESCAPE + "a"
    AQUA = ESCAPE + "b"
    RED = ESCAPE + "c"
    LIGHT_PURPLE = ESCAPE + "d"
    YELLOW = ESCAPE + "e"
    WHITE = ESCAPE + "f"
    OBFUSCATED = ESCAPE + "k"
    BOLD = ESCAPE + "l"
    STRIKETHROUGH = ESCAPE + "m"
    UNDERLINE = ESCAPE + "n"
    ITALIC = ESCAPE + "o"
    RESET = ESCAPE + "R"
