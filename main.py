import os
import pandas as pd
import random
import datetime as dt
import smtplib

my_email = os.environ.get("MY_EMAIL")
my_password = os.environ.get("MY_PASSWORD")

now = dt.datetime.now()

# 1. Update the birthdays.csv
df = pd.read_csv("birthdays.csv")


# 2. Check if today matches a birthday in the birthdays.csv
mask = (df['month'] == now.month) & (df['day'] == now.day)
matches = df[mask]

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
if not matches.empty:
    with open(f"./letter_templates/letter_{random.randint(1, 3)}.txt", "r") as file2:
        content = file2.read()
    updated_content = content.replace("[NAME]", matches['name'].item())

    # 4. Send the letter generated in step 3 to that person's email address.
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=matches['email'].item(),
            msg=f"Subject:Happy Birthday\n\n{updated_content}"
        )
