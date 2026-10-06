"""
Base test class with common functionality
FIXED: Import safe_fill correctly
"""
import pytest
from utils.helpers import (
    login_admin, 
    safe_click,
    safe_fill,  # Đã thêm import này
    wait_for_element_visible,
    assert_element_visible,
    assert_element_hidden,
    take_screenshot
)

    
class BaseTest:
    """Base class cho tất cả test cases"""
    
    def login_as_admin(self, page, username="admin", password="admin"):
        """Login as admin with assertion"""
        success = login_admin(page, username, password)
        assert success, "Failed to login as admin"
    
    def navigate_to_section(self, page, section_id: str):
        """Navigate to a specific admin section"""
        selector = f"#{section_id} a"
        assert safe_click(page, selector), f"Failed to navigate to {section_id}"
        
        # Wait for main content to load
        main_selector = f"#main__{section_id.replace('sidebar__', '')}"
        assert wait_for_element_visible(page, main_selector), \
            f"Main content {main_selector} not visible"
    
    def assert_element_visible(self, page, selector: str, message: str = ""):
        """Assert element is visible"""
        assert_element_visible(page, selector, message)
    
    def assert_element_hidden(self, page, selector: str, message: str = ""):
        """Assert element is hidden"""
        assert_element_hidden(page, selector, message)
    
    def safe_click(self, page, selector: str, timeout: int = 5000):
        """Safe click with assertion"""
        assert safe_click(page, selector, timeout), f"Failed to click {selector}"
    
    def safe_fill(self, page, selector: str, value: str, timeout: int = 5000):
        """Safe fill with assertion"""
        assert safe_fill(page, selector, value, timeout), \
            f"Failed to fill {selector} with {value}"
    
    def wait_for_load(self, page, timeout: int = 2000):
        """Wait for page to load"""
        page.wait_for_timeout(timeout)
    
    def capture_screenshot(self, page, name: str):
        """Capture screenshot for debugging"""
        take_screenshot(page, name)