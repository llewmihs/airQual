import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta, timezone
import matplotlib.backends.backend_pdf
from creds.py import api_url

# Set the plot style using seaborn
sns.set_style("darkgrid")

# Fetch data from the API
response = requests.get(api_url)
data = response.json()

# Extract historical daily data
daily_data = data["historical"]["daily"]

# Extract data for p1_sum, p2_sum, and dates
p1_sum = [day["p1_sum"] for day in daily_data]
p2_sum = [day["p2_sum"] for day in daily_data]
dates = [day["ts"] for day in daily_data]

# Convert date strings to datetime objects
dates = [datetime.fromisoformat(date.replace("Z", "+00:00")) for date in dates]

# Get the last week and last month data
one_week_ago = datetime.now(timezone.utc) - timedelta(weeks=1)
one_month_ago = datetime.now(timezone.utc) - timedelta(weeks=4)

last_week_indices = [i for i, date in enumerate(dates) if date >= one_week_ago]
last_month_indices = [i for i, date in enumerate(dates) if date >= one_month_ago]

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Plot last week data
ax1.plot([dates[i] for i in last_week_indices], [p1_sum[i] for i in last_week_indices], label="p1_sum")
ax1.plot([dates[i] for i in last_week_indices], [p2_sum[i] for i in last_week_indices], label="p2_sum")
ax1.set_title("Last Week")
ax1.set_xlabel("Date")
ax1.set_ylabel("Value")
ax1.legend()
ax1.tick_params(axis="x", rotation=90)

# Plot last month data
ax2.plot([dates[i] for i in last_month_indices], [p1_sum[i] for i in last_month_indices], label="p1_sum")
ax2.plot([dates[i] for i in last_month_indices], [p2_sum[i] for i in last_month_indices], label="p2_sum")
ax2.set_title("Last Month")
ax2.set_xlabel("Date")
ax2.set_ylabel("Value")
ax2.legend()
ax2.tick_params(axis="x", rotation=90)

# Save the plot to a PDF
pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
pdf.savefig(fig, bbox_inches="tight")
pdf.close()

plt.show()