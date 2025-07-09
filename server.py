"""
TRDizin MCP Server - Search Turkish academic articles from TRDizin database.
"""
from mcp.server.fastmcp import FastMCP
from trdizin_client import TRDizinClient
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("trdizin-mcp")

# Initialize TRDizin client
trdizin_client = TRDizinClient()

@mcp.tool()
async def search_trdizin_articles(query: str, limit: int = 10) -> str:
    """
    Search for Turkish academic articles in TRDizin database.
    
    Args:
        query: Search term in Turkish or English (e.g., "yapay zeka", "machine learning")
        limit: Number of results to return (default: 10, maximum: 20)
    
    Returns:
        Formatted search results with article details including titles, authors, abstracts, and metadata.
    """
    try:
        # Validate inputs
        if not query or not query.strip():
            return "Error: Search query cannot be empty."
        
        # Ensure limit is within bounds
        limit = max(1, min(limit, 20))
        
        logger.info(f"Searching TRDizin for: '{query}' with limit: {limit}")
        
        # Perform search
        results = trdizin_client.search_articles(query.strip(), limit=limit)
        
        if not results.get('success', False):
            error_msg = results.get('error', 'Unknown error occurred')
            return f"Search failed: {error_msg}"
        
        # Format results for display
        formatted_output = _format_search_output(results)
        
        return formatted_output
        
    except Exception as e:
        logger.error(f"Error in search_trdizin_articles: {e}")
        return f"An unexpected error occurred: {str(e)}"

def _format_search_output(results: dict) -> str:
    """
    Format search results into a readable string output.
    
    Args:
        results: Search results dictionary from TRDizinClient
        
    Returns:
        Formatted string with search results
    """
    try:
        query = results.get('query', '')
        total_results = results.get('total_results', 0)
        returned_results = results.get('returned_results', 0)
        articles = results.get('results', [])
        
        if not articles:
            return f"No articles found for query: '{query}'"
        
        # Build formatted output
        output_lines = []
        output_lines.append(f"🔍 TRDizin Search Results for: '{query}'")
        output_lines.append(f"📊 Found {total_results} total results, showing {returned_results}")
        output_lines.append("=" * 60)
        
        for i, article in enumerate(articles, 1):
            output_lines.append(f"\n📄 Article {i}:")
            output_lines.append("-" * 40)
            
            # Title
            title = article.get('title', 'No title available')
            output_lines.append(f"📝 Title: {title}")
            
            # Authors
            authors = article.get('authors', [])
            if authors:
                authors_str = ", ".join(authors[:3])  # Show first 3 authors
                if len(authors) > 3:
                    authors_str += f" and {len(authors) - 3} others"
                output_lines.append(f"👥 Authors: {authors_str}")
            
            # Publication year
            year = article.get('publication_year')
            if year:
                output_lines.append(f"📅 Year: {year}")
            
            # Journal
            journal = article.get('journal')
            if journal:
                output_lines.append(f"📖 Journal: {journal}")
            
            # Institutions
            institutions = article.get('institutions', [])
            if institutions:
                inst_str = ", ".join(institutions[:2])  # Show first 2 institutions
                if len(institutions) > 2:
                    inst_str += f" and {len(institutions) - 2} others"
                output_lines.append(f"🏛️ Institutions: {inst_str}")
            
            # DOI
            doi = article.get('doi')
            if doi:
                output_lines.append(f"🔗 DOI: {doi}")
            
            # Abstract (truncated)
            abstract = article.get('abstract', '')
            if abstract:
                # Truncate abstract to 200 characters
                truncated_abstract = abstract[:200]
                if len(abstract) > 200:
                    truncated_abstract += "..."
                output_lines.append(f"📋 Abstract: {truncated_abstract}")
            
            # Keywords
            keywords = article.get('keywords', [])
            if keywords:
                keywords_str = ", ".join(keywords[:5])  # Show first 5 keywords
                if len(keywords) > 5:
                    keywords_str += "..."
                output_lines.append(f"🏷️ Keywords: {keywords_str}")
            
            # Language
            language = article.get('language', 'Unknown')
            output_lines.append(f"🌐 Language: {language}")
        
        output_lines.append("\n" + "=" * 60)
        output_lines.append("✅ Search completed successfully")
        
        return "\n".join(output_lines)
        
    except Exception as e:
        logger.error(f"Error formatting output: {e}")
        return f"Error formatting search results: {str(e)}"

if __name__ == "__main__":
    logger.info("Starting TRDizin MCP Server...")
    mcp.run(transport="stdio")
