""" Test the service_framework.utils file """

from service_framework.utils import utils

MODULE_TO_IMPORT_PATH = './tests/unit_tests/data/utils_unit_test/module_to_import.py'
JSON_FILE_TO_LOAD = './tests/unit_tests/data/utils_unit_test/file_to_load.json'


def test_utils__snake_case_to_capital_case__valid_case():
    """
    Make sure a regular snake case string will be converted to capital case.
    """
    snake_case = 'this_is_a_snake_case_string'
    hopefully_capital_case = utils.snake_case_to_capital_case(snake_case)
    assert hopefully_capital_case == 'ThisIsASnakeCaseString'


def test_utils__snake_case_to_capital_case__blank_string():
    """
    Make sure the function doesn't break with no input.
    """
    assert utils.snake_case_to_capital_case('') == ''


def test_utils__convert_path_to_import__leading_current_document_case():
    """
    Test if the leading current document './' will be removed from path.
    """
    path = './dir_name/another_name/filename.py'
    import_path = utils.convert_path_to_import(path)
    assert import_path == 'dir_name.another_name.filename'


def test_utils__convert_path_to_import__previous_document_case():
    """
    Test if using previous document '../' in the path will function correctly.
    """
    path = './dir_name/../another_name/filename.py'
    import_path = utils.convert_path_to_import(path)
    assert import_path == 'dir_name..another_name.filename'


def test_utils__convert_path_to_import__leading_previous_document_case():
    """
    Test if using previous document '../' at path start will function correctly.
    """
    path = '../dir_name/another_name/filename.py'
    import_path = utils.convert_path_to_import(path)
    assert import_path == '..dir_name.another_name.filename'


def test_utils__import_python_file_from_cwd__valid_case():
    """
    Determine if a python file can be properly imported from the current
    working directory.
    """
    imported_module = utils.import_python_file_from_cwd(MODULE_TO_IMPORT_PATH)
    imported_module.print_succeeded()


def test_utils__import_python_file_from_module__valid_case():
    """
    Determine if a python file can be properly imported from within the
    service framework module.
    """
    module_path = 'service_framework.connections.in.replyer'
    _ = utils.import_python_file_from_module(module_path)


def test_utils__get_json_from_rel_path__no_rel_path_case():
    """
    Make sure that the file won't break if you don't provide a rel path.
    """
    response = utils.get_json_from_rel_path(None)
    assert response == {}


def test_utils__get_json_from_rel_path__properly_import_json_file_case():
    """
    Make sure the function can actually do its job.
    """
    loaded_file = utils.get_json_from_rel_path(JSON_FILE_TO_LOAD)
    assert loaded_file['SEE_IT_WORKS'] == 'SUCCESS'
