"""
Test Analytics/Statistics - Cải tiến
Sử dụng DataSeeder để có dữ liệu đầy đủ
"""
import pytest
from utils.helpers import (
    login_admin, safe_click, wait_for_element_visible,
    get_table_row_count, fill_form_safely
)

class TestAnalytics:
    """Test cases cho thống kê"""
    
    def test_view_analytics_page(self, browser_page):
        """Test hiển thị trang thống kê"""
        page = browser_page
        
        # Login
        assert login_admin(page)
        
        # Navigate to Statistics
        assert safe_click(page, "#sidebar__statistics a")
        assert wait_for_element_visible(page, "#main__statistics")
        
        # Đợi data load
        page.wait_for_timeout(3000)
        
        # Verify các elements chính
        assert wait_for_element_visible(page, "#statistics-product-table__body"), \
            "Bảng thống kê sản phẩm không hiển thị"
        
        assert wait_for_element_visible(page, "#statistics-customer-table__body"), \
            "Bảng thống kê khách hàng không hiển thị"
        
        print("✅ Trang thống kê hiển thị đầy đủ")
    
    def test_statistics_product_has_data(self, browser_page):
        """Test thống kê sản phẩm có dữ liệu"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__statistics a")
        assert wait_for_element_visible(page, "#main__statistics")
        
        page.wait_for_timeout(3000)
        
        # Kiểm tra bảng sản phẩm
        product_row_count = get_table_row_count(
            page,
            "#statistics-product-table__body"
        )
        
        assert product_row_count > 0, \
            f"Không có dữ liệu thống kê sản phẩm (có {product_row_count} dòng)"
        
        print(f"✅ Thống kê {product_row_count} sản phẩm")
    
    def test_statistics_customer_has_data(self, browser_page):
        """Test thống kê khách hàng có dữ liệu"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__statistics a")
        assert wait_for_element_visible(page, "#main__statistics")
        
        page.wait_for_timeout(3000)
        
        # Kiểm tra bảng khách hàng
        customer_row_count = get_table_row_count(
            page,
            "#statistics-customer-table__body"
        )
        
        assert customer_row_count > 0, \
            f"Không có dữ liệu thống kê khách hàng (có {customer_row_count} dòng)"
        
        print(f"✅ Thống kê {customer_row_count} khách hàng")
    
    def test_filter_statistics_by_date(self, browser_page):
        """Test lọc thống kê theo ngày"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__statistics a")
        assert wait_for_element_visible(page, "#main__statistics")
        
        page.wait_for_timeout(3000)
        
        # Lưu số liệu ban đầu
        initial_product_count = get_table_row_count(
            page,
            "#statistics-product-table__body"
        )
        
        # Apply date filter
        page.fill("#statistics__date-start", "2025-09-01")
        page.fill("#statistics__date-end", "2025-10-31")
        assert safe_click(page, "#statistics__date-btn"), "Không thể click lọc"
        
        page.wait_for_timeout(3000)
        
        # Verify vẫn có data (hoặc ít hơn sau khi lọc)
        filtered_count = get_table_row_count(
            page,
            "#statistics-product-table__body"
        )
        
        print(f"✅ Lọc ngày: {initial_product_count} → {filtered_count} sản phẩm")
    
    def test_reset_statistics_filter(self, browser_page):
        """Test reset bộ lọc thống kê"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__statistics a")
        assert wait_for_element_visible(page, "#main__statistics")
        
        page.wait_for_timeout(3000)
        
        # Apply filter
        page.fill("#statistics__date-start", "2025-09-01")
        page.fill("#statistics__date-end", "2025-09-30")
        safe_click(page, "#statistics__date-btn")
        page.wait_for_timeout(2000)
        
        # Reset
        assert safe_click(page, "#statistics__date-reset-btn"), "Không thể click reset"
        page.wait_for_timeout(2000)
        
        # Verify được reset
        assert page.input_value("#statistics__date-start") == "", \
            "Date start không được reset"
        assert page.input_value("#statistics__date-end") == "", \
            "Date end không được reset"
        
        print("✅ Reset filter thành công")
    
    def test_view_total_revenue(self, browser_page):
        """Test hiển thị tổng doanh thu"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__statistics a")
        assert wait_for_element_visible(page, "#main__statistics")
        
        page.wait_for_timeout(3000)
        
        # Kiểm tra có hiển thị tổng doanh thu không
        assert wait_for_element_visible(
            page,
            "#statistics-product__total-revenue",
            timeout=5000
        ), "Không hiển thị tổng doanh thu sản phẩm"
        
        assert wait_for_element_visible(
            page,
            "#statistics-customer__total-revenue",
            timeout=5000
        ), "Không hiển thị tổng doanh thu khách hàng"
        
        # Lấy giá trị doanh thu
        product_revenue = page.text_content("#statistics-product__total-revenue")
        customer_revenue = page.text_content("#statistics-customer__total-revenue")
        
        print(f"✅ Doanh thu sản phẩm: {product_revenue}")
        print(f"✅ Doanh thu khách hàng: {customer_revenue}")
    
    def test_view_special_products(self, browser_page):
        """Test hiển thị sản phẩm đặc biệt (bán chạy nhất/ế nhất)"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__statistics a")
        assert wait_for_element_visible(page, "#main__statistics")
        
        page.wait_for_timeout(3000)
        
        # Kiểm tra có hiển thị special products không
        assert wait_for_element_visible(
            page,
            "#statistics-product__special-product",
            timeout=5000
        ), "Không hiển thị sản phẩm đặc biệt"
        
        # Kiểm tra có bestProduct và worstProduct
        if wait_for_element_visible(page, "#bestProduct", timeout=3000):
            best_product = page.text_content("#bestProduct")
            print(f"✅ Sản phẩm chạy nhất: {best_product}")
        
        if wait_for_element_visible(page, "#worstProduct", timeout=3000):
            worst_product = page.text_content("#worstProduct")
            print(f"✅ Sản phẩm ế nhất: {worst_product}")
    
    def test_top_customers_filter(self, browser_page):
        """Test lọc top khách hàng"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__statistics a")
        assert wait_for_element_visible(page, "#main__statistics")
        
        page.wait_for_timeout(3000)
        
        # Nhập top N
        top_n = "3"
        assert fill_form_safely(page, "statistics-customer__top-input", top_n), \
            "Không thể nhập top N"
        
        # Trigger input event
        page.evaluate("""
            const input = document.getElementById('statistics-customer__top-input');
            input.dispatchEvent(new Event('input', { bubbles: true }));
        """)
        
        page.wait_for_timeout(2000)
        
        # Verify có ít hơn hoặc bằng N khách hàng
        customer_count = get_table_row_count(
            page,
            "#statistics-customer-table__body"
        )
        
        assert customer_count <= int(top_n), \
            f"Hiển thị {customer_count} khách hàng, vượt quá top {top_n}"
        
        print(f"✅ Hiển thị top {customer_count} khách hàng")
    
    def test_view_statistics_bill(self, browser_page):
        """Test xem hóa đơn trong thống kê"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__statistics a")
        assert wait_for_element_visible(page, "#main__statistics")
        
        page.wait_for_timeout(3000)
        
        # Click nút "Hóa đơn" đầu tiên trong bảng sản phẩm
        bill_buttons = page.query_selector_all(".statistics-product__show-bill-btn")
        
        if len(bill_buttons) > 0:
            bill_buttons[0].click()
            page.wait_for_timeout(1000)
            
            # Verify modal hiển thị
            assert wait_for_element_visible(
                page,
                "#modal-detailStatistic",
                timeout=5000
            ), "Modal hóa đơn không hiển thị"
            
            print("✅ Modal hóa đơn thống kê hiển thị")
        else:
            pytest.skip("Không có nút xem hóa đơn")

