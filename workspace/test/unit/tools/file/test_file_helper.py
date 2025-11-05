import os
import pytest
from workspace.tools.file.file_helper import list_files_by_ext, file_exists, list_all_files
from workspace.config.error_code import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.tool, pytest.mark.file]


# ------------------------------------------------------------
# 🧩 list_files_by_ext 測試
# ------------------------------------------------------------
def test_list_files_invalid_path():
    files, code = list_files_by_ext(None)
    assert files == []
    assert code == ResultCode.tools_file_invalid_path

    files, code = list_files_by_ext(12345)
    assert files == []
    assert code == ResultCode.tools_file_invalid_path


def test_list_files_dir_not_found(tmp_path):
    fake_dir = tmp_path / "not_exist"
    files, code = list_files_by_ext(str(fake_dir))
    assert code == ResultCode.tools_file_dir_not_found


def test_list_files_empty_dir(tmp_path):
    files, code = list_files_by_ext(str(tmp_path))
    assert files == []
    assert code == ResultCode.tools_file_no_files_found


def test_list_files_permission_denied(monkeypatch, tmp_path):
    def mock_listdir(_):
        raise PermissionError("mock permission denied")
    monkeypatch.setattr(os, "listdir", mock_listdir)
    files, code = list_files_by_ext(str(tmp_path))
    assert files == []
    assert code == ResultCode.tools_file_permission_denied


def test_list_files_list_failed(monkeypatch, tmp_path):
    def mock_listdir(_):
        raise RuntimeError("mock generic error")
    monkeypatch.setattr(os, "listdir", mock_listdir)
    files, code = list_files_by_ext(str(tmp_path))
    assert files == []
    assert code == ResultCode.tools_file_list_failed


def test_list_files_success(tmp_path):
    (tmp_path / "data.csv").write_text("A,B\n1,2", encoding="utf-8")
    (tmp_path / "config.json").write_text("{}", encoding="utf-8")
    files, code = list_files_by_ext(str(tmp_path))
    assert code == ResultCode.SUCCESS
    assert len(files) == 2


# ------------------------------------------------------------
# 🧩 file_exists 測試
# ------------------------------------------------------------
def test_file_exists_invalid_path():
    ok, code = file_exists(None)
    assert not ok
    assert code == ResultCode.tools_file_invalid_path

    ok, code = file_exists(123)
    assert not ok
    assert code == ResultCode.tools_file_invalid_path


def test_file_exists_normal(tmp_path):
    test_file = tmp_path / "a.txt"
    test_file.write_text("hello", encoding="utf-8")
    ok, code = file_exists(str(test_file))
    assert ok is True
    assert code == ResultCode.SUCCESS

    ok, code = file_exists(str(tmp_path / "missing.txt"))
    assert ok is False
    assert code == ResultCode.SUCCESS


def test_file_exists_unknown_error(monkeypatch, tmp_path):
    def mock_exists(_):
        raise RuntimeError("mock")
    monkeypatch.setattr(os.path, "exists", mock_exists)
    ok, code = file_exists(str(tmp_path))
    assert ok is False
    assert code == ResultCode.tools_file_unknown_error


# ------------------------------------------------------------
# 🧩 list_all_files 測試
# ------------------------------------------------------------
def test_list_all_files_invalid_path():
    files, code = list_all_files(None)
    assert files == []
    assert code == ResultCode.tools_file_invalid_path


def test_list_all_files_dir_not_found(tmp_path):
    fake_dir = tmp_path / "nope"
    files, code = list_all_files(str(fake_dir))
    assert files == []
    assert code == ResultCode.tools_file_dir_not_found


def test_list_all_files_empty_dir(tmp_path):
    files, code = list_all_files(str(tmp_path))
    assert files == []
    assert code == ResultCode.tools_file_no_files_found


def test_list_all_files_permission_denied(monkeypatch, tmp_path):
    def mock_listdir(_):
        raise PermissionError("mock")
    monkeypatch.setattr(os, "listdir", mock_listdir)
    files, code = list_all_files(str(tmp_path))
    assert files == []
    assert code == ResultCode.tools_file_permission_denied


def test_list_all_files_list_failed(monkeypatch, tmp_path):
    def mock_listdir(_):
        raise RuntimeError("mock generic error")
    monkeypatch.setattr(os, "listdir", mock_listdir)
    files, code = list_all_files(str(tmp_path))
    assert files == []
    assert code == ResultCode.tools_file_list_failed


def test_list_all_files_success(tmp_path):
    (tmp_path / "a.txt").write_text("hi", encoding="utf-8")
    (tmp_path / "b.csv").write_text("ok", encoding="utf-8")
    files, code = list_all_files(str(tmp_path))
    assert code == ResultCode.SUCCESS
    assert len(files) == 2
