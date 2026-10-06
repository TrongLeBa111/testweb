# Hướng Dẫn Chạy Tests với Playwright

## Cấu Trúc Thư Mục

```
project/
│
├── conftest.py                 # Pytest fixtures
├── pytest.ini                  # Pytest configuration
│
├── data/
│   └── fixtures.py            # Test data factory
│
├── utils/
│   ├── helpers.py             # Helper functions
│   ├── base_test.py           # Base test class
│   └── data_manager.py        # Data manager
│
└── tests/
    ├── test_product_improved.py
    ├── test_order_improved.py
    ├── test_customer.py
    └── test_analytics.py
```

## Cài Đặt

### 1. Cài đặt dependencies

```bash
pip install pytest playwright pytest-playwright
```

### 2. Cài đặt browsers cho Playwright

```bash
playwright install chromium
```

### 3. Khởi động local server

Đảm bảo server đang chạy trên:
- Admin: `http://127.0.0.1:5500/twilight_admin_K23_2024/index_admin.html`
- Store: `http://127.0.0.1:5500/twilight-store/index.html`

## Chạy Tests

### Chạy tất cả tests

```bash
pytest
```

### Chạy test file cụ thể

```bash
pytest tests/test_product_improved.py
```

### Chạy test function cụ thể

```bash
pytest tests/test_product_improved.py::TestProduct::test_add_product_success
```

### Chạy với browser hiển thị (không headless)

```bash
pytest --headed
```

### Chạy với browser cụ thể

```bash
pytest --browser=chromium
pytest --browser=firefox
pytest --browser=webkit
```

### Chạy với slow motion (để debug)

```bash
pytest --slowmo=1000
```

### Chạy tests với markers

```bash
# Chỉ chạy smoke tests
pytest -m smoke

# Bỏ qua slow tests
pytest -m "not slow"
```

### Chạy tests song song (nhanh hơn)

```bash
pip install pytest-xdist
pytest -n auto
```

## Debug Tests

### 1. Sử dụng breakpoint

```python
def test_something(browser_page):
    page = browser_page
    # ... code ...
    
    import pdb; pdb.set_trace()  # Dừng ở đây
    
    # ... code tiếp ...
```

### 2. Chụp screenshot khi test fail

```python
def test_something(browser_page):
    page = browser_page
    try:
        # ... test code ...
        pass
    except Exception as e:
        page.screenshot(path="test_failed.png")
        raise
```

### 3. Xem browser khi chạy test

```bash
pytest --headed --slowmo=500 tests/test_product_improved.py
```

## Giải Quyết Vấn Đề Thường Gặp

### 1. Timeout errors

Tăng timeout trong code:
```python
page.wait_for_selector("#element", timeout=10000)  # 10 giây
```

Hoặc config global timeout trong pytest.ini

### 2. Element not found

- Đảm bảo đã login admin trước
- Kiểm tra selector đúng chưa
- Sử dụng `wait_for_selector` thay vì click ngay

### 3. Data không hiển thị

- Kiểm tra localStorage có data không
- Tạo test data trước khi test
- Reset filters nếu cần

### 4. Tests chạy không ổn định

- Thêm `page.wait_for_timeout()` sau actions
- Sử dụng `safe_click()` thay vì `click()`
- Đợi elements visible trước khi interact

## Best Practices

### 1. Tạo test data độc lập

```python
def test_something(browser_page, data_manager):
    # Tạo data riêng cho test này
    data_manager.create_test_order()
    # ... test code ...
```

### 2. Sử dụng fixtures

```python
@pytest.fixture
def logged_in_admin(browser_page):
    login_admin(browser_page)
    return browser_page

def test_something(logged_in_admin):
    page = logged_in_admin
    # Đã login sẵn
```

### 3. Cleanup sau tests

```python
def test_something(browser_page, data_manager):
    # Test code
    pass
    # data_manager.cleanup() tự động chạy