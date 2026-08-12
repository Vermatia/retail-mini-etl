"""
Simple ETL pipeline for retail orders data.
"""
import os
import sqlite3
import pandas as pd
from pathlib import Path


def create_sample_data(output_path: str) -> None:
    """Create sample orders.csv if it doesn't exist."""
    if os.path.exists(output_path):
        return
    
    # Create synthetic orders data
    data = {
        'order_id': range(1001, 1031),  # 30 orders
        'order_date': [
            '2024-01-05', '2024-01-10', '2024-01-15', '2024-01-20', '2024-01-25',
            '2024-02-01', '2024-02-05', '2024-02-10', '2024-02-15', '2024-02-20',
            '2024-03-01', '2024-03-05', '2024-03-10', '2024-03-15', '2024-03-20',
            '2024-04-01', '2024-04-05', '2024-04-10', '2024-04-15', '2024-04-20',
            '2024-05-01', '2024-05-05', '2024-05-10', '2024-05-15', '2024-05-20',
            '2024-06-01', '2024-06-05', '2024-06-10', '2024-06-15', '2024-06-20',
        ],
        'product': [
            'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones',
            'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones',
            'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones',
            'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones',
            'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones',
            'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones',
        ],
        'quantity': [
            1, 5, 2, 1, 3,
            2, None, 1, 1, 2,  # Missing quantity in row 7
            1, 4, 2, 1, None,  # Missing quantity in row 15
            2, 6, 3, 1, 2,
            1, None, 2, 2, 4,  # Missing quantity in row 23
            3, 5, 1, 1, 2,
        ],
        'unit_price': [
            999.99, 25.50, 79.99, 299.99, 149.99,
            1099.99, 30.00, 85.50, 349.99, 199.99,
            899.99, 22.99, 75.00, 279.99, 129.99,
            1199.99, 28.75, 82.00, 325.00, 175.50,
            950.00, 26.50, 80.00, 310.00, 155.00,
            1000.00, 32.00, 88.00, 305.00, 165.00,
        ]
    }
    
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✓ Created sample data: {output_path}")


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw orders data:
    - Fill missing quantities with 1
    - Convert quantity to int, unit_price to float
    - Calculate revenue
    """
    df = df.copy()
    
    # Fill missing quantities with 1
    df['quantity'] = df['quantity'].fillna(1)
    
    # Convert types
    df['quantity'] = df['quantity'].astype(int)
    df['unit_price'] = df['unit_price'].astype(float)
    
    # Calculate revenue
    df['revenue'] = df['quantity'] * df['unit_price']
    
    return df


def load_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """Write cleaned data to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✓ Saved to CSV: {output_path}")


def load_to_sqlite(df: pd.DataFrame, db_path: str, table_name: str = 'orders_clean') -> None:
    """Write cleaned data to SQLite database."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    print(f"✓ Saved to SQLite: {db_path} (table: {table_name})")


def print_kpis(df: pd.DataFrame) -> None:
    """Print key performance indicators."""
    total_orders = len(df)
    total_revenue = df['revenue'].sum()
    top_product = df.groupby('product')['revenue'].sum().idxmax()
    top_product_revenue = df.groupby('product')['revenue'].sum().max()
    
    print("\n" + "="*50)
    print("ETL COMPLETE - KEY PERFORMANCE INDICATORS")
    print("="*50)
    print(f"Total Orders: {total_orders}")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Top Product by Revenue: {top_product} (${top_product_revenue:,.2f})")
    print("="*50 + "\n")


def run_etl() -> pd.DataFrame:
    """
    Main ETL pipeline.
    Returns the cleaned dataframe.
    """
    # Extract
    raw_data_path = 'data/raw/orders.csv'
    create_sample_data(raw_data_path)
    
    print(f"✓ Reading from: {raw_data_path}")
    df_raw = pd.read_csv(raw_data_path)
    
    # Transform
    df_clean = transform_data(df_raw)
    
    # Load
    load_to_csv(df_clean, 'data/processed/orders_clean.csv')
    load_to_sqlite(df_clean, 'db/orders.db')
    
    # KPIs
    print_kpis(df_clean)
    
    return df_clean


if __name__ == '__main__':
    run_etl()
