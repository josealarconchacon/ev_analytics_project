import pandas as pd

def top_ev_makes(conn):
    return pd.read_sql_query("""
        SELECT Make, COUNT(*) as total
        FROM ev_population
        GROUP BY Make
        ORDER BY total DESC
        LIMIT 5;
    """, conn)

def ev_count_by_year(conn):
    return pd.read_sql_query("""
        SELECT "Model Year" AS Year, COUNT(*) AS EV_Count
        FROM ev_population
        GROUP BY Year
        ORDER BY Year;
    """, conn)


def ev_count_by_county(conn):
    return pd.read_sql_query("""
        SELECT County, COUNT(*) AS EV_Count
        FROM ev_population
        GROUP BY County
        ORDER BY EV_Count DESC;
    """, conn)

def avg_electric_range_by_make(conn):
    return pd.read_sql_query("""
        SELECT Make, AVG("Electric Range") AS Avg_Range
        FROM ev_population
        WHERE "Electric Range" > 0
        GROUP BY Make
        ORDER BY Avg_Range DESC
        LIMIT 10;
    """, conn)
    
def ev_per_city_within_specific_county(conn):
    return pd.read_sql_query("""
        SELECT City, COUNT(*) AS Count
        FROM ev_population
        WHERE County IN ('King', 'Pierce', 'Snohomish', 'Spokane')
        GROUP BY City
        ORDER BY Count DESC
        LIMIT 20;
    """, conn)