@pytest.mark.slow
class TestAnalyticsIntegration:
    """Integration tests cho analytics"""
    
    def test_analytics_complete_workflow(self, browser_page):
        """
        Test complete analytics workflow:
        1. View tổng quan
        2. Filter theo ngày
        3. View top customers
        4. Reset
        """
        page = browser_page
        
        # Login
        assert login_admin(page)
        assert safe_click(page, "#sidebar__statistics a")
        assert wait_for_element_visible(page, "#main__statistics")
        
        page.wait_for_timeout(3000)
        
        # 1. View tổng quan
        product_count = get_table_row_count(page, "#statistics-product-table__body")
        customer_count = get_table_row_count(page, "#statistics-customer-table__body")
        print(f"1️⃣ Tổng quan: {product_count} SP, {customer_count} KH")
        
        # 2. Filter theo ngày
        page.fill("#statistics__date-start", "2025-10-01")
        page.fill("#statistics__date-end", "2025-10-31")
        safe_click(page, "#statistics__date-btn")
        page.wait_for_timeout(3000)
        
        filtered_product = get_table_row_count(page, "#statistics-product-table__body")
        print(f"2️⃣ Sau filter: {filtered_product} sản phẩm")
        
        # 3. View top customers
        fill_form_safely(page, "statistics-customer__top-input", "3")
        page.evaluate("""
            document.getElementById('statistics-customer__top-input')
                .dispatchEvent(new Event('input', { bubbles: true }));
        """)
        page.wait_for_timeout(2000)
        
        top_count = get_table_row_count(page, "#statistics-customer-table__body")
        print(f"3️⃣ Top customers: {top_count}")
        
        # 4. Reset
        safe_click(page, "#statistics__date-reset-btn")
        page.wait_for_timeout(3000)
        
        final_count = get_table_row_count(page, "#statistics-product-table__body")
        print(f"4️⃣ Sau reset: {final_count} sản phẩm")
        
        print("✨ Analytics workflow hoàn tất!")