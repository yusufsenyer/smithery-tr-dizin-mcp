"""
Test script for TRDizin MCP Server
"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import search_trdizin_articles

async def test_search():
    """Test the MCP search function."""
    print("Testing TRDizin MCP Server...")
    print("=" * 50)
    
    # Test 1: Turkish search
    print("\n🔍 Test 1: Turkish search - 'yapay zeka'")
    result1 = await search_trdizin_articles("yapay zeka", 3)
    print(result1[:500] + "..." if len(result1) > 500 else result1)
    
    # Test 2: English search
    print("\n🔍 Test 2: English search - 'machine learning'")
    result2 = await search_trdizin_articles("machine learning", 2)
    print(result2[:500] + "..." if len(result2) > 500 else result2)
    
    # Test 3: Empty query
    print("\n🔍 Test 3: Empty query")
    result3 = await search_trdizin_articles("", 2)
    print(result3)
    
    # Test 4: Specific Turkish term
    print("\n🔍 Test 4: Specific Turkish term - 'doğal dil işleme'")
    result4 = await search_trdizin_articles("doğal dil işleme", 2)
    print(result4[:500] + "..." if len(result4) > 500 else result4)
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_search())
