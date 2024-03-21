def insert_newlines(string: str, every: int = 64) -> str:
    lines = []
    for i in range(0, len(string), every):
        lines.append(string[i: i + every])
    return "\n".join(lines)
