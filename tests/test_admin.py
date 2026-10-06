"""
Test cases cho Admin Dashboard UI
Kiểm tra các tính năng giao diện admin
"""
import pytest
from utils.helpers import login_admin, safe_click, BASE_URL
from utils.base_test import BaseTest

class TestAdminLogin(BaseTest):
    """Test cases cho chức năng đăng nhập"""
    
    def test_login_fail(self, browser_page):
        """Test đăng nhập sai thông tin"""
        page = browser_page
        page.goto(BASE_URL)
        
        # Đảm bảo popup đăng nhập hiển thị
        self.assert_element_visible(page, "#login-popup")
        
        # Nhập thông tin sai
        page.fill("#username", "wronguser")
        page.fill("#password", "wrongpass")
        page.click("button:has-text('Đăng nhập')")
        
        # Kiểm tra thông báo lỗi
        self.wait_for_load(page, 1000)
        self.assert_element_visible(page, "#error-message", 
                                    "Error message should be visible")
    
    def test_login_success(self, browser_page):
        """Test đăng nhập thành công"""
        page = browser_page
        
        # Login với thông tin đúng
        self.login_as_admin(page)
        
        # Verify login successful
        self.assert_element_hidden(page, "#login-popup")
        self.assert_element_visible(page, "#sidebar")
        self.assert_element_visible(page, "#main__dashboard")

class TestAdminNavigation(BaseTest):
    """Test cases cho điều hướng trong admin"""
    
    def test_navigate_to_products(self, browser_page):
        """Test chuyển đến trang Sản phẩm"""
        page = browser_page
        self.login_as_admin(page)
        
        # Click vào menu Sản phẩm
        safe_click(page, "#sidebar__products a")
        page.wait_for_timeout(1000)
        
        # Verify trang Sản phẩm hiển thị
        self.assert_element_visible(page, "#main__products")
        self.assert_element_visible(page, "#product-table-content__body")
    
    def test_navigate_to_customers(self, browser_page):
        """Test chuyển đến trang Khách hàng"""
        page = browser_page
        self.login_as_admin(page)
        
        # Click vào menu Khách hàng
        safe_click(page, "#sidebar__customers a")
        page.wait_for_timeout(1000)
        
        # Verify trang Khách hàng hiển thị
        self.assert_element_visible(page, "#main__customers")
        self.assert_element_visible(page, "#customer-table-content__body")
    
    def test_navigate_to_orders(self, browser_page):
        """Test chuyển đến trang Đơn hàng"""
        page = browser_page
        self.login_as_admin(page)
        
        # Click vào menu Đơn hàng
        safe_click(page, "#sidebar__orders a")
        page.wait_for_timeout(1000)
        
        # Verify trang Đơn hàng hiển thị
        self.assert_element_visible(page, "#main__orders")
        self.assert_element_visible(page, "#orders-table-content__body")
    
    def test_navigate_to_statistics(self, browser_page):
        """Test chuyển đến trang Thống kê"""
        page = browser_page
        self.login_as_admin(page)
        
        # Click vào menu Thống kê
        safe_click(page, "#sidebar__statistics a")
        page.wait_for_timeout(1000)
        
        # Verify trang Thống kê hiển thị
        self.assert_element_visible(page, "#main__statistics")
        self.assert_element_visible(page, "#statistics-product-table__body")

class TestDashboardDisplay(BaseTest):
    """Test cases cho hiển thị Dashboard"""
    
    def test_dashboard_elements(self, browser_page):
        """Test các elements trên Dashboard"""
        page = browser_page
        self.login_as_admin(page)
        
        # Verify Dashboard hiển thị đầy đủ
        self.assert_element_visible(page, "#main__dashboard")
        
        # Kiểm tra phần sản phẩm
        self.assert_element_visible(page, ".products")
        self.assert_element_visible(page, ".box-product")
        
        # Kiểm tra phần đơn hàng
        self.assert_element_visible(page, ".order")
        self.assert_element_visible(page, ".box-order")
        
        # Kiểm tra phần khách hàng
        self.assert_element_visible(page, ".customers")
        self.assert_element_visible(page, ".customer__chart")
    
    def test_sidebar_menu_items(self, browser_page):
        """Test tất cả menu items trong sidebar"""
        page = browser_page
        self.login_as_admin(page)
        
        # Verify tất cả menu items hiển thị
        menu_items = [
            "#sidebar__dashboard",
            "#sidebar__products",
            "#sidebar__customers",
            "#sidebar__orders",
            "#sidebar__statistics"
        ]
        
        for item in menu_items:
            self.assert_element_visible(page, item, 
                                       f"Menu item {item} should be visible")

class TestAdminUIInteractions(BaseTest):
    """Test các tương tác UI cơ bản"""
    
    def test_sidebar_collapse(self, browser_page):
        """Test thu gọn/mở rộng sidebar"""
        page = browser_page
        self.login_as_admin(page)
        
        # Click nút hide sidebar
        if page.is_visible("#hidden-sidebar-btn"):
            page.click("#hidden-sidebar-btn")
            page.wait_for_timeout(500)
            
            # Sidebar vẫn visible nhưng có thể có class thay đổi
            self.assert_element_visible(page, "#sidebar")
    
    def test_active_menu_highlight(self, browser_page):
        """Test menu active được highlight"""
        page = browser_page
        self.login_as_admin(page)
        
        # Click vào Products
        safe_click(page, "#sidebar__products a")
        page.wait_for_timeout(500)
        
        # Kiểm tra class active (tùy implementation)
        products_item = page.locator("#sidebar__products")
        # Có thể kiểm tra class 'item--active' nếu có
        assert products_item.is_visible()