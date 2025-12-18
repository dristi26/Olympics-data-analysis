import pandas as pd

# Load datasets


def preprocess(df, region_df):



    # Filter for Summer Olympics
    df = df[df['Season'] == 'Summer']

    # # Rename columns in region_df to avoid conflicts
    # region_df.rename(columns={'region': 'Region', 'notes': 'Notes'}, inplace=True)

    # Merge with region_df to include region information
    df = df.merge(region_df, on='NOC', how='left')

    # Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # One-hot encode the 'Medal' column
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)

    # Return the preprocessed DataFrame
    return df



