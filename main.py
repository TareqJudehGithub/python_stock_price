import requests
import smtplib

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Vantage API details:
STOCK_API = "CMY831W7XEGQXU0Y"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
parameters = {
    "apikey": STOCK_API,
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME
}

# News API:
NEWS_API = "aa8144f4fa54488e9f9e5742be375084"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get(url=STOCK_ENDPOINT, params=parameters)
print(response.status_code, "\n")
response.raise_for_status()
stock_data = response.json()


# TODO 1. - Get yesterday's closing stock price:
daily_data = stock_data["Time Series (Daily)"]
data_list = [v for (k, v) in daily_data.items()]
yesterday_data = data_list[0]
yesterday_closing = yesterday_data["4. close"]
print(yesterday_closing)
# TODO 2. - Get the day before yesterday's closing stock price
day_before = data_list[1]
day_before_closing = day_before["4. close"]
print(day_before_closing)

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = round(abs(float(yesterday_closing) - float(day_before_closing)), 2)
print(difference)

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = difference / float(yesterday_closing) * 100
print(f"{round(diff_percent, 2)}%")

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if diff_percent > 1:
    print("Great News!")


    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if diff_percent > 1:
    NEWS_params = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(
        url=NEWS_ENDPOINT,
        params=NEWS_params
    )
    articles_data = news_response.json()["articles"]

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
three_articles = articles_data[:3]




    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"Headline: {article['title']} \nBrief: {article['description']}" for article in three_articles]
#TODO 9. - Send each article as a separate message via Twilio.
# Send Email:
for article in formatted_articles:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user="tj.coder1975@gmail.com", password="BlueOcean75@")
        connection.sendmail(
            from_addr="tj.coder1975@gmail.com",
            to_addrs="tareq.joudeh@gmail.com",
            msg="Subject:Stock Update!\n\n"
                f"{article}".encode("utf8")
        )

#Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

