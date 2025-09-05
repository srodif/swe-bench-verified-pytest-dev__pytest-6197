import pytest

def test_init_py_regression_default_patterns(testdir):
    """Test that __init__.py files are not collected with default python_files patterns.
    
    This is a regression test for pytest 5.2.3 where random __init__.py files
    were being collected even when they don't match python_files patterns.
    """
    # Create a non-test package with an __init__.py that would fail if imported.
    non_test_pkg = testdir.mkdir("non_test_package")
    non_test_pkg.ensure("__init__.py").write("assert False, 'This should not be collected'")
    
    # Create a real test file
    testdir.makepyfile(test_something="def test_something(): pass")
    
    # Run pytest with collect-only to see what gets collected
    result = testdir.runpytest("--collect-only")
    
    # Should collect the real test
    assert "test_something" in result.stdout.str()
    
    # Should NOT collect the __init__.py
    assert "non_test_package" not in result.stdout.str()
    
    # Run pytest normally - should not fail due to the assert False
    result = testdir.runpytest()
    
    # Should pass the real test
    assert "1 passed" in result.stdout.str()
    assert result.ret == 0


def test_init_py_collected_with_wildcard_python_files(testdir):
    """Test that __init__.py files ARE collected when python_files includes *.py."""
    # Configure python_files to include all .py files
    testdir.makeini("[pytest]\npython_files = *.py")
    
    # Create a test package with a test in __init__.py
    test_pkg = testdir.mkdir("test_package")
    test_pkg.ensure("__init__.py").write("def test_in_init(): pass")
    
    # Run pytest with collect-only to see what gets collected
    result = testdir.runpytest("--collect-only")
    
    # Should collect the test in __init__.py
    assert "__init__.py" in result.stdout.str()
    assert "test_in_init" in result.stdout.str()
    
    # Run pytest normally
    result = testdir.runpytest()
    
    # Should pass the test in __init__.py
    assert "1 passed" in result.stdout.str()
    assert result.ret == 0
