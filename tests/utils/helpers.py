from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import os

# URLs
BASE_URL = "http://127.0.0.1:5500/twilight_admin_K23_2024/index_admin.html"
STORE_URL = "http://127.0.0.1:5500/twilight-store/index.html"

# Timeout constants (ms)
DEFAULT_TIMEOUT = 30000  # 30s
LONG_TIMEOUT = 60000     # 60s  
SHORT_TIMEOUT = 10000    # 10s

def login_admin(page, username="admin", password="admin", timeout=DEFAULT_TIMEOUT):
    """Login admin với timeout handling"""
    try:
        page.goto(BASE_URL, wait_until="networkidle", timeout=timeout)
        page.fill("#username", username, timeout=SHORT_TIMEOUT)
        page.fill("#password", password, timeout=SHORT_TIMEOUT)
        page.click("button:has-text('Đăng nhập')", timeout=SHORT_TIMEOUT)
        page.wait_for_selector("#login-popup", state="hidden", timeout=timeout)
        print("✅ Login admin thành công")
        return True
    except PlaywrightTimeoutError as e:
        print(f"❌ Login admin timeout: {e}")
        return False

def safe_click(page, selector, timeout=DEFAULT_TIMEOUT):
    """Click an toàn với retry và timeout handling"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            page.wait_for_selector(selector, state="visible", timeout=timeout)
            page.click(selector, timeout=SHORT_TIMEOUT)
            print(f"✅ Clicked: {selector}")
            return True
        except PlaywrightTimeoutError:
            if attempt == max_retries - 1:
                print(f"❌ Failed to click after {max_retries} attempts: {selector}")
                return False
            print(f"⚠️  Retry {attempt + 1}/{max_retries} for: {selector}")
            page.wait_for_timeout(1000)
    return False

def safe_fill(page, selector, value, timeout=SHORT_TIMEOUT):
    """Điền dữ liệu vào input một cách an toàn"""
    try:
        page.wait_for_selector(selector, state="visible", timeout=timeout)
        page.fill(selector, value, timeout=SHORT_TIMEOUT)
        print(f"✅ Filled {selector} with value: {value}")
        return True
    except PlaywrightTimeoutError:
        print(f"❌ Timeout: cannot fill {selector}")
        return False
    except Exception as e:
        print(f"❌ Error filling {selector}: {e}")
        return False

def wait_for_element_visible(page, selector, timeout=DEFAULT_TIMEOUT):
    """Đợi element visible với timeout handling"""
    try:
        page.wait_for_selector(selector, state="visible", timeout=timeout)
        print(f"✅ Element visible: {selector}")
        return True
    except PlaywrightTimeoutError:
        print(f"❌ Element not visible: {selector}")
        return False

def assert_element_visible(page, selector, message=""):
    """Assert element is visible"""
    is_visible = wait_for_element_visible(page, selector, timeout=SHORT_TIMEOUT)
    assert is_visible, message or f"Element {selector} should be visible"

def assert_element_hidden(page, selector, message=""):
    """Assert element is hidden"""
    is_hidden = not page.is_visible(selector)
    assert is_hidden, message or f"Element {selector} should be hidden"

def take_screenshot(page, name):
    """Take screenshot for debugging"""
    try:
        os.makedirs("screenshots", exist_ok=True)
        page.screenshot(path=f"screenshots/{name}.png")
        print(f"✅ Screenshot saved: {name}.png")
    except Exception as e:
        print(f"❌ Failed to take screenshot: {e}")

def wait_for_navigation(page, timeout=DEFAULT_TIMEOUT):
    """Đợi navigation hoàn tất"""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
        return True
    except PlaywrightTimeoutError:
        print("⚠️  Navigation timeout")
        return False

def fill_form_safely(page, field_id, value, timeout=SHORT_TIMEOUT):
    """Fill form field một cách an toàn"""
    try:
        page.wait_for_selector(f"#{field_id}", state="visible", timeout=timeout)
        page.fill(f"#{field_id}", value, timeout=SHORT_TIMEOUT)
        return True
    except PlaywrightTimeoutError:
        print(f"❌ Cannot fill field: {field_id}")
        return False

def get_table_row_count(page, table_selector, timeout=SHORT_TIMEOUT):
    """Đếm số dòng trong bảng một cách an toàn"""
    try:
        page.wait_for_selector(table_selector, state="visible", timeout=timeout)
        rows = page.query_selector_all(f"{table_selector} tr")
        return len(rows)
    except PlaywrightTimeoutError:
        return 0

def verify_alert_message(page, expected_text, timeout=SHORT_TIMEOUT):
    """Verify custom alert message"""
    try:
        alert_selector = "#custom-alert .custom-alert__msg"
        page.wait_for_selector(alert_selector, state="visible", timeout=timeout)
        actual_text = page.text_content(alert_selector)
        return expected_text in actual_text
    except PlaywrightTimeoutError:
        return False

def close_modal(page, modal_selector, timeout=SHORT_TIMEOUT):
    """Đóng modal một cách an toàn"""
    try:
        close_btn = f"{modal_selector} .close-pop, {modal_selector} .modal-close-btn"
        if page.is_visible(close_btn):
            safe_click(page, close_btn, timeout)
            return True
        return False
    except:
        return False

def register_new_user(page, timeout=DEFAULT_TIMEOUT):
    """KHÔNG NÊN DÙNG - Sử dụng DataSeeder thay thế"""
    print("⚠️  Warning: Đang dùng register qua UI - nên dùng DataSeeder.seed_customers()")
    username = f"testuser{page.evaluate('Math.floor(Math.random() * 10000)')}"
    password = "Test@1231"
    try:
        page.goto(STORE_URL, wait_until="networkidle", timeout=timeout)
        safe_click(page, ".nav-link", timeout=SHORT_TIMEOUT)
        page.wait_for_selector("#register-form", timeout=SHORT_TIMEOUT)
        safe_click(page, ".auto-form_switch-btn", timeout=SHORT_TIMEOUT)
        page.fill("#register-form input[placeholder='Tài khoản của bạn']", username)
        page.fill("#register-form input[placeholder='Mật khẩu của bạn']", password)
        page.fill("#register-form input[placeholder='Nhập lại mật khẩu']", password)
        safe_click(page, "#register-form button.btn--primary", timeout=SHORT_TIMEOUT)
        page.wait_for_timeout(2000)
        print(f"✅ Đăng ký thành công: {username}")
        return username, password
    except PlaywrightTimeoutError as e:
        print(f"❌ Đăng ký timeout: {e}")
        return None, None

def create_test_order(page, username, password, timeout=LONG_TIMEOUT):
    """KHÔNG NÊN DÙNG - Sử dụng DataSeeder thay thế"""
    print("⚠️  Warning: Đang tạo order qua UI - nên dùng DataSeeder.seed_orders()")
    try:
        page.goto(STORE_URL, wait_until="networkidle", timeout=timeout)
        safe_click(page, ".nav-link", timeout=SHORT_TIMEOUT)
        page.wait_for_selector("#login-form", timeout=SHORT_TIMEOUT)
        page.fill("#login-form input[placeholder='Tài khoản của bạn']", username)
        page.fill("#login-form input[placeholder='Mật khẩu của bạn']", password)
        safe_click(page, "#login-form button.btn--primary", timeout=SHORT_TIMEOUT)
        page.wait_for_timeout(2000)
        page.wait_for_selector("#productContainer .home-product-item", timeout=timeout)
        safe_click(page, "#productContainer .home-product-item", timeout=SHORT_TIMEOUT)
        page.wait_for_timeout(1000)
        if page.is_visible(".submit-to-cart"):
            safe_click(page, ".submit-to-cart", timeout=SHORT_TIMEOUT)
            page.wait_for_timeout(1000)
        print("✅ Đã tạo order test")
        return True
    except PlaywrightTimeoutError as e:
        print(f"❌ Tạo order timeout: {e}")
        return False