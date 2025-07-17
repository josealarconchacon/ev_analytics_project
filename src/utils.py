import os

def save_to_csv(df, filename):
    # Create the output/summaries directory if it doesn't exist
    os.makedirs("output/summaries", exist_ok=True)
    df.to_csv(f"output/summaries/{filename}", index=False)
