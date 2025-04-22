import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, mock_open, MagicMock
from check_equivalence import load_schema_and_data, qed, synthetic_data, Output
import shutil
import pandas as pd


@pytest.fixture
def mock_conn():
    mock_conn = MagicMock()
    
    mock_conn.execute = MagicMock()
    
    return mock_conn

def test_load_schema_and_data(mock_conn):
    mock_schema_content = 'CREATE TABLE test_table (id INT, name CHAR(50));'
    mock_data_content = 'INSERT INTO test_table VALUES (1, "test");'

    with patch('builtins.open', mock_open()) as mock_file:
        mock_file.return_value.read.side_effect = [
            mock_schema_content, 
            mock_data_content 
        ]

        with patch('duckdb.connect', return_value=mock_conn):
            schema_path = 'test_schema.sql'
            load_path = 'test_data.sql'
            
            conn, schema = load_schema_and_data(schema_path, load_path)
            
            mock_conn.execute.assert_any_call('CREATE TABLE test_table (id INT, name CHAR(50));')
            mock_conn.execute.assert_any_call('INSERT INTO test_table VALUES (1, "test");')
            
            mock_conn.commit.assert_called()


def test_qed():
    schema = """
    CREATE TABLE employees (
      empno      INTEGER,   
      ename      VARCHAR(100),   
      job        VARCHAR(100),   
      mgr        INTEGER,   
      hiredate   DATE,   
      sal        INTEGER,   
      comm       INTEGER,   
      deptno     INTEGER,   
      CONSTRAINT pk_emp PRIMARY KEY (empno),   
      CONSTRAINT no_sal CHECK (sal > 0)   
    );

    CREATE TABLE departments (
      deptno     INTEGER,   
      deptname   VARCHAR(100),   
      location   VARCHAR(100),   
      CONSTRAINT pk_dept PRIMARY KEY (deptno),   
      CONSTRAINT unique_deptname UNIQUE (deptname)   
    );
    """
    
    orig_query = """
    SELECT ename
    FROM employees
    WHERE job = 'Manager';
    """

    optimized_query = """
    SELECT e.ename
    FROM employees e
    WHERE e.job = 'Manager';
    """

    os.makedirs('tmp', exist_ok=True)

    with patch('subprocess.run') as mock_subprocess_run:
        mock_subprocess_run.return_value = MagicMock(stdout="QED: provable for temp.json\n")

        result = qed(schema, orig_query, optimized_query)
        
        assert result == Output.EQUAL
        assert mock_subprocess_run.call_count == 2

    shutil.rmtree('tmp')

def test_qed_with_joins():
    schema = """
    CREATE TABLE employees (
      empno      INTEGER,   
      ename      VARCHAR(100),   
      job        VARCHAR(100),   
      mgr        INTEGER,   
      hiredate   DATE,   
      sal        INTEGER,   
      comm       INTEGER,   
      deptno     INTEGER,   
      CONSTRAINT pk_emp PRIMARY KEY (empno),   
      CONSTRAINT no_sal CHECK (sal > 0)   
    );

    CREATE TABLE departments (
      deptno     INTEGER,   
      deptname   VARCHAR(100),   
      location   VARCHAR(100),   
      CONSTRAINT pk_dept PRIMARY KEY (deptno),   
      CONSTRAINT unique_deptname UNIQUE (deptname)   
    );
    """
    
    orig_query = """
    SELECT e.ename
    FROM employees e
    INNER JOIN departments d ON e.deptno = d.deptno
    WHERE d.deptname = 'Sales';
    """

    optimized_query = """
    SELECT e.ename
    FROM employees e
    WHERE e.deptno IN (
      SELECT d.deptno
      FROM departments d
      WHERE d.deptname = 'Sales'
    );
    """

    os.makedirs('tmp', exist_ok=True)

    with patch('subprocess.run') as mock_subprocess_run:
        mock_subprocess_run.return_value = MagicMock(stdout="QED: provable for temp.json\n")
        
        result = qed(schema, orig_query, optimized_query)
        
        assert result == Output.EQUAL
        assert mock_subprocess_run.call_count == 2

    shutil.rmtree('tmp')

