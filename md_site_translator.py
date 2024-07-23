import sys, os

# ===== SETUP PATH RELATED STUFF =====
real_file_dir : str = os.path.dirname(os.path.abspath(__file__)) # location of the directory containing the file on the machine
working_dir : str = os.getcwd() # location of the directory the command is executed from

## loads the theme used if no other theme is provided
default_theme_dot_css : str = ""
with open(f"{real_file_dir}/default_theme.css", "r") as default_theme:
    default_theme_dot_css = default_theme.readlines()

out_file : str = f"{working_dir}/out.html" # default output file
theme_path : str = f"{working_dir}/theme.css" # default theme file
# ====================================

def show_help() -> None: # basic help menu
    pass

if len(sys.argv) <= 1: # checks if arguments are provided
    print("\033[0;31mNOT ENOUGH ARGUMENTS TO USE RoyalWebsite")
    show_help()
    exit()

# ===== HTML FORMATING FUNCTIONS =====
def in_tag_content(tag : str, content : str) -> str:
    return f"<{tag}>{content}</{tag}>" if tag != "br" else "<br>"

def html_line(tag : str, ln_content : str, tabs : int, half_tabed : bool, spaced : bool):
    content = ("&emsp;" * tabs)
    content += "&ensp;" if half_tabed else ""
    content += "&nbsp;" if spaced else ""
    return in_tag_content(tag, content + ln_content) + "\n"
# ====================================

def compile_md_to_html(md_file : str) -> None: # main function of the program
    # checks that the file passed is valid
    if not os.path.exists(working_dir + "/" + md_file):
        raise FileNotFoundError(md_file)

    # if the theme doesn't exist, create it with the default value from above
    if not os.path.exists(theme_path):
        with open(theme_path, "w") as theme_file:
            theme_file.writelines(default_theme_dot_css)
   
    # initialize the buffer that will contain the HTML code
    output_HTML_buffer : str = f'''
    \r<link rel="stylesheet" type="text/css" href={theme_path}>
    \r<div class="md_translation_content">'''
    
    with open(md_file, "r") as source:
        for line in source.readlines():
####################################################################### REFORMATED UNTIL HERE            
            h_value = 0
            blockquote_value = 0
            # finds the text size <hn> if needed
            for i in range(4):
                if line[:i+1] == (">" * i)+" ":
                    blockquote_value = i
            if blockquote_value:
                line = line[blockquote_value+1:]
            for i in range(7):
                if line[:i+1] == ("#" * i)+" ":
                    h_value = i
            if h_value:
                line = line[h_value+1:]
            
            
            # writes the line to the buffer
            ln_tabs_number : int = 0
            ln_half_tabed : bool = False
            ln_spaced : bool = False
            while line [0] == "\t":
                line = line[1:]
                ln_tabs_number += 1
            while line[0:4] == "    ":
                line = line[4:]
                ln_tabs_number += 1
            if line[0:2] == "  ":
                line = line[2:]
                ln_half_tabed = True
            if line[0] == " ":
                line = line[1:]
                ln_spaced = True
            
            ln_already_compiled : bool = False
            if line[:2] == "![":
                expr : list[str] = line.split("]")
                image_alt = expr[0][2:]
                image_link = expr[1].split(")")[0][1:]
                ln_already_compiled = True
                result = f"<img src=\"{image_link}\" alt=\"{image_alt}\"></img>\n"

            if line[0] == "[" and "](" in line:
                expr = line.split("]")
                link_name = expr[0][1:]
                link_link = expr[1].split(")")[0][1:]
                ln_already_compiled = True
                result = f"<a href=\"{link_link}\">{link_name}</a>"
            
            if (line[:3] == "___"\
                  or line[:3] == "***"\
                  or line[:3] == "---") and\
                ln_half_tabed+ln_tabs_number+ln_spaced == 0:
                line_not_rule : bool = False
                for char in line :
                    ln_tag = "p"
                    if not (char == line[0] or char == "\n"):
                        line_not_rule = True
                if not line_not_rule:
                    result = "<span class=\"horizontal_rule\"></span>\n"
                    ln_already_compiled = True
            
            if not ln_already_compiled:
                ln_tag = ""
                if h_value:
                    ln_tag = f"h{h_value}"
                elif line == "\n":
                    ln_tag = "br"
                else :
                    ln_tag = "p"
                result = html_line(ln_tag, line[:-1], ln_tabs_number, ln_half_tabed, ln_spaced)
            for i in range(blockquote_value):
                result = in_tag_content("blockquote", result[:-1])+"\n"

            output_HTML_buffer += result


        # closes the <p> tag
        output_HTML_buffer += "</div>"
        print(output_HTML_buffer)
    # TODO : clean this shit
    tmp = open(out_file, "w")
    tmp.writelines(output_HTML_buffer)

match sys.argv[1]:
    case comp:
        if not os.path.exists(sys.argv[2]):
            raise FileNotFoundError
        compile_md_to_html(sys.argv[2])
