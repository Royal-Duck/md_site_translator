import sys, os

out_file = "out.html"
theme_path = "theme.css"
default_theme_dot_css =\
'''
* {
    padding : 0;
    margin : 0;
    box-sizing : border-box;
}
'''


def show_help() -> None:
    pass

if len(sys.argv) <= 1:
    show_help()
    raise Exception("not enough arguments to proceed")

def in_tag_content(tag : str, content : str) -> str:
    return f"<{tag}>{content}</{tag}>" if tag != "br" else "<br>"

def html_line(tag : str, ln_content : str, tabs : int, half_tabed : bool, spaced : bool):
    content = ("&emsp;" * tabs)
    content += "&ensp;" if half_tabed else ""
    content += "&nbsp;" if spaced else ""
    return in_tag_content(tag, content + ln_content) + "\n"

def compile_md_to_html(md_file : str) -> None:
    if not os.path.exists(theme_path):
        with open(theme_path, "w") as theme_file:
            theme_file.writelines(default_theme_dot_css)
    output_md_buffer : str =\
f'''
<link rel="stylesheet" type="text/css" href={theme_path}>
<div class="md_translation_content">
'''
    with open(md_file, "r") as source:
        for line_index, line in enumerate(
                    iter(lambda: source.readline(), '')
                ):
            h_value = 0
            # finds the text size <hn> if needed
            for i in range(6):
                if line[:i+1] == ("#" * i)+" ":
                    h_value = i
            if h_value:
                line = line[h_value+1:]
            
            # writes the line to the buffer
            ln_tabs_number : int = 0
            ln_half_tabed : bool = False
            ln_spaced : int = False
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
            
            ln_tag = ""
            if h_value:
                ln_tag = f"h{h_value}"
            elif line == "\n":
                ln_tag = "br"
            else :
                ln_tag = "p"
            output_md_buffer += html_line(ln_tag, line[:-1], ln_tabs_number, ln_half_tabed, ln_spaced)

        # closes the <p> tag
        output_md_buffer += "</div>"
        print(output_md_buffer)
    # TODO : clean this shit
    tmp = open(out_file, "w")
    tmp.writelines(output_md_buffer)

match sys.argv[1]:
    case comp:
        if not os.path.exists(sys.argv[2]):
            raise FileNotFoundError
        compile_md_to_html(sys.argv[2])
