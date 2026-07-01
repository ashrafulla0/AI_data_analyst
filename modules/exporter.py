import pandas as pd
from io import BytesIO


def export_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Dataset"
        )

    output.seek(0)

    return output.getvalue()