import os
import re
import sys

class Colours:
    # Private Methods
    def __get_background_colour(self, background_colour_name):
        """Gets the RGB value of the background colour.
        
        Returns the string to apply specified background colour."""
        r, g, b = self.__get_rgb_value(background_colour_name)

        return f"\033[48;2;{r};{g}{b}m" #The ANSI escape sequence for the background colour.
    def __get_foreground_colour(self, foreground_colour_name):
        """Gets the RGB value of the colour, and returns the formatted foreground string.
        
        Returns the string to apply specified foreground colour."""
        r, g, b = self.__get_rgb_value(foreground_colour_name)

        return f"\033[38;2;{r};{g};{b}m" #The ANSI escape sequence for the foreground colour.
    def __get_rgb_value(self, our_colour_name):
        """Gets the RGB value of the colour from the 'colours.txt' file.
        
        Returns the R, G, B values in an set."""

        # Removes spaces and sets the text to all caps, for easier comparison.
        our_colour_name = self.__tag_format_name(our_colour_name)

        with open("colours.txt", "r") as f:
            for line in f.readlines():
                if line[0] == "#" or line[0] == None:
                    continue
                # Grab only the name from the file.
                file_colour_name = line[0:line.find(' ')]

                # When we are on the right line, copy the RGB data.
                if file_colour_name == our_colour_name:
                    first_quote = int(line.find('"') + 1)
                    last_quote = int(line.rfind('"'))

                    # Format it as an set for easier unpacking later.
                    rgb_value = line[first_quote:last_quote].replace(' ', '').split(',')

        return rgb_value

    def __is_colour_valid(self, colour_to_check):
        """Checks to see if the colour is in the 'colours.txt' file, 
        
        Returns: bool"""
        # Removes spaces and sets the text to all caps, for easier comparison.
        colour_to_check = self.__tag_format_name(colour_to_check)

        with open("colours.txt", 'r') as f:
            for line in f.readlines():
                # Grab only the name from the file.
                colour_name = line[0:line.find(' ')]

                # If the colour_to_check is in the file, then return true. 
                if colour_to_check == colour_name:
                    return True
                else:
                    continue
        # If colour_to_check is not in the file, then return false.
        return False
    def __is_tag_valid(self, tag_to_check):
            """Compares the tag with an set of valid tags, to see if the tag is valid. 
            
            Returns: bool"""
            tags = ['b', 'ul', 'i', 'blink', 'sblink', 'cross', 'faint', r'/b', r'/ul', r'/i', r'/blink', r'/sblink', r'/cross', r'/faint']
            
            if tag_to_check in tags:
                return True
            else:
                return False

    def __tag_format_name(self, tag):
        """Automatically Formats a tag for a specific purpose, depending what is included in the tag.
        
        Returns the formatted text"""

        if tag.find('<') != -1 or tag.find('>') != -1:
            return tag.replace('<', '').replace('>', '')

        return tag.replace(' ', '').upper()
    def __tag_handle_special(self, text):
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

        # Special Tags Vars (for easier coding)
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

        tags = re.findall(r'\<[\w /]+\>', text)

        for tag in tags:
            tag_name = tag.replace('<', '').replace('>','')

            if self.__is_tag_valid(tag_name) == False:
                del tag
                continue
            
            # Start disgusting elif check, because I have no idea how to optimise it.
            if tag_name == "b" or tag_name == "/b":
                text = text.replace(r'<b>', SETBOLD)
                text = text.replace(r'</b>', UNSETBOLD)
                break

            elif tag_name == "blink" or tag_name == r"/blink":
                text = text.replace(r'<blink>', SETBLINK)
                text = text.replace(r'</blink>', UNSETBLINK)
                break

            elif tag_name == "sblink" or tag_name == r"/sblink":
                text = text.replace(r'<sblink>', SETSLOWBLINK)
                text = text.replace(r'</sblink>', UNSETBLINK)
                break

            elif tag_name == "ul" or tag_name == r"/ul":
                text = text.replace(r'<ul>', SETUNDERLINE)
                text = text.replace(r'</ul>', UNSETUNDERLINE)
                break

            elif tag_name == "i" or tag_name == r"/i":
                text = text.replace(r'<i>', SETITALIC)
                text = text.replace(r'</i>', UNSETITALIC)
                break

            elif tag_name == "cross" or tag_name == r"/cross":
                text = text.replace(r'<cross>', SETCROSSED)
                text = text.replace(r'</cross>', UNSETCROSSED)
                break

            elif tag_name == "faint" or tag_name == r"/faint":
                text = text.replace(r'<faint>', SETFAINT)
                text = text.replace(r'</faint>', UNSETFAINT)
                break

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
        
        if default_colour_name == "DEFAULT":
            default_colour = DEFAULTFG
        else:
            # Setting the default_colour ANSI escape sequence.
            default_r, default_g, default_b = self.__get_rgb_value(default_colour_name)
            default_colour = f"\033[38;2;{default_r};{default_g};{default_b}m"

        tags = re.findall(r'\<[\w ]+\>', text_to_print)

        if not ignore_tags:
            for tag in tags:
                tag_name = self.__tag_format_name(tag) #Removes '<>' from tag.

                if tag_name == "def" or tag_name == "default":
                    text_to_print = text_to_print.replace(f'<{tag_name}>', default_colour)
                    continue
                
                is_valid_colour = self.__is_colour_valid(tag_name)
                is_tag_valid = self.__is_tag_valid(tag_name)

                if not is_valid_colour and not is_tag_valid:
                    print(f"'{tag}' is NOT a valid colour/tag in the list. Please add it, or check the spelling.")
                    return False
                elif is_valid_colour:
                    mask = self.__get_foreground_colour(tag_name) # the ANSI escape sequence for the RGB colour.
                    text_to_print = text_to_print.replace(f"<{tag_name}>", mask)
        
        if background_colour_name == "DEFAULT":
            background_colour = DEFAULTBG
        else:
            background_colour = self.__get_background_colour(background_colour_name)

        text_to_print = self.__tag_handle_special(text_to_print)

        # Concatenate all of the options together, resulting in coloured text that does not effect any other lines.
        print(background_colour + default_colour + text_to_print + RESETALL) 

    def print_all_colours(self):
        """Print every colour from 'colours.txt' into the terminal with relitive name."""
        
        with open("colours.txt", 'r') as f:
            for i,line in enumerate(f.readlines()):
                if line[0] == "#" or line[0] == None or line == "\n":
                    continue
                # Set the 'default colours' header on the first line.
                if i == 7:
                    self.cprint('[<blink>DEFAULT COLOURS</blink>]')
                # Set the custom colours header on the 22nd line.
                elif i == 29:
                    self.cprint('\n[<blink>CUSTOM COLOURS</blink>]')
                colour_name = line[0:line.find(' ')]

                self.cprint(colour_name, colour_name)
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
        
        colour_name = self.__tag_format_name(colour_name)
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

# Instance the method so the user doesn't have to. (Idea taken from the 'Random' module)
_inst = Colours()
cprint = _inst.cprint
colours_add_custom = _inst.colours_add_custom
print_all_colours = _inst.print_all_colours
print_all_tags = _inst.print_all_tags
help_me_pls = _inst.help_me_pls

if not os.path.isfile(f"{os.getcwd()}/colours.txt"):
    Colours()._create_main_file()
    cprint("[<green><b>SUCESS</b><def>] <amber>'colours.txt'<def> created! Coloured text now works!")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            help_me_pls()
        elif sys.argv[1] == "--palette":
            print_all_colours()
        elif sys.argv[1] == "--tags":
            print_all_tags()
    elif len(sys.argv) == 6:
        if sys.argv[1] == "--add-colour":
            custom_colour_name = sys.argv[2]
            r, g, b = sys.argv[3:]
        else:
            cprint(f'[<sblink><b><red>ERROR</b></sblink><def>] "<b><red>{sys.argv[1]}</b><def>" is not a valid argument.')