# workspace/test/unit/tools/test_loader.py
import os
import json
import pytest
import pandas as pd
from workspace.tools.loader.loader import (
    load_system_env,
    load_profile_env,
    load_profile_file,
    load_to_env,
    get_env,
    get_all_env,
)
from workspace.config.error_code import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.tool, pytest.mark.loader]


# ------------------------------------------------------------
# 🧩 檔案不存在
# ------------------------------------------------------------
def test_file_not_found(tmp_path):
    fake_path = tmp_path / "not_exist.env"
    data, code = load_system_env(str(fake_path))
    assert code == ResultCode.tools_loader_file_not_found


# ------------------------------------------------------------
# 🧩 不支援格式 (.txt)
# ------------------------------------------------------------
def test_unsupported_format(tmp_path):
    txt_file = tmp_path / "names.txt"
    txt_file.write_text("這是一個不支援的格式", encoding="utf-8")
    data, code = load_profile_file(str(txt_file))
    assert code == ResultCode.tools_loader_unsupported_format


# ------------------------------------------------------------
# 🧩 JSON 格式錯誤
# ------------------------------------------------------------
def test_json_format_error(tmp_path):
    json_file = tmp_path / "broken.json"
    json_file.write_text("{invalid_json:true", encoding="utf-8")
    data, code = load_profile_file(str(json_file))
    assert code == ResultCode.tools_loader_read_failed


# ------------------------------------------------------------
# 🧩 ENV 正常讀取（System）
# ------------------------------------------------------------
def test_env_system_success(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("A=1\nB=2\n", encoding="utf-8")
    data, code = load_system_env(str(env_file))
    assert code == ResultCode.SUCCESS
    assert "records" in data and isinstance(data["records"], list)
    assert data["records"][0]["A"] == "1"
    assert data["meta"]["source_type"] == ".env"


# ------------------------------------------------------------
# 🧩 ENV 正常讀取（Profiles）
# ------------------------------------------------------------
def test_env_profile_success(tmp_path):
    env_file = tmp_path / "names.env"
    env_file.write_text(
        "a_name=小明\na_password=Pass@123\na_email=xm@example.com\na_modetype=1\n"
        "b_name=小華\nb_password=Abc@456\nb_email=xh@example.com\nb_modetype=2\n",
        encoding="utf-8",
    )
    data, code = load_profile_env(str(env_file), required_fields={"name", "password", "email", "modetype"})
    assert code == ResultCode.SUCCESS
    assert "records" in data
    assert isinstance(data["records"], list)
    assert len(data["records"]) == 2
    assert {"name", "password", "email", "modetype"} <= set(data["records"][0].keys())


# ------------------------------------------------------------
# 🧩 CSV 正常讀取
# ------------------------------------------------------------
def test_csv_success(tmp_path):
    csv_file = tmp_path / "names.csv"
    csv_file.write_text("name,password,email,modetype\n小明,Pass@123,xm@example.com,1\n小華,Abc@456,xh@example.com,2\n", encoding="utf-8")
    data, code = load_profile_file(str(csv_file))
    assert code == ResultCode.SUCCESS
    assert isinstance(data["records"], list)
    assert len(data["records"]) == 2
    assert data["records"][0]["name"] == "小明"


# ------------------------------------------------------------
# 🧩 JSON 正常讀取
# ------------------------------------------------------------
def test_json_success(tmp_path):
    json_file = tmp_path / "names.json"
    content = [
        {"name": "小明", "password": "Pass@123", "email": "xm@example.com", "modetype": 1},
        {"name": "小華", "password": "Abc@456", "email": "xh@example.com", "modetype": 2},
    ]
    json_file.write_text(json.dumps(content, ensure_ascii=False), encoding="utf-8")
    data, code = load_profile_file(str(json_file))
    assert code == ResultCode.SUCCESS
    assert isinstance(data["records"], list)
    assert data["records"][1]["name"] == "小華"


# ------------------------------------------------------------
# 🧩 權限被拒（模擬 PermissionError）
# ------------------------------------------------------------
def test_permission_denied(monkeypatch, tmp_path):
    json_file = tmp_path / "test.json"
    json_file.write_text("{}", encoding="utf-8")

    def mock_open(*args, **kwargs):
        raise PermissionError("mock permission denied")

    monkeypatch.setattr("builtins.open", mock_open)
    data, code = load_profile_file(str(json_file))
    assert code == ResultCode.tools_loader_permission_denied


# ------------------------------------------------------------
# 🧩 測試 load_to_env / get_env / get_all_env
# ------------------------------------------------------------
def test_load_to_env_and_getters(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("HELLO=WORLD\n", encoding="utf-8")
    code = load_to_env(str(env_file))
    assert code == ResultCode.SUCCESS
    assert get_env("HELLO") == "WORLD"
    all_env, code2 = get_all_env()
    assert code2 == ResultCode.SUCCESS
    assert "HELLO" in all_env
