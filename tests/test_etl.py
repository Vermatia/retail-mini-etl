"""
Unit tests for the ETL pipeline.
Run with: pytest tests/ -v
"""
import os
import pandas as pd
import pytest
from src.etl import transform_data, create_sample_data


@pytest.fixture
def sample_raw_data():
    """Create sample raw data for testing."""
    return pd.DataFrame({
        'order_id': [1, 2, 3, 4],
        'order_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
        'quantity': [1, None, 2, None],  # Missing values
        'unit_price': [999.99, 25.50, 79.99, 299.99]
    })


def test_revenue_column_exists_and_non_negative(sample_raw_data):
    """Test that revenue column exists and all values are non-negative."""
    df_clean = transform_data(sample_raw_data)
    
    # Check revenue column exists
    assert 'revenue' in df_clean.columns, "Revenue column should exist"
    
    # Check all revenue values are non-negative
    assert (df_clean['revenue'] >= 0).all(), "All revenue values should be non-negative"
    
    # Verify revenue calculation
    assert df_clean.loc[0, 'revenue'] == 999.99 * 1
    assert df_clean.loc[1, 'revenue'] == 25.50 * 1  # Filled with 1


def test_missing_quantity_filled_with_one(sample_raw_data):
    """Test that missing quantities are filled with 1."""
    df_clean = transform_data(sample_raw_data)
    
    # Check no missing values in quantity
    assert df_clean['quantity'].isna().sum() == 0, "No missing quantities should remain"
    
    # Verify missing values were filled with 1
    # Row 1 (index 1) had None, should be 1
    assert df_clean.loc[1, 'quantity'] == 1, "Missing quantity should be filled with 1"
    
    # Row 3 (index 3) had None, should be 1
    assert df_clean.loc[3, 'quantity'] == 1, "Missing quantity should be filled with 1"
    
    # Verify non-missing values remain unchanged
    assert df_clean.loc[0, 'quantity'] == 1
    assert df_clean.loc[2, 'quantity'] == 2
