import os
import json

# Test file writing
test_file = "app/static/data/test_write.json"
test_data = {"test": "working", "timestamp": "2024-04-07"}

try:
    # Ensure directory exists
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    
    # Write test file
    with open(test_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"✅ Test file written successfully to: {test_file}")
    
    # Read it back
    with open(test_file, 'r') as f:
        read_data = json.load(f)
    
    print(f"✅ Test file read successfully: {read_data}")
    
    # Clean up
    os.remove(test_file)
    print(f"✅ Test file removed successfully")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print(f"❌ Exception type: {type(e).__name__}")
    print(f"❌ Working directory: {os.getcwd()}")
    print(f"❌ File path: {os.path.abspath(test_file)}")
