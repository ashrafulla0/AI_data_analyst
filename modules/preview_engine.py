import pandas as pd
import numpy as np


class PreviewEngine:
    """
    Executes ETL operations on a COPY of dataframe.
    Original dataframe is NEVER modified.
    """

    def __init__(self, df):

        self.original_df = df.copy(deep=True)
        self.preview_df = df.copy(deep=True)

        self.summary = []
        self.stats = {}

    # -----------------------------------------------------

    def remove_duplicates(self):

        before = len(self.preview_df)

        self.preview_df = self.preview_df.drop_duplicates()

        removed = before - len(self.preview_df)

        self.summary.append({
            "operation": "Remove Duplicates",
            "affected_rows": removed,
            "status": "Success"
        })

    # -----------------------------------------------------

    def fill_missing(self, method="median"):

        filled = 0

        numeric_cols = self.preview_df.select_dtypes(
            include=np.number
        ).columns

        for col in numeric_cols:

            missing = self.preview_df[col].isna().sum()

            if missing == 0:
                continue

            filled += missing

            if method == "median":
                value = self.preview_df[col].median()

            elif method == "mean":
                value = self.preview_df[col].mean()

            else:
                value = 0

            self.preview_df[col] = self.preview_df[col].fillna(value)

        self.summary.append({

            "operation": "Fill Missing Values",

            "affected_cells": filled,

            "status": "Success"

        })

    # -----------------------------------------------------

    def convert_dates(self):

        converted = 0

        for col in self.preview_df.columns:

            if "date" in col.lower():

                before = self.preview_df[col].copy()

                self.preview_df[col] = pd.to_datetime(
                    self.preview_df[col],
                    errors="coerce"
                )

                changed = (
                    before.astype(str)
                    != self.preview_df[col].astype(str)
                ).sum()

                converted += changed

        self.summary.append({

            "operation": "Convert Dates",

            "affected_cells": converted,

            "status": "Success"

        })

    # -----------------------------------------------------

    def rename_column(self, old, new):

        if old in self.preview_df.columns:

            self.preview_df.rename(
                columns={old: new},
                inplace=True
            )

            self.summary.append({

                "operation": "Rename Column",

                "column": old,

                "new_name": new,

                "status": "Success"

            })

        else:

            self.summary.append({

                "operation": "Rename Column",

                "column": old,

                "new_name": new,

                "status": "Failed",

                "reason": "Column not found"

            })
        # -----------------------------------------------------

    def drop_column(self, column):

        if column in self.preview_df.columns:

            self.preview_df.drop(
                columns=[column],
                inplace=True
            )

            self.summary.append({

                "operation": "Drop Column",

                "column": column,

                "status": "Success"

            })

        else:

            self.summary.append({

                "operation": "Drop Column",

                "column": column,

                "status": "Failed",

                "reason": "Column not found"

            })
        # -----------------------------------------------------

    def split_column(self, column):
        if column not in self.preview_df.columns:
            self.summary.append({
                "operation": "Split Column",
                "column": column,
                "status": "Failed",
                "reason": "Column not found"
            })

            return

        cols = list(self.preview_df.columns)

        idx = cols.index(column)

        if idx == len(cols) - 1:
            self.summary.append({
                "operation": "Split Column",
                "column": column,
                "status": "Failed",
                "reason": "No next column exists"
            })

            return
        next_col = cols[idx + 1]

        split_data = (
            self.preview_df[column]
            .astype(str)
            .str.split(" ", n=1, expand=True)
        )

        self.preview_df[column] = split_data[0]
        if len(split_data.columns) > 1:
            self.preview_df[next_col] = split_data[1]

        self.summary.append({
            "operation": "Split Column",
            "column": column,
            "status": "Success"
        })

    # -----------------------------------------------------

    # -----------------------------------------------------

    def create_column(self, new_col, formula):
        try:
            import re

        # Wrap columns containing spaces with backticks
            for col in sorted(self.preview_df.columns, key=len, reverse=True):
                if " " in col:
                    formula = formula.replace(col, f"`{col}`")

                self.preview_df[new_col] = self.preview_df.eval(formula)

                self.summary.append({
                    "operation": "Create Column",

                    "column": new_col,
                    "formula": formula,

                    "status": "Success"

                })

        except Exception as e:
            self.summary.append({
                "operation": "Create Column",

                "column": new_col,
                "formula": formula,

                "status": "Failed",

                "reason": str(e)

            })
    def group_by(self, group_column, agg_column, operation="sum"):
        try:
            if operation == "sum":
                grouped = self.preview_df.groupby(group_column, as_index=False)[agg_column].sum()

            elif operation == "mean":
                grouped = self.preview_df.groupby(group_column, as_index=False)[agg_column].mean()

            elif operation == "count":
                grouped = self.preview_df.groupby(group_column, as_index=False)[agg_column].count()

            elif operation == "max":
                grouped = self.preview_df.groupby(group_column, as_index=False)[agg_column].max()

            elif operation == "min":
                grouped = self.preview_df.groupby(group_column, as_index=False)[agg_column].min()

            else:
                grouped = self.preview_df.groupby(group_column, as_index=False)[agg_column].sum()
            self.preview_df = grouped

            self.summary.append({
                "operation": "Group By",
                "group_column": group_column,
                "aggregation": operation,
                "value_column": agg_column,
                "status": "Success"
            })

        except Exception as e:
            self.summary.append({
                "operation": "Group By",
                "status": "Failed",
                "reason": str(e)
            })
    # -----------------------------------------------------

    def filter_rows(self, condition):
        try:
            before = len(self.preview_df)

            self.preview_df = self.preview_df.query(condition)

            after = len(self.preview_df)

            self.summary.append({
                "operation": "Filter Rows",

                "condition": condition,

                "rows_removed": before - after,

                "status": "Success"

            })

        except Exception as e:
            self.summary.append({
                "operation": "Filter Rows",

                "condition": condition,

                "status": "Failed",

                "reason": str(e)

            })
    
    # -----------------------------------------------------

    def statistics(self):

        self.stats = {

            "rows_before": len(self.original_df),

            "rows_after": len(self.preview_df),

            "columns_before": len(self.original_df.columns),

            "columns_after": len(self.preview_df.columns),

            "missing_before": int(
                self.original_df.isna().sum().sum()
            ),

            "missing_after": int(
                self.preview_df.isna().sum().sum()
            ),

            "duplicates_before": int(
                self.original_df.duplicated().sum()
            ),

            "duplicates_after": int(
                self.preview_df.duplicated().sum()
            )

        }

        return self.stats

    # -----------------------------------------------------

    def get_preview(self):

        return {

            "original_df": self.original_df,

            "preview_df": self.preview_df,

            "summary": self.summary,

            "statistics": self.statistics()

        }
    def merge_columns(self, col1, col2, new_col=None):
        if col1 not in self.preview_df.columns:
            return

        if col2 not in self.preview_df.columns:
            return

        if new_col is None:
            new_col = col1

        self.preview_df[new_col] = (
            self.preview_df[col1].astype(str)
            + " "
            + self.preview_df[col2].astype(str)
        )

        if new_col != col1:
            self.preview_df.drop(columns=[col1], inplace=True)
        self.preview_df.drop(columns=[col2], inplace=True)
        self.summary.append({
            "operation": "Merge Columns",
            "column1": col1,
            "column2": col2,
            "new_column": new_col,
            "status": "Success"
        })
    
    # -----------------------------------------------------

    def replace_value(self, old_value, new_value):
        count = (
            self.preview_df.astype(str)
            .eq(str(old_value))
            .sum()
            .sum()
        )

        self.preview_df = self.preview_df.replace(
            old_value,
            new_value
        )

        self.summary.append({
            "operation": "Replace Value",

            "old_value": old_value,

            "new_value": new_value,

            "affected_cells": int(count),

            "status": "Success"
        })
    # -----------------------------------------------------

    def change_dtype(self, column, dtype):
        if column not in self.preview_df.columns:
            self.summary.append({
                "operation": "Change Data Type",

                "column": column,

                "status": "Failed",

                "reason": "Column not found"
            })

            return

        try:
            dtype = dtype.lower()
            if dtype in ["int", "integer"]:
                self.preview_df[column] = (
                    pd.to_numeric(
                        self.preview_df[column],
                        errors="coerce"
                    ).astype("Int64")
                )

            elif dtype in ["float", "double"]:
                self.preview_df[column] = pd.to_numeric(
                    self.preview_df[column],
                    errors="coerce"
                )

            elif dtype in ["string", "text"]:
                self.preview_df[column] = (
                    self.preview_df[column]
                    .astype(str)
                )

            elif dtype in ["datetime", "date"]:
                self.preview_df[column] = pd.to_datetime(
                    self.preview_df[column],
                    errors="coerce"
                )

                self.summary.append({
                    "operation": "Change Data Type",

                    "column": column,

                     "new_type": dtype,

                     "status": "Success"

                })

        except Exception as e:
            self.summary.append({
                "operation": "Change Data Type",

                "column": column,

                "status": "Failed",

                 "reason": str(e)

            })