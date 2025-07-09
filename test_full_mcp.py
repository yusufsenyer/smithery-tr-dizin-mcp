"""
Full integration test for TRDizin MCP Server
"""
import asyncio
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from server import mcp

async def test_mcp_tools():
    """Test MCP tools directly."""
    print("Testing TRDizin MCP Tools...")
    print("=" * 50)
    
    # Get available tools
    tools = await mcp.list_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # Test the search tool
    if tools:
        tool = tools[0]
        print(f"\nTesting tool: {tool.name}")
        print(f"Description: {tool.description}")
        
        # Test with Turkish query
        print("\n🔍 Testing with Turkish query: 'yapay zeka'")
        try:
            result = await mcp.call_tool("search_trdizin_articles", {"query": "yapay zeka", "limit": 2})
            print("✅ Success!")
            print(f"Result length: {len(str(result))}")
            print(f"First 300 chars: {str(result)[:300]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test with English query
        print("\n🔍 Testing with English query: 'computer science'")
        try:
            result = await mcp.call_tool("search_trdizin_articles", {"query": "computer science", "limit": 1})
            print("✅ Success!")
            print(f"Result length: {len(str(result))}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test error handling
        print("\n🔍 Testing error handling with empty query")
        try:
            result = await mcp.call_tool("search_trdizin_articles", {"query": "", "limit": 1})
            print("✅ Error handled correctly!")
            print(f"Result: {result}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ MCP tool tests completed!")

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
