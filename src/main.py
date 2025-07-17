from load_data import load_csv
from create_db import create_db
from queries import top_ev_makes, ev_count_by_year, ev_count_by_county, avg_electric_range_by_make
from plots import plot_bar, plot_line
from utils import save_to_csv

# Load data
df = load_csv("data/ev_data.csv")

# Create DB and load table
conn = create_db(df)

# Run Queries
df_makes = top_ev_makes(conn)
df_years = ev_count_by_year(conn)
df_country = ev_count_by_county(conn)
df_range = avg_electric_range_by_make(conn)

# Save Results
save_to_csv(df_makes, "top_ev_makes.csv")
save_to_csv(df_years, "ev_by_year.csv")
save_to_csv(df_country, "ev_by_county.csv")
save_to_csv(df_range, "avg_electric_range_by_make.csv")

# Create Plots
plot_bar(df_makes, "Make", "total", "Top 5 EV Manufacturers", "top_ev_makes.png")
plot_line(df_years, "Year", "EV_Count", "EV Count by Year", "ev_by_year.png")
plot_bar(df_country, "County", "EV_Count", "EV Count by County", "ev_by_country.png")
plot_bar(df_range, "Make", "Avg_Range", "Average Electric Range by Make", "avg_electric_range_by_make.png")

print("Analysis complete. Check the output/ folder.")
