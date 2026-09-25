from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd


BASE_URL = (
    "https://wwwn.cdc.gov/Nchs/Data/Nhanes/"
    "Public/2017/DataFiles"
)

FILES = [
    "P_DEMO",
    "P_BMX",
    "P_BPXO",
    "P_LUX",
    "P_HDL",
    "P_TRIGLY",
    "P_GLU",
    "P_DIQ",
]

OUT_DIR = Path("../data/raw/2017-2020")
OUT_DIR.mkdir(parents=True, exist_ok=True)


for name in FILES:
    path = OUT_DIR / f"{name}.xpt"
    url = f"{BASE_URL}/{name}.XPT"

    if path.exists():
        print(f"{name}: already exists")
        continue

    print(f"{name}: downloading...")
    urlretrieve(url, path)


# Example: load one downloaded file
demo = pd.read_sas(
    OUT_DIR / "P_DEMO.xpt",
    format="xport",
)

print(demo.shape)
print(demo.head())
