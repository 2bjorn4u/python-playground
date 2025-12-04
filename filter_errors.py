def extract_matchines_lines(source_path: str, target_path: str, keyword: str) -> int:
    keyword_count = 0
    with open(source_path, "r") as src, \
        open(target_path, "w") as dst:
        for line in src:
            if keyword in line:
                dst.write(line)
                keyword_count += 1
    return keyword_count

extract_matchines_lines()



with open("app.log", "r") as src, \
    open("errors.log", "w+") as dst:

    for line in src:
        if "ERROR" in line:
            dst.write(line)
    dst.seek(0)
    for line in dst:
        print(line, end="")