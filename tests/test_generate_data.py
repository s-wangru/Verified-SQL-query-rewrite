import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
from unittest.mock import mock_open, patch
import pytest
from generate_data import parse_schema, generate_value, generate_dat_file, generate_data, DELIMITER

INT32_MIN = -(2**31)  # -2147483648
INT32_MAX = 2**31 - 1  # 2147483647

def test_parse_schema_valid_1():
    schema_sql = """
    CREATE TABLE employees (
        id INT,
        name VARCHAR,
        salary DOUBLE,
        hired_at DATE
    );
    """
    result = parse_schema(schema_sql)
    expected = [
        ('id', 'INT'),
        ('name', 'VARCHAR'),
        ('salary', 'DOUBLE'),
        ('hired_at', 'DATE')
    ]
    assert result == expected, result

def test_parse_schema_valid_2():
    schema_sql = """
    CREATE TABLE employees (
        id INT,
        name VARCHAR,
        salary DOUBLE,
        hired_at DATE
    );
    """
    result = parse_schema(schema_sql)
    expected = [
        ('id', 'INT'),
        ('name', 'VARCHAR'),
        ('salary', 'DOUBLE'),
        ('hired_at', 'DATE')
    ]
    assert result == expected, result

def test_parse_schema_invalid_1():
    schema_sql = """
    CREATE TABLE employees (
        id INT,
        name VARCHAR,
        primary key (p_key)
    );
    """
    result = parse_schema(schema_sql)
    expected = [
        ('id', 'INT'),
        ('name', 'VARCHAR')
    ]
    assert result == expected, result

def test_parse_schema_invalid_2():
    schema_sql = """
    create table catalog_page
    (
    cp_catalog_page_sk        integer               not null,
    cp_catalog_page_id        char(16)              not null,
    cp_start_date_sk          integer                       ,
    cp_end_date_sk            integer                       ,
    cp_department             varchar(50)                   , 
    cp_current_price          decimal(7,2)
    );
    """
    result = parse_schema(schema_sql)
    expected = [
        ('cp_catalog_page_sk', 'INTEGER'),
        ('cp_catalog_page_id', 'CHAR(16)'),
        ('cp_start_date_sk', 'INTEGER'),
        ('cp_end_date_sk', 'INTEGER'),
        ('cp_department', 'VARCHAR(50)'),
        ('cp_current_price', 'DECIMAL(7,2)'),
    ]
    assert result == expected, result

def test_generate_value_int():
    result = generate_value('INT')
    try:
        result_int = int(result)
    except ValueError:
        assert False
    
    assert INT32_MIN <= result_int <= INT32_MAX

def test_generate_value_boolean():
    result = generate_value('BOOLEAN')
    assert result in ['True', 'False']

def test_generate_value_date():
    result = generate_value('DATE')
    assert re.match(r"\d{4}-\d{2}-\d{2}", result)

def test_generate_value_string():
    col_type = 'CHAR'
    result = generate_value(col_type)
    assert isinstance(result, str)
    assert ' ' not in result

def test_generate_value_string_args():
    col_type = 'VARCHAR(10)'
    result = generate_value(col_type)
    assert isinstance(result, str)
    assert ' ' not in result
    assert len(result) <= 10

def test_generate_value_time():
    col_type = 'TIME'
    result = generate_value(col_type)
    assert re.match(r"\d{2}:\d{2}:\d{2}", result)

def test_generate_value_timestamp():
    col_type = 'TIMESTAMP'
    result = generate_value(col_type)
    assert re.match(r"\d{2}:\d{2}:\d{2}", result)

def test_generate_value_float():
    col_type = 'DOUBLE'
    result = generate_value(col_type)
    assert isinstance(result, str)
    assert re.match(r"^-?\d+\.\d{2}$", result), result

def test_generate_value_decimal():
    col_type = 'DECIMAL'
    result = generate_value(col_type)
    assert isinstance(result, str)
    assert re.match(r"^-?\d+\.\d{2}$", result), result

def test_generate_value_decimal_args():
    col_type = 'DECIMAL(5,3)'
    result = generate_value(col_type)
    assert isinstance(result, str)
    assert -100000 < float(result) < 100000
    assert re.match(r"^-?\d+\.\d{3}$", result), result

