"""
Data Manager để quản lý test data
"""
from utils.helpers import register_new_user, create_test_order

class DataManager:
    """Quản lý tạo và cleanup test data"""
    
    def __init__(self, page):
        self.page = page
        self.created_users = []
        self.created_orders = []
    
    def create_test_user(self):
        """Tạo 1 user test"""
        username, password = register_new_user(self.page)
        self.created_users.append({'username': username, 'password': password})
        return username, password
    
    def create_test_order(self, username=None, password=None):
        """Tạo 1 đơn hàng test"""
        order_info = create_test_order(self.page, username, password)
        self.created_orders.append(order_info)
        return order_info
    
    def setup_analytics_data(self, order_count=5):
        """Tạo dữ liệu cho analytics/statistics"""
        test_data = []
        
        for i in range(order_count):
            # Tạo user mới
            username, password = self.create_test_user()
            
            # Tạo đơn hàng cho user này
            order_info = self.create_test_order(username, password)
            
            test_data.append({
                'username': username,
                'password': password,
                'order': order_info
            })
        
        return test_data
    
    def cleanup(self):
        """Cleanup test data nếu cần"""
        # Note: Vì dữ liệu lưu trong localStorage,
        # có thể cần thêm logic để xóa test data
        # Hiện tại để trống vì mỗi test chạy độc lập
        self.created_users.clear()
        self.created_orders.clear()