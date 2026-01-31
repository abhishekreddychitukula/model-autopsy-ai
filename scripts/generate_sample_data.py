# Sample Test Data Generator for Model Autopsy AI

import pandas as pd
import numpy as np

def generate_sample_data():
    """Generate sample CSV files for testing"""
    
    np.random.seed(42)
    n_samples = 1000
    
    # Training data (baseline)
    train_data = {
        'age': np.random.normal(35, 10, n_samples),
        'income': np.random.normal(50000, 15000, n_samples),
        'credit_score': np.random.normal(700, 50, n_samples),
        'loan_amount': np.random.normal(200000, 50000, n_samples),
        'employment_years': np.random.normal(5, 3, n_samples),
        'debt_ratio': np.random.uniform(0.1, 0.5, n_samples),
        'location': np.random.choice(['urban', 'suburban', 'rural'], n_samples),
        'education': np.random.choice(['high_school', 'bachelors', 'masters'], n_samples),
        'loan_approved': np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
    }
    
    train_df = pd.DataFrame(train_data)
    
    # Production old (similar to training)
    old_data = {
        'age': np.random.normal(35, 10, n_samples),
        'income': np.random.normal(50000, 15000, n_samples),
        'credit_score': np.random.normal(700, 50, n_samples),
        'loan_amount': np.random.normal(200000, 50000, n_samples),
        'employment_years': np.random.normal(5, 3, n_samples),
        'debt_ratio': np.random.uniform(0.1, 0.5, n_samples),
        'location': np.random.choice(['urban', 'suburban', 'rural'], n_samples),
        'education': np.random.choice(['high_school', 'bachelors', 'masters'], n_samples),
        'loan_approved': np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
    }
    
    old_df = pd.DataFrame(old_data)
    
    # Production new (with drift)
    new_data = {
        'age': np.random.normal(32, 12, n_samples),  # Younger population (drift)
        'income': np.random.normal(45000, 20000, n_samples),  # Lower income (drift)
        'credit_score': np.random.normal(680, 60, n_samples),  # Lower scores (drift)
        'loan_amount': np.random.normal(250000, 60000, n_samples),  # Higher loans (drift)
        'employment_years': np.random.normal(4, 4, n_samples),  # Less experience (drift)
        'debt_ratio': np.random.uniform(0.2, 0.6, n_samples),  # Higher debt (drift)
        'location': np.random.choice(['urban', 'suburban', 'rural', 'remote'], n_samples),  # New category!
        'education': np.random.choice(['high_school', 'bachelors', 'masters', 'phd'], n_samples, p=[0.3, 0.4, 0.2, 0.1]),  # New category!
        'loan_approved': np.random.choice([0, 1], n_samples, p=[0.5, 0.5])  # Different distribution
    }
    
    new_df = pd.DataFrame(new_data)
    
    # Save files to samples directory
    import os
    samples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'samples')
    os.makedirs(samples_dir, exist_ok=True)
    
    train_df.to_csv(os.path.join(samples_dir, 'sample_train.csv'), index=False)
    old_df.to_csv(os.path.join(samples_dir, 'sample_prod_old.csv'), index=False)
    new_df.to_csv(os.path.join(samples_dir, 'sample_prod_new.csv'), index=False)
    
    print("✅ Sample data files created:")
    print("   - sample_train.csv")
    print("   - sample_prod_old.csv")
    print("   - sample_prod_new.csv")
    print("\nExpected drift in:")
    print("   - age (distribution shift)")
    print("   - income (mean shift)")
    print("   - credit_score (variance change)")
    print("   - location (new category: 'remote')")
    print("   - education (new category: 'phd')")

if __name__ == "__main__":
    generate_sample_data()
