import os
import re
import sys

COLOUR_DICT: {}

class Colours:
    # Private Methods
    def _colour_to_escape_sequence(self, colour_tag: str, foreground_colour=True):
        """Gets either the RGB value and creates an ANSI Escape String
        
        Returns: ANSI Escape Sequence"""
        colour_name = colour_tag.replace('<', '').replace('>', '')

        r, g, b = self._get_rgb_value(colour_name)

        if foreground_colour:
            return f"\033[38;2;{r};{g};{b}m"
        else:
            return f"\033[48;2;{r};{g}{b}m"

    def _get_rgb_value(self, our_colour_name: str):
        """Gets the RGB value of the colour from the 'colours.txt' file.
        
        Returns the R, G, B values in an set."""

        global COLOUR_DICT
        our_colour_name = our_colour_name.replace(' ', '').upper()

        if our_colour_name in COLOUR_DICT:
            return COLOUR_DICT[our_colour_name]

        
    def _is_colour_valid(self, tag: str):
        """Checks to see if the colour is in the 'colours.txt' file, 
        
        Returns: bool"""
        colour_to_check = tag.replace(' ', '').replace('<', '').replace('>', '').upper()

        return colour_to_check in COLOUR_DICT

    def _tag_format_name(self, tag: str):
        """Automatically Formats a tag for a specific purpose, depending what is included in the tag.
        
        Returns the formatted text"""

        if tag.find('<') != -1 or tag.find('>') != -1:
            return tag.replace('<', '').replace('>', '')

        return tag.replace(' ', '').upper()
    def _tag_handle_special(self, text: str):
        """Removes the special tags from the text and makes them functional
        
        Special Tags:
        - <b>
        - <ul>
        - <i>
        - <blink>
        - <sblink>
        - <cross>
        - <faint>

        Returns: text_with_tags_applied
        """

        # Special Tags Vars
        SETBOLD = "\033[1m"
        UNSETBOLD = "\033[22m"

        SETUNDERLINE = "\033[4m"
        UNSETUNDERLINE = "\033[24m"

        SETITALIC = "\033[3m"
        UNSETITALIC = "\033[23m"

        SETBLINK = "\033[5m"
        SETSLOWBLINK = "\033[5m"
        UNSETBLINK = "\033[25m"

        SETCROSSED = "\033[9m"
        UNSETCROSSED = "\033[29m"

        SETFAINT = "\033[2m"
        UNSETFAINT = "\033[22m"

        VALID_TAGS = {
            '<b>':SETBOLD, 
            '<blink>':SETBLINK, 
            '<ul>':SETUNDERLINE, 
            '<i>':SETITALIC, 
            '<cross>':SETCROSSED, 
            '<faint>':SETFAINT, 
            '<sblink>':SETSLOWBLINK,
            '</b>':UNSETBOLD, 
            '</blink>':UNSETBLINK, 
            '</ul>':UNSETUNDERLINE, 
            '</i>':UNSETITALIC, 
            '</cross>':UNSETCROSSED, 
            '</faint>':UNSETFAINT, 
            '</sblink>':UNSETBLINK
            }

        tags = re.findall(r'\<[\w /]+\>', text)

        for tag in tags:
            if tag in VALID_TAGS:
                text = text.replace(f'{tag}', f'{VALID_TAGS[tag]}')

        return text

    def _create_main_file(self):
        """Creates the 'colours.txt' file with all default colours.
        
        Note: This is needed for the script to work!"""

        default_colour_names = ['WHITE', 'BLACK', 'GREY', 'RED', 'GREEN', 'BLUE', 'MAROON', 'LIMEGREEN', 'TEAL', 'LIGHTBLUE', 'YELLOW', 'AMBER', 'ORANGE', 'OLIVE', 'TAN', 'PURPLE', 'LIGHTPURPLE', 'OPERAMAUVE', 'FUCHSIA', 'PINK', 'CYAN', 'SILVER']
        default_colour_rgb = ['255, 255, 255', '0, 0, 0', '178, 190, 181', '255, 0, 0', '0, 255, 0', '0, 0, 255', '128, 0, 0', '50, 205, 50', '0, 128, 128', '128, 216, 240', '255, 255, 0', '255, 191, 0', '255, 170, 0', '153, 153, 0', '210, 180, 140', '128, 0, 128', '204, 135, 232', '178, 132, 190', '255, 0, 255', '255, 192, 203', '0, 255, 255', '192, 192, 192']

        with open("colours.txt", "w") as f:

            f.write("# If you want to add a custom colour, you can use the '--add-colour' paramater with the arguments '\"name\" r g b'\n")
            f.write("#  this is the safest way to add a custom colour.\n")
            f.write('#\n')
            f.write('# If you want to manually add custom colours please format it like so:\n')
            f.write('#  COLOURNAME = "r, g, b".\n')
            f.write('#  please make sure the name is CAPITALIZED and has no spaces or special characters.\n\n')

            for name, rgb in zip(default_colour_names, default_colour_rgb):

                if name == default_colour_names[-1]:
                    f.write(f"{name} = \"{rgb}\"")
                else:
                    f.write(f"{name} = \"{rgb}\"\n")  

    # Public Methods
    def cprint(self, text_to_print, default_colour_name="DEFAULT", background_colour_name="DEFAULT", ignore_tags=False):
        """Prints coloured text to the terminal using colour tags.
        
        Note: Run the script with '--tags' or '--palette' to show all tags or colours respectively."""
        
        # Default strings to revert colours.
        RESETALL = f"\033[m"
        DEFAULTBG = f"\033[49m"
        DEFAULTFG = f"\033[39m"

        VALID_COLOUR = False
        
        if default_colour_name == "DEFAULT":
            default_colour = DEFAULTFG
        else:
            # Setting the default_colour ANSI escape sequence.
            default_r, default_g, default_b = self._get_rgb_value(default_colour_name)
            default_colour = f"\033[38;2;{default_r};{default_g};{default_b}m"

        DEFAULT_DICT = {
            '<def>':default_colour,
            '<default>':default_colour
        }

        if not ignore_tags:
            # Handle any special tags, before checking for colour.
            text_to_print = self._tag_handle_special(text_to_print)

            tags = re.findall(r'\<[\w ]+\>', text_to_print)

            for tag in tags:
                #formatted_tag_name = self._tag_format_name(tag) #Removes '<>' from tag.

                if tag in DEFAULT_DICT:
                    text_to_print = text_to_print.replace(f'{tag}', DEFAULT_DICT[tag])
                    continue

                VALID_COLOUR = self._is_colour_valid(tag)

                if not VALID_COLOUR:
                    print(f"'{tag}' is NOT a valid colour/tag in the list. Please add it, or check the spelling.")
                    return False
                    
                mask = self._colour_to_escape_sequence(tag) # the ANSI escape sequence for the RGB colour.
                text_to_print = text_to_print.replace(f"{tag}", mask)

        if background_colour_name == "DEFAULT":
            background_colour = DEFAULTBG
        else:
            background_colour = self._colour_to_escape_sequence(background_colour_name, foreground_colour=False)

        # Concatenate all of the options together, resulting in coloured text that does not effect any other lines.
        print(background_colour + default_colour + text_to_print + RESETALL) 

    def print_all_colours(self):
            for colour in COLOUR_DICT:
                cprint(colour, colour)

    def print_all_tags(self):
        cprint('<b>b - Bold</b>')
        cprint('<ul>ul - Underline</ul>')
        cprint('<i>i - Italic</i>')
        cprint('<blink>blink - Blink</blink>')
        cprint('<sblink>sblink - Slow Blink</sblink>')
        cprint('<cross>cross - Cross</cross>')
        cprint('<faint>faint - Faint</faint>')

    def colours_add_custom(self, colour_name, r, g, b):
        """Create a custom colour with RGB values, and add it to 'colours.txt'."""
        
        rgb = [r, g, b]
        for x in rgb:
            if int(x) > 255 or int(x) < 0:
                self.cprint("[<red>ERROR<def>] RGB Values can not exceed 255 or drop below 0")
                return
        
        colour_name = self._tag_format_name(colour_name)
        with open("colours.txt", 'r') as f:
            for line in f.readlines():
                line_colour = line[0:line.find(' ')]
                if line_colour == colour_name:
                    self.cprint(f"[<b><red>ERROR<b><def>] '{colour_name}' is already in the list!")
                    return

        with open("colours.txt", "a") as f:
            f.write(f"\n{colour_name} = \"{r}, {g}, {b}\"")
        
        self.cprint(f"{colour_name} SUCESSFULLY ADDED!", colour_name)
    def help_me_pls(self):
        self.cprint("MORE INFO AVALIBLE IN THE HELP.TXT DOC")
        self.cprint('Here is a quick tutorial on how to use the <light blue>\'cprint\'<default> command\n')
        self.cprint("<light blue>'cprint'<def> takes 2 paramaters. The first is the <green>'text_to_print' <def>and <green>'default_colour_name'<def>.")
        self.cprint("The <green>'text_to_print'<def> is self explanitory, it is simply the text you wish to output. \nThe <green>'default_colour_name'<def> is the default colour of the text. Which, unless specified otherwise, is white.\n")
        self.cprint('For example, if I wanted all of my default text to be <orange>orange<def> we can do that simply by changing the default colour. \nLike this: <light blue>Colours.cprint<def>("this is my text", "orange")\n\nThis will output this.')
        self.cprint("this is my text\n", "orange")
        self.cprint("That is all well and good, but how do I colourize only specific bits of text (like in this tutorial text)??")
        print("we can do this easily by adding tags. Tags look like this '<>' and contain a colour.\nSo if I wanted to make some text multiple colours this is how to do it.\n")
        print("cprint('<red>This is red text, <orange>This is orange and <light blue>This is light blue')\n\nThis will output the following")
        self.cprint('<red>This is red text, <orange>This is orange and <light blue>This is light blue\n')
        print("That is basically it, although there is 1 special tag that you will want to take note of and that is the <def> or <default> tag.\nBoth are interchangeable. These tags set the colour back to the specified default colour.\nThey are used just like the tags above. However it will always set the colour back to the default specified when calling 'cprint' insted of a specific colour like <red>.")

        self.cprint("\nOh and 1 last tip, if you want to see all of your colours in your terminal window. You can either call the <light blue>'print_all_colours'<def> function\n or you can just add the <pink>'--display-colours'<def> option when opening the script.\n")
        self.cprint("If you need any more information, check the<pink>'help.txt'<def>file and learn about every function.", "orange")

