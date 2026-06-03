# WoS Fast5000 Merger

Merge Web of Science Fast 5000 export files into a single Parquet file.

## Features

* Merge multiple WoS Fast 5000 export files
* Preserve original record order
* Remove duplicate records using `UT`
* Export to a single compressed Parquet file
* Keep all original WoS fields

## Requirements

```bash
pip install pandas pyarrow
```

## Supported Files

The script supports the standard Web of Science Fast 5000 export naming scheme:

```text
savedrecs.txt
savedrecs (1).txt
savedrecs (2).txt
...
savedrecs (n).txt
```

Files are processed in the following order:

```text
savedrecs.txt
savedrecs (1).txt
savedrecs (2).txt
...
savedrecs (n).txt
```

The original record order inside each file is preserved.

Numbered files do not need to be continuous.

Example:

```text
savedrecs.txt
savedrecs (3).txt
savedrecs (7).txt
savedrecs (20).txt
```

## Usage

Place all export files and the script in the same directory:

```text
savedrecs.txt
savedrecs (1).txt
savedrecs (2).txt
...
merge_wos.py
```

Run:

```bash
python merge_wos.py
```

Output:

```text
wos_all.parquet
```

## Notes

* Designed for Web of Science tab-delimited Fast 5000 exports.
* Duplicate records are identified by the `UT` field.
* The first occurrence of a duplicated `UT` is kept.
* All original WoS columns are retained.
* The script is not intended for BibTeX, EndNote, CSV, Excel, or other WoS export formats.
