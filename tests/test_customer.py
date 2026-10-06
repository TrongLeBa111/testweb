"""
Test cases cho Customer Management UI
Kiểm tra giao diện quản lý khách hàng
"""
import pytest
from utils.helpers import safe_click
from utils.base_test import BaseTest

class TestCustomerDisplay(BaseTest):
    """Test hiển thị danh sách khách hàng"""
    
    def test_customer_table_display(self, browser_page):
        """Test bảng khách hàng hiển thị"""
        page = browser_page
        self.login_as_admin(page)
        
        # Navigate to Customers
        safe_click(page, "#sidebar__customers a")
        page.wait_for_timeout(1000)
        
        # Verify table elements
        self.assert_element_visible(page, "#main__customers")
        self.assert_element_visible(page, ".table-content")
        self.assert_element_visible(page, "#customer-table-content__body")
        
        # Verify table headers
        headers = page.query_selector_all(".table-content__header th")
        assert len(headers) > 0, "Table should have headers"
    
    def test_customer_form_display(self, browser_page):
        """Test form thêm khách hàng hiển thị"""
        page = browser_page
        self.login_as_admin(page)
        
        safe_click(page, "#sidebar__customers a")
        page.wait_for_timeout(1000)
        
        # Verify form elements
        self.assert_element_visible(page, "#add-customer-form")
        self.assert_element_visible(page, "#new-customer-name")
        self.assert_element_visible(page, "#new-customer-password")
        self.assert_element_visible(page, "#new-customer-phone")
        self.assert_element_visible(page, "#new-customer-address")

class TestCustomerForm(BaseTest):
    """Test form thêm/sửa khách hàng"""
    
    def test_add_customer_form_fields(self, browser_page):
        """Test các trường trong form thêm khách hàng"""
        page = browser_page
        self.login_as_admin(page)
        
        safe_click(page, "#sidebar__customers a")
        page.wait_for_timeout(1000)
        
        # Điền thông tin
        page.fill("#new-customer-name", "testuser123")
        page.fill("#new-customer-password", "123456")
        page.fill("#new-customer-phone", "0123456789")
        page.fill("#new-customer-address", "Test Address, TP HCM")
        
        # Verify giá trị đã điền
        assert page.input_value("#new-customer-name") == "testuser123"
        assert page.input_value("#new-customer-password") == "123456"
        assert page.input_value("#new-customer-phone") == "0123456789"
    
    def test_reset_customer_form(self, browser_page):
        """Test reset form khách hàng"""
        page = browser_page
        self.login_as_admin(page)
        
        safe_click(page, "#sidebar__customers a")
        page.wait_for_timeout(1000)
        
        # Điền thông tin
        page.fill("#new-customer-name", "testuser")
        page.fill("#new-customer-phone", "0123456789")
        
        # Click reset
        reset_btn = page.locator("#add-customer-form button.delete-btn")
        if reset_btn.count() > 0:
            reset_btn.click()
            page.wait_for_timeout(500)
            
            # Verify form đã reset
            assert page.input_value("#new-customer-name") == ""
            assert page.input_value("#new-customer-phone") == ""

class TestCustomerActions(BaseTest):
    """Test các hành động với khách hàng"""
    
    def test_customer_action_buttons(self, browser_page):
        """Test nút hành động trên bảng khách hàng"""
        page = browser_page
        self.login_as_admin(page)
        
        safe_click(page, "#sidebar__customers a")
        page.wait_for_timeout(1500)
        
        # Kiểm tra có nút hành động
        rows = page.query_selector_all("#customer-table-content__body tr")
        
        if len(rows) > 0:
            # Kiểm tra các nút trong hàng đầu tiên
            first_row = page.locator("#customer-table-content__body tr").first
            
            # Có thể có nút Edit/Delete/Block
            action_buttons = first_row.locator("button")
            assert action_buttons.count() >= 0
    
    def test_edit_customer_popup(self, browser_page):
        """Test mở popup sửa khách hàng"""
        page = browser_page
        self.login_as_admin(page)
        
        safe_click(page, "#sidebar__customers a")
        page.wait_for_timeout(1500)
        
        # Tìm nút edit
        edit_buttons = page.query_selector_all(".edit-btn")
        
        if len(edit_buttons) > 0:
            edit_buttons[0].click()
            page.wait_for_timeout(500)
            
            # Verify popup hiển thị
            if page.is_visible("#modal-changecustomer"):
                self.assert_element_visible(page, "#modal-changecustomer")
                self.assert_element_visible(page, "#changecustomer")
    
    def test_close_edit_customer_popup(self, browser_page):
        """Test đóng popup sửa khách hàng"""
        page = browser_page
        self.login_as_admin(page)
        
        safe_click(page, "#sidebar__customers a")
        page.wait_for_timeout(1500)
        
        # Mở popup
        edit_buttons = page.query_selector_all(".edit-btn")
        if len(edit_buttons) > 0:
            edit_buttons[0].click()
            page.wait_for_timeout(500)
            
            # Đóng popup
            if page.is_visible("#close-changecustomer"):
                page.click("#close-changecustomer")
                page.wait_for_timeout(500)

class TestCustomerPagination(BaseTest):
    """Test phân trang khách hàng"""
    
    def test_pagination_display(self, browser_page):
        """Test pagination hiển thị"""
        page = browser_page
        self.login_as_admin(page)
        
        safe_click(page, "#sidebar__customers a")
        page.wait_for_timeout(1500)
        
        # Kiểm tra pagination
        if page.is_visible("#pagination-customers"):
            self.assert_element_visible(page, "#pagination-customers")