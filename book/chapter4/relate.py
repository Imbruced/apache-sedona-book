def relate_string_to_table(matrix: str):
    # Labels
    row_labels = ["interior", "boundary", "exterior"]
    col_labels = ["interior", "boundary", "exterior"]

    table = []

    # Header row
    header = [""] + col_labels
    table.append(header)

    idx = 0
    for r in row_labels:
        row = [r]
        for _ in col_labels:
            row.append(matrix[idx])
            idx += 1
        table.append(row)

    col_width = max([len(el) for el in row_labels])

    lines = []
    for r_idx, row in enumerate(table):
        line = "|"
        for c_idx, item in enumerate(row):
            line += f" {str(item).center(col_width)} |"
        lines.append(line)

    return "\n".join(lines)
