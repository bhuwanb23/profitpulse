"""
Test imports for profitability predictor modules
"""

try:
    from sklearn.model_selection import train_test_split
    print("✅ sklearn.model_selection imported successfully")
except ImportError as e:
    print(f"❌ Failed to import sklearn.model_selection: {e}")

try:
    from sklearn.preprocessing import StandardScaler
    print("✅ sklearn.preprocessing imported successfully")
except ImportError as e:
    print(f"❌ Failed to import sklearn.preprocessing: {e}")

try:
    import pandas as pd
    print("✅ pandas imported successfully")
except ImportError as e:
    print(f"❌ Failed to import pandas: {e}")

try:
    import numpy as np
    print("✅ numpy imported successfully")
except ImportError as e:
    print(f"❌ Failed to import numpy: {e}")

print("Import test completed.")