def create_colour_dict():
    colours = {}

    with open("colours.txt", 'r') as f:
        global COLOUR_DICT

        for line in f.readlines():
            if line.startswith('#') or line.startswith('\n'):
                continue

            colour_name = line[0:line.find(' ')]
            r, g, b = line[line.find('"')+1:line.rfind('"')].replace(' ', '').split(',')

            colours[colour_name] = (r,g,b)
    
    COLOUR_DICT = colours


# Instance the method so the user doesn't have to. (Idea taken from the 'Random' module)
_inst = Colours()
cprint = _inst.cprint
colours_add_custom = _inst.colours_add_custom
print_all_colours = _inst.print_all_colours
print_all_tags = _inst.print_all_tags
help_me_pls = _inst.help_me_pls

if not os.path.isfile(f"{os.getcwd()}/colours.txt"):
    Colours()._create_main_file()

create_colour_dict()
cprint('<red> test <blue> test <b>best</b>')

if __name__ == "__main__":
    pass
    #Creates dictionary with colour names and values.

    #try:
    #    if len(sys.argv) == 2:
    #        if sys.argv[1] == "--help":
    #            print("Avalible commands are:\n '--help' - Displays this dialogue\n '--tags' - Show all valid tags, and what they look like.\n '--palette' - Prints all colours in the terminal, with their respective names. (works with custom colours)\n '--add-colour [name] [r] [g] [b]' - Add a custom RGB colour to your colours file.")
    #        elif sys.argv[1] == "--palette":
    #            print_all_colours()
    #        elif sys.argv[1] == "--tags":
    #            print_all_tags()
    #    elif len(sys.argv) == 6:
    #        if sys.argv[1] == "--add-colour":
    #            custom_colour_name = sys.argv[2]
    #            r, g, b = sys.argv[3:]
    #    else:
    #        cprint(f'[<sblink><b><red>ERROR</b></sblink><def>] "<b><maroon>{sys.argv[1]}</b><def>" is not a valid argument.')
    #        exit(1)
    #except:
    #    cprint(f'[<sblink><b><red>ERROR</b></sblink><def>] You must supply at least 1 argument.')
    #    exit(1)