def test_qed_with_left_join():
    schema = """
    CREATE TABLE employees (
      empno      INTEGER,   
      ename      VARCHAR(100),   
      job        VARCHAR(100),   
      mgr        INTEGER,   
      hiredate   DATE,   
      sal        INTEGER,   
      comm       INTEGER,   
      deptno     INTEGER,   
      CONSTRAINT pk_emp PRIMARY KEY (empno),   
      CONSTRAINT no_sal CHECK (sal > 0)   
    );

    CREATE TABLE departments (
      deptno     INTEGER,   
      deptname   VARCHAR(100),   
      location   VARCHAR(100),   
      CONSTRAINT pk_dept PRIMARY KEY (deptno),   
      CONSTRAINT unique_deptname UNIQUE (deptname)   
    );
    """
    
    orig_query = """
    SELECT e.ename
    FROM employees e
    INNER JOIN departments d ON e.deptno = d.deptno
    WHERE d.location = 'New York';
    """

    optimized_query = """
    SELECT e.ename
    FROM employees e
    LEFT JOIN departments d ON e.deptno = d.deptno
    WHERE d.location = 'New York';
    """

    os.makedirs('tmp', exist_ok=True)

    with patch('subprocess.run') as mock_subprocess_run:
        mock_subprocess_run.return_value = MagicMock(stdout="QED: provable for temp.json\n")
        
        result = qed(schema, orig_query, optimized_query)
        
        assert result == Output.EQUAL
        assert mock_subprocess_run.call_count == 2

    shutil.rmtree('tmp')

def test_qed_with_left_join_nonprovable():
    schema = """
    CREATE TABLE employees (
      empno      INTEGER,   
      ename      VARCHAR(100),   
      job        VARCHAR(100),   
      mgr        INTEGER,   
      hiredate   DATE,   
      sal        INTEGER,   
      comm       INTEGER,   
      deptno     INTEGER,   
      CONSTRAINT pk_emp PRIMARY KEY (empno),   
      CONSTRAINT no_sal CHECK (sal > 0)   
    );

    CREATE TABLE departments (
      deptno     INTEGER,   
      deptname   VARCHAR(100),   
      location   VARCHAR(100),   
      CONSTRAINT pk_dept PRIMARY KEY (deptno),   
      CONSTRAINT unique_deptname UNIQUE (deptname)   
    );
    """
    
    orig_query = """
    SELECT e.ename
    FROM employees e
    LEFT JOIN departments d ON e.deptno = d.deptno
    WHERE d.location = 'New York';
    """

    optimized_query = """
    SELECT e.ename
    FROM employees e
    LEFT JOIN departments d ON e.deptno = d.deptno AND d.location = 'New York';
    """

    os.makedirs('tmp', exist_ok=True)

    with patch('subprocess.run') as mock_subprocess_run:
        mock_subprocess_run.return_value = MagicMock(stdout="QED: not provable for temp.json\n")
        
        result = qed(schema, orig_query, optimized_query)
        
        assert result == Output.NEQUAL
        assert mock_subprocess_run.call_count == 2

    shutil.rmtree('tmp')

@pytest.fixture
def mock_conn():
    mock_conn = MagicMock()
    
    mock_conn.execute.return_value.fetchdf.return_value = pd.DataFrame([
        {"ename": "Alice"},
        {"ename": "David"}
    ])

    return mock_conn

def test_synthetic_data_equal(mock_conn):
    orig_query = "SELECT e.ename FROM employees e WHERE e.job = 'Manager';"
    optimized_query = "SELECT e.ename FROM employees e WHERE e.job = 'Manager';"
    
    result = synthetic_data(mock_conn, orig_query, optimized_query)

    assert result == Output.EQUAL
    mock_conn.execute.assert_called_with(optimized_query)

def test_synthetic_data_unequal(mock_conn):
    orig_query = "SELECT e.ename FROM employees e WHERE e.job = 'Manager';"
    optimized_query = "SELECT e.ename FROM employees e WHERE e.job = 'Developer';"
    
    mock_conn.execute.return_value.fetchdf.side_effect = [
        pd.DataFrame([{"ename": "Alice"}]),
        pd.DataFrame([{"ename": "Bob"}]) 
    ]

    result = synthetic_data(mock_conn, orig_query, optimized_query)

    assert result == Output.NEQUAL
    mock_conn.execute.assert_called_with(optimized_query)

def test_synthetic_data_inconclusive(mock_conn):
    orig_query = "SELECT e.ename FROM employees e WHERE e.job = 'Manager';"
    optimized_query = "SELECT e.ename FROM employees e WHERE e.job = 'Data Scientist';"
    
    mock_conn.execute.return_value.fetchdf.side_effect = [
        pd.DataFrame([{"ename": "Alice"}]),
        Exception("Query not supported")
    ]

    result = synthetic_data(mock_conn, orig_query, optimized_query)

    assert result == Output.INCONCLUSIVE
    mock_conn.execute.assert_called_with(optimized_query)