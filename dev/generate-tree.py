import shutil


def wrap_sequence(
    prefix: str,
    connector: str,
    key: str,
    seq_list: list[str],
    have_children: bool,
    desc="",
):
    """Builds wrapped text lines for a tree node with optional sequence and description.
    Args:
        prefix (str): The prefix for the current tree level (indentation + connectors).
        connector (str): The connector symbol linking the node to its parent (e.g., "├──" or "└──").
        key (str): The name of the current node.
        seq_list (list[str]): A list of elements to display on the same line as the key.
        have_children (bool): Whether the node has child elements.
        desc (str, optional): Description text to display on the right side of the node. Defaults to "".
    Returns:
        list[str]: A list of formatted strings representing this node and its wrapped lines.
    """

    # Init term dimentions
    term_width = shutil.get_terminal_size().columns
    desc_width = 2 * term_width // 5
    max_width = term_width - desc_width

    # Init variable for code
    desc_split = wrap_desc(desc, desc_width)
    base_line = f"{prefix}{connector} {key}"
    wrap_connector = "│   " if connector == "├──" else "    "
    if have_children:
        wrap_connector += "│"
    indent = " " * (len(base_line) + 1 - len(prefix + wrap_connector))
    lines = []
    current_line = base_line

    # Check if we can append each elt on one line
    for elem in seq_list:
        elem_str = f" {elem}"
        if len(current_line) + len(elem_str) > max_width - 1:
            # Create a line with this content and we will create a new
            if desc_split:  # add desc
                spaces = " " * (max_width - len(current_line))
                current_line += f"{spaces}{desc_split.pop(0)}"
            lines.append(current_line)
            current_line = (
                prefix + wrap_connector + indent + elem.strip()
            )  # create new line
        else:
            # Can spread on one line
            current_line += elem_str

    # Last line
    if desc_split:
        spaces = " " * (max_width - len(current_line))
        current_line += f"{spaces}{desc_split.pop(0)}"
    lines.append(current_line)
    for line_desc in desc_split:
        spaces = " " * ((max_width) - len(prefix + wrap_connector))
        lines.append(prefix + wrap_connector + spaces + line_desc)

    return lines


def wrap_desc(desc: str, desc_width: int):

    words = desc.split(" ")
    lines = []
    current_line = ""
    for word in words:
        # +1 for the space between words if it's not the first word in the line
        extra_len = len(word) + (1 if current_line else 0)
        if len(current_line) + extra_len > desc_width:
            # Line is full -> append it to lines
            lines.append(current_line)
            # For subsequent lines, add indentation
            current_line = "  " + word
        else:
            # Add the word to the current line
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def build_lines(dict_cmd: dict, prefix=""):

    lines = []
    items = list(dict_cmd.items())
    for i, (key, value) in enumerate(items):
        connector = "└──" if i == len(items) - 1 else "├──"
        seq_list = value.get("__seq__", [])
        desc = value.get("__desc__", "")
        children = {
            k: v
            for k, v in value.items()
            if isinstance(v, dict) and k not in ("__seq__", "__desc__")
        }
        if desc:
            desc = "# " + desc
        wrapped_lines = wrap_sequence(
            prefix, connector, key, seq_list, children != {}, desc
        )
        lines.extend(wrapped_lines)
        if children:
            extension = "    " if i == len(items) - 1 else "│   "
            lines.extend(build_lines(children, prefix + extension))
    return lines


def print_tree(dict_cmd):
    lines = build_lines(dict_cmd)
    for line in lines:
        print(line)


def main(cmd):
    print_tree(cmd)