def test_generate_value_decimal_args():
    col_type = 'DECIMAL(2,1)'
    result = generate_value(col_type)
    assert isinstance(result, str)
    assert -100 < float(result) < 100
    assert re.match(r"^-?\d+\.\d{1}$", result), result

def test_generate_dat_file_creates_correct_number_of_rows():
    schema_sql = """CREATE TABLE test_table (
                        id INT, 
                        name CHAR(50)
                    );
                """
    num_rows = 5
    filename = "test_file.dat"

    with patch('generate_data.generate_value', return_value="mocked_value"):
        with patch('builtins.open', mock_open()) as mock_file:
            generate_dat_file(schema_sql, num_rows, filename)
            
            mock_file.assert_called_with(filename, "w", encoding="utf-8")
            handle = mock_file()
            assert handle.write.call_count == num_rows

def test_generate_dat_file_content():
    schema_sql = """CREATE TABLE test_table (
                        id INT, 
                        name CHAR(50)
                    );
                """
    num_rows = 3
    filename = "test_file.dat"

    mock_values = ["123", "mock_name", "456", "mock_name2", "789", "mock_name3"]
    with patch('generate_data.generate_value', side_effect=mock_values):
        with patch('builtins.open', mock_open()) as mock_file:
            generate_dat_file(schema_sql, num_rows, filename)

            handle = mock_file()
            written_content = handle.write.call_args_list
            assert len(written_content) == num_rows

            for i in range(num_rows):
                assert written_content[i][0][0] == DELIMITER.join(mock_values[i*2:(i+1)*2]) + DELIMITER + "\n"

@patch("builtins.open", mock_open(read_data="CREATE TABLE test_table (id INT, name CHAR(50));"))
@patch("generate_data.generate_dat_file")
def test_generate_data_valid_schema(mock_generate_dat_file):
    schema_path = "schema.sql"
    output_path = "output"
    num_rows = 5

    generate_data(schema_path, output_path, num_rows)

    mock_generate_dat_file.assert_called_once_with(
        "CREATE TABLE test_table (id INT, name CHAR(50));\n", 
        num_rows, 
        os.path.join(output_path, "test_table.dat")
    )

@patch("builtins.open", mock_open(read_data="""CREATE TABLE test_table1 (id INT); 
                                                CREATE TABLE test_table2 (name CHAR(50));"""))
@patch("generate_data.generate_dat_file")
def test_generate_data_multiple_tables(mock_generate_dat_file):
    schema_path = "schema.sql"
    output_path = "output"
    num_rows = 3

    generate_data(schema_path, output_path, num_rows)

    mock_generate_dat_file.assert_any_call(
        "CREATE TABLE test_table1 (id INT);\n", 
        num_rows, 
        os.path.join(output_path, "test_table1.dat")
    )
    mock_generate_dat_file.assert_any_call(
        "CREATE TABLE test_table2 (name CHAR(50));\n", 
        num_rows, 
        os.path.join(output_path, "test_table2.dat")
    )

@patch("builtins.open", mock_open(read_data="CREATE TABLE  (id INT);"))
def test_generate_data_invalid_schema():
    schema_path = "invalid_schema.sql"
    output_path = "output"
    num_rows = 5

    with pytest.raises(ValueError, match="Table name not found in the schema."):
        generate_data(schema_path, output_path, num_rows)

@patch("builtins.open", mock_open(read_data="CREATE TABLE test_table (id INT); ; CREATE TABLE another_table (name CHAR(50));"))
@patch("generate_data.generate_dat_file")
def test_generate_data_multiple_empty_statements(mock_generate_dat_file):
    schema_path = "schema_with_empty.sql"
    output_path = "output"
    num_rows = 5

    generate_data(schema_path, output_path, num_rows)

    mock_generate_dat_file.assert_any_call(
        "CREATE TABLE test_table (id INT);\n", 
        num_rows, 
        os.path.join(output_path, "test_table.dat")
    )
    mock_generate_dat_file.assert_any_call(
        "CREATE TABLE another_table (name CHAR(50));\n", 
        num_rows, 
        os.path.join(output_path, "another_table.dat")
    )
