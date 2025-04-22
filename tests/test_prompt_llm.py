import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, mock_open
from prompt_llm import get_optimized_query, write_output_file

def test_write_output_file_basic():
    query_pairs = [
        ("SELECT * FROM employees", "SELECT id, name FROM employees"),
        ("SELECT * FROM departments", "SELECT deptno, deptname FROM departments")
    ]

    with patch("builtins.open", mock_open()) as mock_file:
        write_output_file(query_pairs, "output.txt")
        
        mock_file.assert_called_with("output.txt", "w")
        
        mock_file().write.assert_any_call("User Query: SELECT * FROM employees\n")
        mock_file().write.assert_any_call("Optimized Query: SELECT id, name FROM employees\n\n")
        mock_file().write.assert_any_call("User Query: SELECT * FROM departments\n")
        mock_file().write.assert_any_call("Optimized Query: SELECT deptno, deptname FROM departments\n\n")

def test_write_output_file_empty_queries():
    query_pairs = []
    
    with patch("builtins.open", mock_open()) as mock_file:
        write_output_file(query_pairs, "output.txt")
        
        mock_file().write.assert_not_called()

def test_write_output_file_single_pair():
    query_pairs = [
        ("SELECT * FROM employees", "SELECT id, name FROM employees")
    ]

    with patch("builtins.open", mock_open()) as mock_file:
        write_output_file(query_pairs, "output.txt")
        
        mock_file().write.assert_any_call("User Query: SELECT * FROM employees\n")
        mock_file().write.assert_any_call("Optimized Query: SELECT id, name FROM employees\n\n")

def test_write_output_file_open_failure():
    query_pairs = [
        ("SELECT * FROM employees", "SELECT id, name FROM employees")
    ]
    
    with patch("builtins.open", side_effect=IOError("Unable to open file")):
        with pytest.raises(IOError):
            write_output_file(query_pairs, "output.txt")

def test_prompt_llm():
    query = """SELECT e.ename
    FROM employees e
    INNER JOIN departments d ON e.deptno = d.deptno
    WHERE d.location = 'New York';"""

    schema = """CREATE TABLE employees (
    empno      INTEGER PRIMARY KEY,
    ename      VARCHAR(100),
    job        VARCHAR(100),
    mgr        INTEGER,
    hiredate   DATE,
    sal        INTEGER,
    comm       INTEGER,
    deptno     INTEGER
    );

    CREATE TABLE departments (
    deptno     INTEGER PRIMARY KEY,
    deptname   VARCHAR(100),
    location   VARCHAR(100)
    );
    """

    stats = """employees: 1000
    departments: 100
    """

    workload_stats = schema + '\n' + stats

    # can remove the mock if want to test the actual API call
    fake_response = {
        'choices': [{
            'message': {
                'content': """SELECT e.ename 
                    FROM employees e 
                    WHERE e.deptno IN (
                        SELECT d.deptno 
                        FROM departments d 
                        WHERE d.location = 'New York'
                    );"""
            }
        }]
    }

    with patch('openai.ChatCompletion.create', return_value=fake_response):
        optimized = get_optimized_query(query, workload_stats)

    assert optimized is not None
    assert isinstance(optimized, str)
    assert "SELECT" in optimized
    assert "FROM" in optimized
    assert ";" in optimized