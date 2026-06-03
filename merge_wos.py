from pathlib import Path
import pandas as pd
import re


def read_wos_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:

        header = f.readline().rstrip("\n").split("\t")
        ncols = len(header)

        rows = []

        for lineno, line in enumerate(f, start=2):

            fields = line.rstrip("\n").split("\t")

            # WoS Fast5000 exports contain one extra empty field at the end
            if len(fields) == ncols + 1:
                fields = fields[:-1]

            if len(fields) != ncols:
                print(
                    f"Warning: {path.name}:{lineno} "
                    f"has {len(fields)} columns "
                    f"(expected {ncols}). Skipped."
                )
                continue

            rows.append(fields)

    return pd.DataFrame(rows, columns=header)


def discover_files():

    files = []

    # First Fast5000 export
    base_file = Path("savedrecs.txt")

    if base_file.exists():
        files.append(base_file)

    # Following Fast5000 exports
    numbered_files = []

    for p in Path(".").glob("savedrecs*.txt"):

        m = re.search(r"\((\d+)\)", p.name)

        if m:
            numbered_files.append(
                (int(m.group(1)), p)
            )

    numbered_files.sort(key=lambda x: x[0])

    files.extend(
        p for _, p in numbered_files
    )

    return files


def main():

    files = discover_files()

    if not files:
        raise FileNotFoundError(
            "No savedrecs.txt or savedrecs (n).txt files found."
        )

    print("Files to merge:")

    for f in files:
        print("  ", f.name)

    dfs = []

    for file in files:

        print(f"Reading {file.name}")

        dfs.append(
            read_wos_file(file)
        )

    df = pd.concat(
        dfs,
        ignore_index=True
    )

    print(f"\nMerged records: {len(df):,}")

    if "UT" in df.columns:

        before = len(df)

        df = df.drop_duplicates(
            subset="UT",
            keep="first"
        )

        print(
            f"Removed duplicates: {before - len(df):,}"
        )

        print(
            f"Final records: {len(df):,}"
        )

    output_file = "wos_all.parquet"

    df.to_parquet(
        output_file,
        engine="pyarrow",
        compression="snappy",
        index=False
    )

    print(f"\nSaved: {output_file}")


if __name__ == "__main__":
    main()