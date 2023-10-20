import pandas as pd

# Sample dataset, for simplicity I'm setting the data here instead of read it from CSV
data = {
    'Investor ID': [1, 2, 3, 4, 5, 6, 7, 2, 3, 4, 6, 7, 7, 7, 6, 1],
    'Syndicate ID': ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 
                     'B', 'B', 'C', 'D', 'E', 'C', 'A'],
    'Transaction Amount': [1000, 1500, 1300, 1400, 1000, 2000, 3000, 
                           5000, 7000, 7000, 1000, 3000, 4000, 5000, 
                           9000, 9000],
    'Transaction Date': ['2023-01-01', '2023-02-15', '2023-03-20', 
                         '2023-04-10', '2023-01-05', '2023-02-18', 
                         '2023-03-25', '2023-04-15', '2023-05-01', 
                         '2023-05-18', '2023-05-12', '2023-05-21', 
                         '2022-05-11', '2023-01-01', '2023-03-01', 
                         '2023-08-01']
}

df = pd.DataFrame(data)
# 'Transaction Date' column string to datetime format
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
# Group by Investor ID and count unique Syndicate IDs
investor_counts = df.groupby('Investor ID')['Syndicate ID'].nunique()
# Sort the investors by the number of unique syndicates in descending order
investor_counts = investor_counts.sort_values(ascending=False)
# Get the top 5 investors
top_investors = investor_counts.head(5)
# Calculate the total amount invested for each of the top investors
total_investment = df[df['Investor ID'].isin(top_investors.index)].groupby('Investor ID')['Transaction Amount'].sum()
# Convert series to dataframe to prepare the result
df_new = top_investors.reset_index()
# Now prepare final result. We converted the series top_investors to data frame df_new and now merge that with the
# series total_investment based on the Investor ID. This will be our final result
result = df_new.merge(total_investment, left_on='Investor ID', right_index=True)
# Print
print(result)