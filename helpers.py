
def append_unl(name):
    return name + ".unl"


def get_id_by_name(node_dict, node_name):
    for node_id in node_dict:
        if node_dict[node_id]["name"] == node_name:
            return node_id
    return None


def wrap_command(text):
    return '\r\n'.join(['enable', text, 'end'])