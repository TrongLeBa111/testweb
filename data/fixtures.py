import random
import json
from pathlib import Path

class TestDataFactory:
    """Factory class để tạo test data"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "samples"
    
    def create_customer_data(self, **overrides):
        """Tạo customer data"""
        base_data = {
            'name': f'testuser_{random.randint(1000, 9999)}',
            'password': 'Test@123',
            'phone': f'012345{random.randint(1000, 9999)}',
            'address': 'Test Address, Test City, Test Province'
        }
        base_data.update(overrides)
        return base_data
    
    def create_product_data(self, **overrides):
        """Tạo product data"""
        brands = ['SAMSUNG', 'APPLE', 'XIAOMI', 'OPPO']
        base_data = {
            'name': f'Test Phone {random.randint(100, 999)}',
            'brand': random.choice(brands),
            'versions': 1,
            'price': random.randint(5000000, 50000000),
            'chip': f'TestChip {random.randint(100, 999)}',
            'battery': f'{random.randint(3000, 6000)}mAh',
            'screen_size': f'{random.uniform(5.0, 7.0):.1f}',
            'refresh_rate': f'{random.choice([60, 90, 120])}Hz'
        }
        base_data.update(overrides)
        return base_data
    
    def create_order_data(self, customer_data=None, products=None):
        """Tạo order data"""
        if not customer_data:
            customer_data = self.create_customer_data()
        
        if not products:
            products = [self.create_product_data()]
        
        return {
            'customer': customer_data,
            'products': products,
            'order_date': '2025-09-27',
            'status': 'pending'
        }
    
    def load_sample_data(self, filename):
        """Load static sample data từ JSON files"""
        file_path = self.data_dir / filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def create_bulk_test_data(self, customers=5, products=10, orders=3):
        """Tạo bulk data cho performance tests"""
        return {
            'customers': [self.create_customer_data() for _ in range(customers)],
            'products': [self.create_product_data() for _ in range(products)], 
            'orders': [self.create_order_data() for _ in range(orders)]
        }