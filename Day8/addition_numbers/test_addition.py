from addition import add,subtract,multiply,divide

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

def test_add_mixed_numbers():
    assert add(2, -3) == -1

def test_add_zero():
    assert add(0, 5) == 5
    assert add(5, 0) == 5
def test_add_floats():
    assert add(2.5, 3.1) == 5.6
    assert add(-2.5, -3.1) == -5.6
    assert add(2.5, -3.1) == -0.6000000000000001

def test_subtract_positive_numbers():
    assert subtract(5, 3) == 2  

def test_subtract_negative_numbers():
    assert subtract(-5, -3) == -2   

def test_multiply_zero():
    assert multiply(5, 0) == 0
    assert multiply(0, 5) == 0

def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass  # Expected behavior
    else:
        assert False, "Expected ZeroDivisionError"