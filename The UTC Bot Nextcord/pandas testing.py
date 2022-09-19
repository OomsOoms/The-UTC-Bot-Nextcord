
import pandas as pd


mydataset = {
  "log_channel": ["hey", ""],
  "event_1_channel": ["", ""],
  "event_2_channel": ["", ""]
}
"""
mydataset = {
  "discord_id": ["Ooms", "gprime"],
  "solve1": ["10.78", "9.08"]
}

"""

myvar = pd.DataFrame(mydataset)

#myvar.to_csv("channel_config.csv", index=False)

df = pd.read_csv('channel_config.csv')

# data of Player and their performance
data = {
  "log_channel": ["hey", ""],
  "event_1_channel": ["", ""],
  "event_2_channel": ["", ""]
}
 
# Make data frame of above data
df = pd.DataFrame(data)
 
# append data frame to CSV file
df.to_csv('channel_config.csv', mode='a', index=False, header=False)
 
# print message
print("Data appended successfully.")

#print(df.values.tolist())
#print(df)
#print(df["log_channel"])
#count_row = df.shape[0]  # Gives number of rows
#count_col = df.shape[1]  # Gives number of columns
#print(count_row, count_col)

