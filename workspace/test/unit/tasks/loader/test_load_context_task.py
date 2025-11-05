# workspace/test/unit/tasks/test_load_context_task.py
import os
import pytest
from workspace.tasks.loader.load_system_context_task import load_system_context
from workspace.tasks.loader.load_profile_context_task import load_profile_context
from workspace.tasks.loader.assemble_context_task import assemble_context
from workspace.config import paths
from workspace.config.error_code import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.task, pytest.mark.loader]


# ------------------------------------------------------------
# fixture：建立暫存 profiles 資料夾與 .env
# ------------------------------------------------------------
@pytest.fixture
def temp_profiles_dir(tmp_path, monkeypatch):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    monkeypatch.setattr(paths, "PROFILE_FILE_PATH", str(profiles_dir / "names"))
    return profiles_dir


@pytest.fixture
def valid_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "DEBUG=true\nTRANSFER_CHAIN=TRON\nBACKEND_RA_BASE_URL=https://ra\n"
        "BACKEND_DR_BASE_URL=https://dr\nOPS_USERNAME=admin\nOPS_PASSWORD=123456\nOPS_OTP_SECRET=XYZKEY\n",
        encoding="utf-8"
    )
    monkeypatch.setattr(paths, "ENV_FILE", str(env_file))
    return env_file


# ------------------------------------------------------------
# 🧩 系統設定缺少欄位
# ------------------------------------------------------------
def test_env_missing_required_key(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("DEBUG=true\nOPS_USERNAME=admin\n", encoding="utf-8")
    monkeypatch.setattr(paths, "ENV_FILE", str(env_file))
    ctx, code = load_system_context()
    assert code == ResultCode.task_env_missing_key


# ------------------------------------------------------------
# 🧩 Profiles 錯誤情境覆蓋
# ------------------------------------------------------------
def test_no_profile_file(temp_profiles_dir, valid_env_file):
    ctx, code = load_profile_context()
    assert code == ResultCode.task_name_file_missing


def test_multiple_profile_files(temp_profiles_dir, valid_env_file):
    (temp_profiles_dir / "names.env").write_text("a_name=小明\na_password=123\na_email=xm@example.com\na_modetype=1\n", encoding="utf-8")
    (temp_profiles_dir / "names.csv").write_text("name,password,email,modetype\n小華,456,xh@example.com,2\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_name_multiple_files_detected


def test_name_empty(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n,Pass@123,xm@example.com,1\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_name_empty_value


def test_name_invalid_char(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明@,Pass@123,xm@example.com,1\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_name_invalid_key_format


def test_name_length_short(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\nA,Pass@123,xm@example.com,1\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_name_invalid_key_length


def test_name_length_long(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    long_name = "超過二十字測試超過二十字測試超過二十字測試"
    csv_path.write_text(f"name,password,email,modetype\n{long_name},Pass@123,xm@example.com,1\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_name_invalid_key_length


def test_password_missing(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明,,xm@example.com,1\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_password_missing


def test_password_length_invalid(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明,123,xm@example.com,1\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_password_invalid_length


def test_password_charset_invalid(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明,abc 中文,xm@example.com,1\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_password_invalid_charset



def test_email_missing(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明,Pass@123,,1\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_email_missing


def test_email_invalid_format(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明,Pass@123,not-an-email,1\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_email_invalid_format


def test_modetype_missing(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明,Pass@123,xm@example.com,\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_mode_type_missing


def test_modetype_not_digit(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明,Pass@123,xm@example.com,ABC\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_mode_type_invalid_format


def test_modetype_invalid_value(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明,Pass@123,xm@example.com,3\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.task_mode_type_invalid_value


# ------------------------------------------------------------
# 🧩 成功情境 & 組合驗證
# ------------------------------------------------------------
def test_profile_csv_success(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明,Pass@123,xm@example.com,1\n小華,Abc@456,xh@example.com,2\n", encoding="utf-8")
    ctx, code = load_profile_context()
    assert code == ResultCode.SUCCESS
    assert "小明" in ctx


def test_full_assemble_success(temp_profiles_dir, valid_env_file):
    csv_path = temp_profiles_dir / "names.csv"
    csv_path.write_text("name,password,email,modetype\n小明,Pass@123,xm@example.com,1\n小華,Abc@456,xh@example.com,2\n", encoding="utf-8")

    common_ctx, code1 = load_system_context()
    assert code1 == ResultCode.SUCCESS
    index_ctx, code2 = load_profile_context()
    assert code2 == ResultCode.SUCCESS
    full_ctx, code3 = assemble_context(common_ctx, index_ctx)
    assert code3 == ResultCode.SUCCESS
    assert "COMMON" in full_ctx
    assert "INDEX" in full_ctx
    assert "API" in full_ctx
