# TRDizin MCP Server - Troubleshooting Guide

## 🚨 Common Smithery.ai Deployment Issues

### Issue: "Unexpected internal error or timeout"

#### **✅ CURRENT STATUS: Dockerfile Removed**
The project now uses **native Python runtime** without Docker for better Smithery.ai compatibility.

#### **Solution 1: Use Current Configuration (Recommended)**
The project is now optimized for Smithery.ai:
- ✅ No Dockerfile (uses native Python)
- ✅ Simplified `smithery.yaml`
- ✅ Minimal `requirements.txt`
- ✅ All tests passing

#### **Solution 2: Try Alternative Configuration**
If the main config still fails, try the alternative:

```bash
# Backup current config
cp smithery.yaml smithery.yaml.backup

# Use alternative config
cp smithery.alternative.yaml smithery.yaml
```

#### **Solution 3: Update smithery.yaml**
Ensure your `smithery.yaml` has proper timeout and memory settings:

```yaml
startCommand:
  type: stdio
configSchema:
  type: object
  properties: {}
commandFunction: |-
  (config) => ({
    command: 'python',
    args: ['server.py']
  })
exampleConfig: {}
timeout: 30000
memory: 512
```

### Issue: "Module not found" or Import Errors

#### **Solution: Check Dependencies**
Ensure all dependencies are properly specified:

```bash
# Test locally first
pip install -r requirements.txt
python server.py
```

#### **Fixed requirements.txt:**
```
requests==2.32.4
mcp==1.10.1
urllib3==2.5.0
```

### Issue: "Connection timeout" or API Errors

#### **Solution: Test TRDizin API**
```bash
# Test API connectivity
python -c "import requests; print(requests.get('https://search.trdizin.gov.tr/api/defaultSearch/publication/?q=test&limit=1').status_code)"
```

Should return `200` if API is accessible.

### Issue: "Server not responding"

#### **Solution: Check Server Startup**
```bash
# Test MCP server locally
python server.py

# Test with simple query
python -c "import asyncio; from server import search_trdizin_articles; print(asyncio.run(search_trdizin_articles('test', 1)))"
```

## 🔧 Deployment Alternatives

### Option 1: Minimal Deployment (Recommended)
1. Remove `Dockerfile`
2. Keep only essential files:
   - `server.py`
   - `trdizin_client.py`
   - `requirements.txt`
   - `smithery.yaml`
   - `README.md`

### Option 2: Use Python Runtime Directly
Update `smithery.yaml` to use Python directly:

```yaml
startCommand:
  type: stdio
configSchema:
  type: object
  properties: {}
commandFunction: |-
  (config) => ({
    command: 'python3',
    args: ['server.py']
  })
exampleConfig: {}
```

### Option 3: Alternative MCP Framework
If FastMCP causes issues, consider using the standard MCP SDK:

```python
# Alternative server.py structure
import asyncio
from mcp.server import Server
from mcp.types import Tool

server = Server("trdizin-mcp")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_trdizin_articles",
            description="Search Turkish academic articles",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                }
            }
        )
    ]
```

## 🧪 Local Testing Commands

### Test 1: Basic Functionality
```bash
python -c "from trdizin_client import TRDizinClient; client = TRDizinClient(); result = client.search_articles('test', 1); print('Success:', result['success'])"
```

### Test 2: MCP Server
```bash
python test_mcp.py
```

### Test 3: Full Integration
```bash
python test_full_mcp.py
```

## 📞 Support Steps

### Step 1: Verify Local Setup
```bash
# Check Python version
python --version

# Check dependencies
pip list | grep -E "(requests|mcp|urllib3)"

# Test basic functionality
python -c "import server; print('Server imports successfully')"
```

### Step 2: Simplify Deployment
1. Remove unnecessary files
2. Use minimal `smithery.yaml`
3. Test with simple Dockerfile or no Dockerfile

### Step 3: Check Smithery Logs
- Look for specific error messages in Smithery deployment logs
- Check for timeout issues
- Verify memory usage

## 🚀 Quick Fix Commands

```bash
# Quick fix for Smithery deployment
git rm Dockerfile
git add .
git commit -m "Remove Dockerfile for Smithery compatibility"
git push

# Alternative: Use simple Dockerfile
cp Dockerfile.simple Dockerfile
git add Dockerfile
git commit -m "Use simplified Dockerfile"
git push
```

## 📋 Deployment Checklist

- [ ] `server.py` and `trdizin_client.py` are present
- [ ] `requirements.txt` has exact versions
- [ ] `smithery.yaml` is properly configured
- [ ] No complex Dockerfile (or use simple version)
- [ ] Local testing passes
- [ ] Repository is up to date
- [ ] Smithery has access to repository

## 🎯 Success Indicators

✅ **Local Test Passes:**
```bash
python server.py
# Should start without errors
```

✅ **API Test Passes:**
```bash
python -c "from trdizin_client import TRDizinClient; print(TRDizinClient().search_articles('test', 1)['success'])"
# Should print: True
```

✅ **MCP Test Passes:**
```bash
python test_full_mcp.py
# Should complete without errors
```

---

**If issues persist, try the minimal deployment approach without Docker!**
