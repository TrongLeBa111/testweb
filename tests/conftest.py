"""
Pytest Configuration - Cải tiến với DataSeeder
"""
import pytest
from playwright.sync_api import sync_playwright
from utils.data_seeder import DataSeeder
from utils.helpers import BASE_URL, LONG_TIMEOUT

@pytest.fixture(scope="session")
def browser():
    """Browser fixture cho toàn bộ test session"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # Set True khi chạy CI/CD
            slow_mo=50       # Làm chậm để dễ debug
        )
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def browser_page(browser):
    """
    Page fixture - Tạo page mới và seed data cho mỗi test
    Scope="function" đảm bảo mỗi test có environment riêng
    """
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )
    page = context.new_page()
    
    # Set default timeout
    page.set_default_timeout(LONG_TIMEOUT)
    
    # Navigate to admin page first (để có thể access localStorage)
    page.goto(BASE_URL, wait_until="networkidle")
    
    # Seed dữ liệu test
    seeder = DataSeeder(page)
    seeder.seed_all_test_data(
        customer_count=5,
        order_count=20
    )
    
    yield page
    
    # Cleanup: Clear data sau mỗi test
    seeder.clear_all_data()
    context.close()

@pytest.fixture(scope="function")
def data_seeder(browser_page):
    """
    DataSeeder fixture - Để test có thể seed thêm data đặc biệt
    """
    return DataSeeder(browser_page)

@pytest.fixture(scope="function") 
def empty_page(browser):
    """
    Empty page fixture - Không seed data
    Dùng khi test cần kiểm tra trạng thái empty
    """
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )
    page = context.new_page()
    page.set_default_timeout(LONG_TIMEOUT)
    
    # Navigate và clear data
    page.goto(BASE_URL, wait_until="networkidle")
    page.evaluate("localStorage.clear()")
    
    yield page
    context.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Setup môi trường test - chạy một lần duy nhất
    """
    print("\n" + "="*50)
    print("🚀 Bắt đầu Test Suite")
    print("="*50)
    
    yield
    
    print("\n" + "="*50)
    print("✨ Kết thúc Test Suite")
    print("="*50)

# Pytest configuration
def pytest_configure(config):
    """Cấu hình pytest"""
    config.addinivalue_line(
        "markers", 
        "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test items - thêm markers tự động"""
    for item in items:
        # Tự động mark các test có "integration" trong tên
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)