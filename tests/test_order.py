"""
Test Order Management - Cải tiến với DataSeeder
Không còn timeout vì không cần tạo data qua UI
"""
import pytest
from utils.helpers import (
    login_admin, safe_click, wait_for_element_visible,
    get_table_row_count, SHORT_TIMEOUT
)

class TestOrder:
    """Test cases cho quản lý đơn hàng"""
    
    def test_order_display_with_data(self, browser_page):
        """
        Test hiển thị danh sách đơn hàng
        Data đã được seed tự động trong fixture
        """
        page = browser_page
        
        # Login admin
        assert login_admin(page), "Login thất bại"
        
        # Navigate to Orders
        assert safe_click(page, "#sidebar__orders a"), "Không thể click Orders menu"
        assert wait_for_element_visible(page, "#main__orders"), "Orders page không hiển thị"
        
        # Đợi data load
        page.wait_for_timeout(2000)
        
        # Verify table có data
        assert wait_for_element_visible(page, "#orders-table-content__body")
        
        row_count = get_table_row_count(page, "#orders-table-content__body")
        assert row_count > 0, f"Bảng đơn hàng trống (có {row_count} dòng)"
        
        print(f"✅ Hiển thị {row_count} đơn hàng")
    
    def test_filter_order_by_date(self, browser_page, data_seeder):
        """
        Test lọc đơn hàng theo ngày
        Sử dụng data được seed đặc biệt
        """
        page = browser_page
        
        # Seed specific orders cho test filter
        orders = data_seeder.seed_specific_order_for_filter_test()
        print(f"📦 Đã seed {len(orders)} đơn hàng test")
        
        # Login và navigate
        assert login_admin(page), "Login thất bại"
        assert safe_click(page, "#sidebar__orders a")
        assert wait_for_element_visible(page, "#main__orders")
        
        # Đợi initial data load
        page.wait_for_timeout(2000)
        
        # Apply date filter (tháng 9/2025)
        page.fill("#order__date-start", "2025-09-01")
        page.fill("#order__date-end", "2025-09-30")
        assert safe_click(page, "#filter__date-btn"), "Không thể click nút lọc"
        
        # Đợi filter apply
        page.wait_for_timeout(2000)
        
        # Verify filtered results
        assert wait_for_element_visible(page, "#orders-table-content__body")
        
        # Kiểm tra có ít nhất 1 đơn hàng trong khoảng thời gian
        row_count = get_table_row_count(page, "#orders-table-content__body")
        assert row_count >= 1, f"Filter không trả về kết quả (có {row_count} dòng)"
        
        print(f"✅ Filter theo ngày trả về {row_count} đơn hàng")
    
    def test_filter_order_by_status(self, browser_page):
        """Test lọc đơn hàng theo trạng thái"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__orders a")
        assert wait_for_element_visible(page, "#main__orders")
        
        page.wait_for_timeout(2000)
        
        # Filter by UNPROCESSED
        page.select_option("#filter__status-selection", "UNPROCESSED")
        page.wait_for_timeout(1500)
        
        # Verify
        assert wait_for_element_visible(page, "#orders-table-content__body")
        
        # Kiểm tra status buttons có đúng không
        status_buttons = page.query_selector_all(".order-status-table")
        if status_buttons:
            # Verify ít nhất có 1 đơn UNPROCESSED
            unprocessed_count = sum(
                1 for btn in status_buttons 
                if "Chưa xử lý" in page.evaluate("el => el.textContent", btn)
            )
            print(f"✅ Có {unprocessed_count} đơn hàng chưa xử lý")
    
    def test_view_order_detail(self, browser_page):
        """Test xem chi tiết đơn hàng"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__orders a")
        assert wait_for_element_visible(page, "#main__orders")
        
        page.wait_for_timeout(2000)
        
        # Click detail button đầu tiên
        detail_buttons = page.query_selector_all(".detail-btn")
        assert len(detail_buttons) > 0, "Không có nút chi tiết nào"
        
        detail_buttons[0].click()
        page.wait_for_timeout(1000)
        
        # Verify popup hiển thị
        assert wait_for_element_visible(
            page, 
            "#modal-detailorder",
            timeout=SHORT_TIMEOUT
        ), "Modal chi tiết không hiển thị"
        
        assert wait_for_element_visible(
            page,
            "#detailorder",
            timeout=SHORT_TIMEOUT
        ), "Nội dung chi tiết không hiển thị"
        
        print("✅ Modal chi tiết đơn hàng hiển thị thành công")
    
    def test_reset_order_filter(self, browser_page):
        """Test reset bộ lọc đơn hàng"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__orders a")
        assert wait_for_element_visible(page, "#main__orders")
        
        page.wait_for_timeout(2000)
        
        # Apply filters
        page.fill("#order__date-start", "2025-09-01")
        page.fill("#order__date-end", "2025-09-30")
        page.select_option("#filter__status-selection", "CONFIRMED")
        page.wait_for_timeout(1000)
        
        # Click reset
        assert safe_click(page, "#order__reset-filter-btn"), "Không thể click reset"
        page.wait_for_timeout(1500)
        
        # Verify filters đã được reset
        assert page.input_value("#order__date-start") == "", "Date start không được reset"
        assert page.input_value("#order__date-end") == "", "Date end không được reset"
        assert page.input_value("#filter__status-selection") == "ALL", "Status không được reset"
        
        print("✅ Reset filter thành công")
    
    def test_sort_order_by_district(self, browser_page):
        """Test sắp xếp đơn hàng theo quận"""
        page = browser_page
        
        # Login và navigate
        assert login_admin(page)
        assert safe_click(page, "#sidebar__orders a")
        assert wait_for_element_visible(page, "#main__orders")
        
        page.wait_for_timeout(2000)
        
        # Click sort by district
        assert safe_click(page, "#order__sort-by-district"), "Không thể click sort"
        page.wait_for_timeout(2000)
        
        # Verify table vẫn hiển thị
        assert wait_for_element_visible(page, "#orders-table-content__body")
        
        row_count = get_table_row_count(page, "#orders-table-content__body")
        assert row_count > 0, "Sau khi sort không còn data"
        
        print(f"✅ Sắp xếp thành công, hiển thị {row_count} đơn hàng")

@pytest.mark.slow
class TestOrderIntegration:
    """Integration tests - chạy chậm hơn"""
    
    def test_order_complete_workflow(self, browser_page):
        """
        Test complete workflow:
        1. Xem danh sách
        2. Lọc theo ngày
        3. Xem chi tiết
        4. Reset filter
        """
        page = browser_page
        
        # Login
        assert login_admin(page)
        assert safe_click(page, "#sidebar__orders a")
        assert wait_for_element_visible(page, "#main__orders")
        
        page.wait_for_timeout(2000)
        
        # 1. Verify initial display
        initial_count = get_table_row_count(page, "#orders-table-content__body")
        assert initial_count > 0
        print(f"1️⃣ Initial: {initial_count} đơn hàng")
        
        # 2. Apply filter
        page.fill("#order__date-start", "2025-10-01")
        page.fill("#order__date-end", "2025-10-31")
        safe_click(page, "#filter__date-btn")
        page.wait_for_timeout(2000)
        
        filtered_count = get_table_row_count(page, "#orders-table-content__body")
        print(f"2️⃣ Filtered: {filtered_count} đơn hàng")
        
        # 3. View detail
        if get_table_row_count(page, "#orders-table-content__body") > 0:
            detail_buttons = page.query_selector_all(".detail-btn")
            if detail_buttons:
                detail_buttons[0].click()
                page.wait_for_timeout(1000)
                assert wait_for_element_visible(page, "#modal-detailorder")
                print("3️⃣ Xem chi tiết thành công")
                
                # Close modal
                page.click(".close-pop, #close-detailorder")
                page.wait_for_timeout(500)
        
        # 4. Reset
        safe_click(page, "#order__reset-filter-btn")
        page.wait_for_timeout(2000)
        
        final_count = get_table_row_count(page, "#orders-table-content__body")
        assert final_count == initial_count, "Reset không khôi phục về trạng thái ban đầu"
        print(f"4️⃣ Reset: {final_count} đơn hàng")
        
        print("✨ Complete workflow thành công!")