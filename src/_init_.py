from .load_data import load_csv
from .create_db import create_db
from .queries import (
    top_ev_makes,
    ev_count_by_year,
    ev_count_by_county,
    avg_electric_range_by_make,
    ev_per_city_within_specific_county,
    ev_dist_by_type_and_cafv,
    top_ev_models_by_range
)
from .dashboard import main as run_dashboard

def run_web_dashboard():
    """Run the Streamlit web dashboard"""
    import streamlit.web.cli as stcli
    import sys
    import os
    
    # Change to the src directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run the dashboard
    sys.argv = ["streamlit", "run", "dashboard.py", "--server.port=8501"]
    sys.exit(stcli.main())

__all__ = [
    'load_csv',
    'create_db',
    'top_ev_makes',
    'ev_count_by_year',
    'ev_count_by_county',
    'avg_electric_range_by_make',
    'ev_per_city_within_specific_county',
    'ev_dist_by_type_and_cafv',
    'top_ev_models_by_range',
    'run_web_dashboard'
]
