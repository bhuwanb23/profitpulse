"""
Tests for data cleaning module
"""

import pandas as pd
import numpy as np
import pytest
from src.data.preprocessing.cleaning import clean_dataframe, remove_duplicates, clean_text_columns


def test_remove_duplicates():
    """Test removing duplicate rows from DataFrame"""
    # Create test DataFrame with duplicates
    df = pd.DataFrame({
        'A': [1, 2, 2, 3],
        'B': ['a', 'b', 'b', 'c']
    })
    
    # Remove duplicates
    cleaned_df = remove_duplicates(df)
    
    # Check that duplicates are removed
    assert len(cleaned_df) == 3
    assert len(cleaned_df.drop_duplicates()) == len(cleaned_df)


def test_clean_text_columns():
    """Test cleaning text columns"""
    # Create test DataFrame with messy text
    df = pd.DataFrame({
        'text_col': ['  Hello World  ', '  TEST  ', '  lowercase  '],
        'other_col': [1, 2, 3]
    })
    
    # Clean text columns
    cleaned_df = clean_text_columns(df, ['text_col'])
    
    # Check that text is cleaned
    assert cleaned_df['text_col'].iloc[0] == 'hello world'
    assert cleaned_df['text_col'].iloc[1] == 'test'
    assert cleaned_df['text_col'].iloc[2] == 'lowercase'


def test_clean_dataframe():
    """Test comprehensive data cleaning pipeline"""
    # Create test DataFrame with various issues
    df = pd.DataFrame({
        'text_col': ['  Hello World  ', '  TEST  ', '  lowercase  '],
        'numeric_col': [1.0, 2.0, np.nan],
        'duplicate_col': [1, 1, 2]
    })
    
    # Clean DataFrame
    cleaned_df = clean_dataframe(
        df,
        text_columns=['text_col'],
        remove_duplicates_subset=['duplicate_col']
    )
    
    # Check results
    assert len(cleaned_df) == 2  # Duplicates removed
    assert cleaned_df['text_col'].iloc[0] == 'hello world'
    assert cleaned_df['text_col'].iloc[1] == 'lowercase'


if __name__ == "__main__":
    pytest.main([__file__])