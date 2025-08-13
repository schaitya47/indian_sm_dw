<!-- potenial issues  -->
1. SQL Issues 
    - **Problem**: SQL syntax and formatting issues in Mage AI blocks
    - **Common Issues**:
      - Don't use comment in SQL block which are used in mage AI. 
      - Check for semi colon that also creates issue in mage AI block.
    - **Detailed Solutions**:
      - **Comments**: 
        - **Issue**: SQL comments (`--` or `/* */`) can interfere with Mage AI's SQL parsing
        - **Solution**: Remove all SQL comments from blocks or use alternative documentation methods
        - **Files**: All `.sql` files in `data_loaders/`, `data_exporters/`, `transformers/`
      - **Semicolons**: 
        - **Issue**: Trailing semicolons (`;`) at the end of SQL statements can cause execution errors
        - **Solution**: Remove semicolons from the end of SQL statements in Mage blocks
        - **Example**: Change `SELECT * FROM table;` to `SELECT * FROM table`
    - **Best Practices**:
      - Test SQL queries in a database client before adding to Mage blocks
      - Use consistent indentation and formatting
      - Validate table and column names exist in the target database
      - Use parameterized queries for dynamic values

2. SSL Certificate Issues with API Calls
    - **Problem**: API calls to external services (like TickerTape, Screener.in) fail with SSL certificate verification errors
    - **Symptoms**: 
      - `TypeError: 'NoneType' object is not iterable` errors
      - API responses returning None instead of expected data
      - SSL certificate verification failures in logs
    - **Solution**: Disable SSL certificate verification in the CustomSession base class
      - **File**: `c:\Mage_AI\mage_env\Lib\site-packages\Base\CustomRequest.py`
      - **Changes made**:
        1. **Lines 1-5**: Add urllib3 import and disable SSL warnings:
           ```python
           import json
           import brotli
           import urllib3
           from requests import Session, session
           from requests.adapters import HTTPAdapter, Retry
           
           # Disable SSL warnings when verify=False is used
           urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
           ```
        2. **Line ~45**: Set `self.session.verify = False` in the `__init__` method after timeout setting
        3. **Lines ~75-80**: Add `verify=False` parameter to both GET requests in `hit_and_get_data` method:
           ```python
           response = self.session.get(url, params=params, headers=self.headers, verify=False)
           response = self.session.get(url, headers=self.headers, verify=False)
           ```
    - **Security Note**: This disables SSL certificate verification - acceptable for development/testing but should be re-evaluated for production use

3. String Literal Issues in Third-Party Libraries
    - **Problem**: Syntax errors due to embedded newlines in string literals
    - **Symptoms**: `SyntaxError: unterminated string literal` errors
    - **Files Affected**:
      - **File**: `c:\Mage_AI\mage_env\Lib\site-packages\Fundamentals\Screener.py`
      - **Line**: ~502-503
    - **Solution**: Replace problematic string handling with safer text extraction methods
      - **Original problematic code**:
        ```python
        raise ValueError(f"Error: setting columns requires Premium Account: {error.text.strip().replace('\n', ' ')}")
        ```
      - **Fixed code**:
        ```python
        # Use get_text with separator to robustly collapse any internal newlines/whitespace
        msg = error.get_text(separator=' ', strip=True)
        raise ValueError(f"Error: setting columns requires Premium Account: {msg}")
        ```
      - Move inline comments to separate lines to avoid string parsing issues

4. Regex Escape Issues in Mage AI Server
    - **Problem**: Regular expression errors when processing file paths or strings with backslashes
    - **Symptoms**: 
      - `re.error: bad escape \M at position 3` or similar regex errors
      - WebSocket server errors during code execution
      - Issues with Windows file paths containing backslashes in replacement strings
    - **Root Cause**: Mage AI's `output_display.py` uses `re.sub()` without properly escaping backslashes in replacement strings
    - **Solution**: Manually escape backslashes in replacement strings before regex substitution
      - **File**: `c:\Mage_AI\mage_env\Lib\site-packages\mage_ai\server\utils\output_display.py`
      - **Line**: ~202 (in `__interpolate_code_content` function)
      - **Original problematic code**:
        ```python
        content = re.sub(placeholder_pattern, str(replacement), content)
        ```
      - **Fixed code**:
        ```python
        safe_replacement = str(replacement).replace('\\', r'\\')
        content = re.sub(placeholder_pattern, safe_replacement, content)
        ```
    - **Explanation**: This fix escapes single backslashes (`\`) to double backslashes (`\\`) to prevent regex interpretation issues
    - **Impact**: Prevents regex parsing errors when Windows file paths or other strings contain backslashes

