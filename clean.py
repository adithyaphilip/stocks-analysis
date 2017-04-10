import parse


def clean(csv_name):
    with open(csv_name, "r") as f:
        header = None
        rows = []
        for line in f.readlines():
            line = line.strip()
            if header is None:
                header = line
            elif line != header:
                rows.append(line)
    if header is None:
        return
    with open(csv_name, "w") as f:
        f.write(header + "\n")
        for line in rows:
            f.write(line + "\n")


if __name__ == '__main__':
    for symbol in parse.get_symbols_to_fetch():
        clean("csv/" + symbol + ".csv")
