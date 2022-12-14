import pandas as pd

# function for returning merged dataframe for a particular seasonal olympics
def preprocess(df, region_df, season):
    # filtering for seasonal olympics and merge with region_df
    df = df[df['Season'] == season]
    df = df.merge(region_df, on='NOC', how='left')

    # dropping duplicates
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df