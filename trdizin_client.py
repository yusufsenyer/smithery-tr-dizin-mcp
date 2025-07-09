"""
TRDizin API Client for searching Turkish academic articles.
"""
import requests
import urllib.parse
import json
import logging
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TRDizinClient:
    """Client for interacting with TRDizin API."""
    
    def __init__(self):
        self.primary_api_url = "https://search.trdizin.gov.tr/api/defaultSearch/publication/"
        self.fallback_api_url = "https://search.trdizin.gov.tr/tr/yayin/ara"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TRDizin-MCP-Client/1.0'
        })
    
    def search_articles(self, query: str, limit: int = 10, page: int = 1) -> Dict[str, Any]:
        """
        Search for academic articles in TRDizin database.
        
        Args:
            query: Search term (Turkish or English)
            limit: Number of results to return (default: 10, max: 20)
            page: Page number (default: 1)
            
        Returns:
            Dictionary containing search results and metadata
        """
        try:
            # Ensure limit doesn't exceed 20
            limit = min(limit, 20)
            
            # URL encode the query to handle Turkish characters
            encoded_query = urllib.parse.quote(query, safe='')
            
            # Prepare API parameters
            params = {
                'q': query,
                'order': 'relevance-DESC',
                'page': page,
                'limit': limit
            }
            
            logger.info(f"Searching TRDizin for: '{query}' (limit: {limit}, page: {page})")
            
            # Make API request
            response = self.session.get(self.primary_api_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Extract and format results
            formatted_results = self._format_search_results(data, query)
            
            return formatted_results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {
                'success': False,
                'error': f"API request failed: {str(e)}",
                'query': query,
                'results': []
            }
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return {
                'success': False,
                'error': f"Invalid JSON response: {str(e)}",
                'query': query,
                'results': []
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'query': query,
                'results': []
            }
    
    def _format_search_results(self, data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Format raw API response into structured results.
        
        Args:
            data: Raw API response data
            query: Original search query
            
        Returns:
            Formatted search results
        """
        try:
            hits = data.get('hits', {})
            total_results = hits.get('total', {}).get('value', 0)
            articles = hits.get('hits', [])
            
            formatted_articles = []
            
            for article_data in articles:
                source = article_data.get('_source', {})
                formatted_article = self._format_article(source)
                if formatted_article:
                    formatted_articles.append(formatted_article)
            
            return {
                'success': True,
                'query': query,
                'total_results': total_results,
                'returned_results': len(formatted_articles),
                'results': formatted_articles
            }
            
        except Exception as e:
            logger.error(f"Error formatting results: {e}")
            return {
                'success': False,
                'error': f"Error formatting results: {str(e)}",
                'query': query,
                'results': []
            }
    
    def _format_article(self, source: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Format a single article from API response.
        
        Args:
            source: Article source data from API
            
        Returns:
            Formatted article data or None if formatting fails
        """
        try:
            # Extract abstracts (Turkish and English)
            abstracts = source.get('abstracts', [])
            turkish_abstract = ""
            english_abstract = ""
            title = ""
            
            for abstract in abstracts:
                if abstract.get('language') == 'TUR':
                    turkish_abstract = abstract.get('abstract', '')
                    if not title:
                        title = abstract.get('title', '')
                elif abstract.get('language') == 'ENG':
                    english_abstract = abstract.get('abstract', '')
                    if not title:
                        title = abstract.get('title', '')
            
            # Use Turkish title/abstract as primary, English as fallback
            primary_title = title
            primary_abstract = turkish_abstract if turkish_abstract else english_abstract
            
            # Extract authors
            authors = source.get('authors', [])
            author_names = []
            author_institutions = []
            
            for author in authors:
                if author and isinstance(author, dict):
                    if author.get('name'):
                        author_names.append(author['name'])
                    if author.get('institutionName'):
                        institutions = author['institutionName']
                        if isinstance(institutions, list) and institutions:
                            author_institutions.extend(institutions)
                        elif isinstance(institutions, str):
                            author_institutions.append(institutions)
            
            # Remove duplicates from institutions
            author_institutions = list(set(author_institutions))
            
            # Extract other metadata
            publication_year = source.get('publicationYear')
            doi = source.get('doi')
            journal_info = source.get('journal')
            journal_name = None
            if journal_info and isinstance(journal_info, dict):
                journal_name = journal_info.get('name')
            elif isinstance(journal_info, str):
                journal_name = journal_info
            
            # Extract subjects/keywords
            subjects = source.get('subjects', [])
            keywords = []
            if subjects and isinstance(subjects, list):
                for subject in subjects:
                    if isinstance(subject, dict) and subject.get('name'):
                        keywords.append(subject['name'])
                    elif isinstance(subject, str):
                        keywords.append(subject)
            
            return {
                'title': primary_title,
                'authors': author_names,
                'institutions': author_institutions,
                'publication_year': publication_year,
                'journal': journal_name,
                'doi': doi,
                'abstract': primary_abstract,
                'keywords': keywords,
                'language': 'Turkish' if turkish_abstract else 'English'
            }
            
        except Exception as e:
            logger.error(f"Error formatting article: {e}")
            return None
