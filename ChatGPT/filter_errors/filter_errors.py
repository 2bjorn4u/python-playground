import argparse,sys

def extract_matching_lines(source_path: str, target_path: str, keyword: str) -> int:
    """
    Reads lines from source_path, writes those containing keyword to target_path,
    and returns the number of matches.
    """
    keyword_count = 0
    with open(source_path, "r",encoding="utf-8") as src, open(target_path, "w", encoding="utf-8") as dst:
        for line in src:
            if keyword in line:
                dst.write(line)
                keyword_count += 1
    return keyword_count

def main():
    # 1. Create the parser

    parser = argparse.ArgumentParser(
        description="Filter lines from a log file by keyword."
    )

    # 2. Add arguments

    # Positional arguments (optional with defaults)

    parser.add_argument(
        "source",
        nargs="?",
        default="app.log",
        help="Source log file (default: app.log)"
    )
    
    parser.add_argument(
        "target",
        nargs="?",
        default="errors.log",
        help="Destination file for filtered lines (default: errors.log)"
    )

    # Optional argument with flag

    parser.add_argument(
        "-k", "--keyword",
        default="ERROR",
        help="Keyword to filter by (default: ERROR)"
    )

    # 3. Parse arguments

    args = parser.parse_args()

    # 4. Call the function

    try:
        count = extract_matching_lines(args.source, args.target, args.keyword)
    except FileNotFoundError:
        print(f"Unable to find the source-file ('{args.source}').", file=sys.stderr)
        sys.exit(1)

    # 5. Print summary

    print(f"Filtered {count} lines containing '{args.keyword}' into {args.target}")

if __name__ == "__main__":
    main()