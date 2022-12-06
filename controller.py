import old
from pathlib import Path
import pandas as pd

old.olx()
old.ob()
old.izi()
old.kidstaff()


path = Path("C:/Users/shifu/Desktop/Манн/дорогой дневник/excel/")
min_excel_file_size = 4

df = pd.concat([pd.read_excel(f)
                for f in path.glob("*.xlsx")
                if f.stat().st_size >= min_excel_file_size],
               ignore_index=True)

df.to_excel('C:/Users/shifu/Desktop/Манн/дорогой дневник/excel/final.xlsx', index=False)
