#!/usr/bin/env python3
"""
Minimal test for TRDizin MCP Server
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported."""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import requests
        print("✅ requests imported")
        
        import mcp
        print("✅ mcp imported")
        
        # Test our modules
        from trdizin_client import TRDizinClient
        print("✅ trdizin_client imported")
        
        from server import mcp as server_mcp
        print("✅ server imported")
        
        print("🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality."""
    try:
        print("\nTesting basic functionality...")
        
        from trdizin_client import TRDizinClient
        client = TRDizinClient()
        
        # Test a simple search
        result = client.search_articles("test", limit=1)
        
        if result.get('success'):
            print("✅ TRDizin API connection successful")
            print(f"📊 Found {result.get('total_results', 0)} results")
            return True
        else:
            print(f"❌ API test failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TRDizin MCP Server - Minimal Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test functionality
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎉 All tests passed! Ready for deployment.")
            sys.exit(0)
        else:
            print("\n❌ Functionality tests failed.")
            sys.exit(1)
    else:
        print("\n❌ Import tests failed.")
        sys.exit(1)
