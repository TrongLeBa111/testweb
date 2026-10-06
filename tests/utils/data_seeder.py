"""
Data Seeder - Tạo dữ liệu test trực tiếp vào localStorage
Giải quyết vấn đề timeout khi tạo dữ liệu qua UI
"""
import json
from datetime import datetime, timedelta
import random

class DataSeeder:
    """Seed dữ liệu test vào localStorage"""
    
    def __init__(self, page):
        self.page = page
        
    def seed_customers(self, count=5):
        """Seed khách hàng vào localStorage"""
        customers = []
        for i in range(count):
            customer = {
                "username": f"testuser{i}",
                "password": "Test@01234",
                "phone": f"09{str(random.randint(10000000, 99999999))}",
                "name": f"Test User {i}",
                "address": {
                    "city": "TP.HCM",
                    "district": "Quận 1",
                    "numberAndRoad": f"{random.randint(1, 999)} Nguyễn Văn Linh"
                },
                "infoCard": {
                    "cardNumber": "",
                    "expiryDate": "",
                    "cvv": "",
                    "cardholderName": "",
                    "billingAddress": "",
                    "zipCode": ""
                },
                "locked": False
            }
            customers.append(customer)
        
        # Inject vào localStorage
        self.page.evaluate(f"localStorage.setItem('customerArray', JSON.stringify({json.dumps(customers)}))")
        return customers
    
    def seed_orders(self, username="testuser0", count=10):
        """Seed đơn hàng vào localStorage"""
        orders = []
        
        # Sample products cho orders
        sample_products = [
            {
                "name": "iPhone 14 Pro Max",
                "brandId": "APPLE",
                "price": 29990000,
                "pb": "256GB/8GB",
                "quantity": 1,
                "img": "../common/images/img-prd/iphone14promax.png"
            },
            {
                "name": "Samsung Galaxy S23 Ultra",
                "brandId": "SAMSUNG", 
                "price": 25990000,
                "pb": "512GB/12GB",
                "quantity": 2,
                "img": "../common/images/img-prd/s23ultra.png"
            },
            {
                "name": "Xiaomi 13 Pro",
                "brandId": "XIAOMI",
                "price": 18990000,
                "pb": "256GB/12GB",
                "quantity": 1,
                "img": "../common/images/img-prd/xiaomi13pro.png"
            }
        ]
        
        statuses = ["UNPROCESSED", "CONFIRMED", "SUCCEEDED", "FAILED"]
        
        for i in range(count):
            # Random date trong 30 ngày qua
            order_date = datetime.now() - timedelta(days=random.randint(0, 30))
            
            # Random 1-3 sản phẩm
            num_products = random.randint(1, 3)
            checkout_cart = random.sample(sample_products, num_products)
            
            order = {
                "id": f"ORD{str(i).zfill(5)}",
                "customerId": username,
                "name": f"Test User {username[-1]}",
                "phone": f"09{str(random.randint(10000000, 99999999))}",
                "address": {
                    "city": "TP.HCM",
                    "district": f"Quận {random.randint(1, 12)}",
                    "numberAndRoad": f"{random.randint(1, 999)} Nguyễn Văn Linh"
                },
                "checkoutCart": checkout_cart,
                "date": order_date.isoformat(),
                "status": random.choice(statuses)
            }
            orders.append(order)
        
        # Inject vào localStorage
        self.page.evaluate(f"localStorage.setItem('orderArray', JSON.stringify({json.dumps(orders)}))")
        return orders
    
    def seed_cart(self, username="testuser0", product_count=3):
        """Seed giỏ hàng vào localStorage"""
        sample_products = [
            {
                "name": "iPhone 14 Pro Max",
                "brandId": "APPLE",
                "price": 29990000,
                "pb": "256GB/8GB",
                "quantity": 1,
                "isPicked": False,
                "img": "../common/images/img-prd/iphone14promax.png"
            },
            {
                "name": "Samsung Galaxy S23 Ultra",
                "brandId": "SAMSUNG",
                "price": 25990000,
                "pb": "512GB/12GB", 
                "quantity": 2,
                "isPicked": False,
                "img": "../common/images/img-prd/s23ultra.png"
            }
        ]
        
        cart = {
            "cartItem": sample_products[:product_count],
            "counterProducts": sum(p["quantity"] for p in sample_products[:product_count])
        }
        
        cart_key = f"cart_{username}"
        self.page.evaluate(f"localStorage.setItem('{cart_key}', JSON.stringify({json.dumps(cart)}))")
        return cart
    
    def seed_all_test_data(self, customer_count=5, order_count=20):
        """Seed toàn bộ dữ liệu test cần thiết"""
        print("🌱 Bắt đầu seed dữ liệu test...")
        
        # 1. Seed customers
        customers = self.seed_customers(customer_count)
        print(f"✅ Đã seed {len(customers)} customers")
        
        # 2. Seed orders cho mỗi customer
        all_orders = []
        for customer in customers:
            orders = self.seed_orders(
                username=customer['username'],
                count=order_count // customer_count
            )
            all_orders.extend(orders)
        print(f"✅ Đã seed {len(all_orders)} orders")
        
        # 3. Seed cart cho customer đầu tiên
        cart = self.seed_cart(customers[0]['username'])
        print(f"✅ Đã seed cart với {cart['counterProducts']} sản phẩm")
        
        # 4. Set current user
        self.page.evaluate(f"localStorage.setItem('currentUser', JSON.stringify(''))")
        
        print("✨ Hoàn tất seed dữ liệu test!")
        
        return {
            'customers': customers,
            'orders': all_orders,
            'cart': cart
        }
    
    def clear_all_data(self):
        """Xóa toàn bộ dữ liệu test"""
        self.page.evaluate("localStorage.clear()")
        print("🗑️  Đã xóa toàn bộ dữ liệu test")
    
    def seed_specific_order_for_filter_test(self, username="testuser0"):
        """Seed đơn hàng cụ thể để test filter"""
        orders = [
            # Đơn hàng tháng 9
            {
                "id": "ORD00001",
                "customerId": username,
                "name": "Test User",
                "phone": "0912345678",
                "address": {
                    "city": "TP.HCM",
                    "district": "Quận 1",
                    "numberAndRoad": "123 Nguyễn Văn Linh"
                },
                "checkoutCart": [{
                    "name": "iPhone 14 Pro Max",
                    "price": 29990000,
                    "pb": "256GB/8GB",
                    "quantity": 1,
                    "img": "../common/images/img-prd/iphone14promax.png"
                }],
                "date": "2025-09-15T00:00:00.000Z",
                "status": "UNPROCESSED"
            },
            # Đơn hàng tháng 10
            {
                "id": "ORD00002",
                "customerId": username,
                "name": "Test User",
                "phone": "0912345678",
                "address": {
                    "city": "TP.HCM",
                    "district": "Quận 2",
                    "numberAndRoad": "456 Lê Văn Việt"
                },
                "checkoutCart": [{
                    "name": "Samsung Galaxy S23",
                    "price": 25990000,
                    "pb": "512GB/12GB",
                    "quantity": 1,
                    "img": "../common/images/img-prd/s23.png"
                }],
                "date": "2025-10-20T00:00:00.000Z",
                "status": "CONFIRMED"
            }
        ]
        
        self.page.evaluate(f"localStorage.setItem('orderArray', JSON.stringify({json.dumps(orders)}))")
        return orders