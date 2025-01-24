"""SQL validation module to check and format SQL queries.

Returns:
    Tuple[bool, str]: Validation status and formatted SQL or error message
"""

import sqlparse
from typing import Tuple

class SQLValidator:
    def validate_query(self, query: str) -> Tuple[bool, str]:
        try:
            # Format SQL for readability and consistency
            formatted_sql = sqlparse.format(
                query,
                reindent = True,
                keyword_case='upper'
            )
            
            # Basic validation - check for essential SQL keywords
            if not any(keyword in formatted_sql.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
                return False, "Missing SQL keyword"
            
            return True, formatted_sql
        
        except Exception as e:
            return False, str(e)