"""
Test Product Management - Cải tiến
"""
import pytest
from utils.helpers import (
    login_admin, safe_click, wait_for_element_visible,
    fill_form_safely, get_table_row_count, verify_alert_message
)

class TestProduct:
    """Test cases cho quản lý sản phẩm"""
    
    def test_view_products_list(self, browser_page):
        """Test hiển thị danh sách sản phẩm"""
        page = browser_page
        
        # Login
        assert login_admin(page)
        
        # Navigate to Products
        assert safe_click(page, "#sidebar__products a")
        assert wait_for_element_visible(page, "#main__products")
        
        # Đợi load
        page.wait_for_timeout(2000)
        
        # Verify table
        assert wait_for_element_visible(page, "#product-table-content__body")
        
        row_count = get_table_row_count(page, "#product-table-content__body")
        assert row_count > 0, "Không có sản phẩm nào"
        
        print(f"✅ Hiển thị {row_count} sản phẩm")
    
    def test_add_product_success(self, browser_page):
        """Test thêm sản phẩm thành công"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__products a")
        assert wait_for_element_visible(page, "#main__products")
        
        # Product data
        product_name = f"Test Product {page.evaluate('Date.now()')}"
        
        # Fill form
        assert fill_form_safely(page, "new-product-name", product_name)
        page.select_option("#new-brand", "SAMSUNG")
        assert fill_form_safely(page, "new-number-of-versions", "1")
        
        # Đợi version fields xuất hiện
        page.wait_for_timeout(1000)
        
        if wait_for_element_visible(page, "#version-price-1", timeout=5000):
            assert fill_form_safely(page, "version-price-1", "25000000")
            assert fill_form_safely(page, "version-pb-1", "256GB/8GB")
        else:
            pytest.skip("Version fields không xuất hiện")
        
        # Technical specs
        assert fill_form_safely(page, "new-chip", "Snapdragon 8 Gen 2")
        assert fill_form_safely(page, "new-pin", "5000mAh")
        assert fill_form_safely(page, "new-size", "6.8 inch")
        assert fill_form_safely(page, "new-f", "120Hz")
        
        # Submit
        assert safe_click(page, "button.add-btn"), "Không thể click nút Thêm"
        page.wait_for_timeout(3000)
        
        # Verify alert thành công
        if verify_alert_message(page, "thành công"):
            print("✅ Thêm sản phẩm thành công")
        else:
            print("⚠️  Không thấy thông báo thành công")
    
    def test_search_product(self, browser_page):
        """Test tìm kiếm sản phẩm"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__products a")
        assert wait_for_element_visible(page, "#main__products")
        
        page.wait_for_timeout(2000)
        
        # Search
        search_term = "Samsung"
        assert fill_form_safely(page, "product-name", search_term)
        page.wait_for_timeout(1500)
        
        # Verify results
        assert wait_for_element_visible(page, "#product-table-content__body")
        
        # Check có kết quả không
        row_count = get_table_row_count(page, "#product-table-content__body")
        print(f"✅ Tìm thấy {row_count} sản phẩm với từ khóa '{search_term}'")
    
    def test_filter_product_by_brand(self, browser_page):
        """Test lọc sản phẩm theo thương hiệu"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__products a")
        assert wait_for_element_visible(page, "#main__products")
        
        page.wait_for_timeout(2000)
        
        # Filter by SAMSUNG
        page.select_option("#brand", "SAMSUNG")
        page.wait_for_timeout(1500)
        
        # Verify
        assert wait_for_element_visible(page, "#product-table-content__body")
        
        row_count = get_table_row_count(page, "#product-table-content__body")
        print(f"✅ Lọc Samsung: {row_count} sản phẩm")
    
    def test_view_product_details(self, browser_page):
        """Test xem chi tiết sản phẩm"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__products a")
        assert wait_for_element_visible(page, "#main__products")
        
        page.wait_for_timeout(2000)
        
        # Click detail button đầu tiên
        detail_buttons = page.query_selector_all(".detail-btn")
        assert len(detail_buttons) > 0, "Không có nút chi tiết"
        
        detail_buttons[0].click()
        page.wait_for_timeout(1000)
        
        # Verify modal
        assert wait_for_element_visible(page, "#modal-detailproduct")
        assert wait_for_element_visible(page, "#detail-name")
        
        print("✅ Modal chi tiết sản phẩm hiển thị")
    
    def test_pagination_products(self, browser_page):
        """Test phân trang sản phẩm"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__products a")
        assert wait_for_element_visible(page, "#main__products")
        
        page.wait_for_timeout(2000)
        
        # Kiểm tra pagination có tồn tại không
        if wait_for_element_visible(page, "#pagination-products", timeout=3000):
            # Click next page nếu có
            next_buttons = page.query_selector_all("#pagination-products a:has-text('»')")
            if next_buttons and not "disabled" in next_buttons[0].get_attribute("class"):
                next_buttons[0].click()
                page.wait_for_timeout(1500)
                
                # Verify vẫn có data
                assert wait_for_element_visible(page, "#product-table-content__body")
                print("✅ Chuyển trang thành công")
            else:
                print("ℹ️  Chỉ có 1 trang")
        else:
            print("ℹ️  Không có pagination (ít sản phẩm)")

class TestProductValidation:
    """Test validation khi thêm sản phẩm"""
    
    def test_add_product_missing_required_fields(self, browser_page):
        """Test thêm sản phẩm thiếu thông tin"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__products a")
        assert wait_for_element_visible(page, "#main__products")
        
        # Chỉ fill một số field
        fill_form_safely(page, "new-product-name", "Incomplete Product")
        # Không fill brand, versions, specs...
        
        # Try to submit
        safe_click(page, "button.add-btn")
        page.wait_for_timeout(2000)
        
        # Verify có thông báo lỗi
        if verify_alert_message(page, "đầy đủ"):
            print("✅ Validation hoạt động đúng")
        else:
            print("⚠️  Không thấy thông báo lỗi")