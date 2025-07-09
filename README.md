# TRDizin MCP Server

🔍 **Search Turkish Academic Articles with MCP**

A Model Context Protocol (MCP) server that enables searching Turkish academic articles from TRDizin (Turkish Academic Network and Information Center) database. This server integrates seamlessly with AI assistants and chat applications to provide access to Turkish academic research.

## Features

- 🎯 **Direct TRDizin Integration** - Search the official Turkish academic database
- 🌐 **Multilingual Support** - Search in Turkish or English
- 📚 **Rich Article Data** - Get titles, authors, abstracts, institutions, and metadata
- 🚀 **Smithery Ready** - Deploy instantly to Smithery.ai platform
- ⚡ **Fast & Reliable** - Optimized API calls with error handling
- 🔧 **Easy Integration** - Standard MCP protocol for universal compatibility

## Quick Start

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/yusufsenyer/smithery-tr-dizin-mcp.git
cd smithery-tr-dizin-mcp
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the MCP server:**
```bash
python server.py
```

### Deploy to Smithery

1. Push your code to GitHub
2. Connect your repository to Smithery.ai
3. Deploy with one click! 🎉

The `smithery.yaml` configuration is already set up for instant deployment.

## Usage Examples

Once deployed, you can search Turkish academic articles through your AI assistant:

**Turkish Search:**
```
User: "yapay zeka makalelerini bul"
MCP: [Returns formatted list of AI-related Turkish academic articles]
```

**English Search:**
```
User: "machine learning"
MCP: [Returns formatted list of ML-related articles]
```

**Specific Search:**
```
User: "doğal dil işleme"
MCP: [Returns natural language processing articles]
```

## API Reference

### search_trdizin_articles

Search for Turkish academic articles in TRDizin database.

**Parameters:**
- `query` (string): Search term in Turkish or English
- `limit` (integer, optional): Number of results to return (default: 10, max: 20)

**Returns:**
Formatted search results including:
- Article titles (Turkish/English)
- Author names and institutions
- Publication year and journal
- Abstract (truncated for readability)
- DOI and keywords
- Language information

## Technical Details

### Architecture

- **TRDizin Client** (`trdizin_client.py`): Handles API communication and response parsing
- **MCP Server** (`server.py`): Implements MCP protocol and tool registration
- **Error Handling**: Comprehensive error handling for network issues and API failures
- **Turkish Character Support**: Proper URL encoding for Turkish characters (ğ, ü, ş, ı, ö, ç)

### API Endpoints

- **Primary API**: `https://search.trdizin.gov.tr/api/defaultSearch/publication/`
- **Response Format**: JSON with article metadata, abstracts, and author information

### Dependencies

- `requests>=2.28.0` - HTTP client for API calls
- `mcp>=1.0.0` - Model Context Protocol implementation
- `urllib3>=1.26.0` - URL encoding utilities

## Configuration

The server is configured through `smithery.yaml` for Smithery deployment:

```yaml
startCommand:
  type: stdio
configSchema:
  type: object
  properties: {}
commandFunction: |-
  (config) => ({
    command: 'python',
    args: ['-m', 'server']
  })
```

## Error Handling

The server includes robust error handling for:
- Network connectivity issues
- API rate limiting
- Invalid search queries
- JSON parsing errors
- Turkish character encoding

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check TRDizin API documentation
- Review MCP protocol specifications

---

**Made with ❤️ for the Turkish academic community**

*Enabling AI assistants to access Turkish academic research seamlessly*
