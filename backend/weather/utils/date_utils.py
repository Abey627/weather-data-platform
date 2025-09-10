"""
Date utility functions
"""
from datetime import datetime, timedelta

def get_date_range(days_back):
    """
    Calculate start and end date based on the number of days back from today
    
    Args:
        days_back (int): Number of days to go back from today
        
    Returns:
        tuple: (start_date, end_date) both as date objects
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date
