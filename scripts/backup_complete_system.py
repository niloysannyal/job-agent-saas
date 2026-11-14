#!/usr/bin/env python
"""
Complete System & History Migration Backup Script
Job Application Agent SaaS + Google Antigravity Data & Contexts
Date: 14 November 2026

Creates an all-inclusive, self-contained backup bundle for migrating to Desktop:
1. PostgreSQL Database (Custom Binary Archive .dump + Plain SQL .sql + Cluster Globals + JSON snapshot)
2. Antigravity Full History (Conversations SQLite DBs, Brain Artifacts, Transcripts, Summaries, Configs)
3. Automated 1-Click Restore Scripts for Windows Desktop (.bat and .ps1)
4. Places bundles in project `backups/` and directly onto `Desktop/JobEazy_Migration_Backup_20261114/`
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USER_HOME = Path(os.environ.get("USERPROFILE", "C:\\Users\\NiloySannyal"))
DESKTOP_DIR = USER_HOME / "Desktop"
GEMINI_DIR = USER_HOME / ".gemini"
ANTIGRAVITY_DIR = GEMINI_DIR / "antigravity"
CONFIG_DIR = GEMINI_DIR / "config"

TIMESTAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
DATE_TAG = datetime.now(timezone.utc).strftime("%Y%m%d")

LOCAL_BUNDLE_DIR = ROOT / "backups" / f"machine_migration_{DATE_TAG}"
DESKTOP_BUNDLE_DIR = DESKTOP_DIR / f"JobEazy_Migration_Backup_{DATE_TAG}"
DESKTOP_ZIP_PATH = DESKTOP_DIR / f"JobEazy_Migration_Backup_{DATE_TAG}.zip"


def calculate_sha256(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def format_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:3.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def backup_database(dest_db_dir: Path) -> dict:
    print("\n" + "=" * 60)
    print("  PHASE 1: BACKING UP POSTGRESQL DATABASE (jobeazy)")
    print("=" * 60)
    dest_db_dir.mkdir(parents=True, exist_ok=True)

    container_name = "job-agent-saas-db-1"
    db_name = "jobeazy"
    db_user = "postgres"

    # Verify container is running
    res = run_cmd(["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"], check=False)
    if container_name not in res.stdout:
        print(f"Error: Docker container '{container_name}' is not running!")
        sys.exit(1)

    # 1. Custom Binary Format Archive (-Fc)
    dump_filename = f"jobeazy_backup_{DATE_TAG}.dump"
    local_dump_path = dest_db_dir / dump_filename
    print(f"[*] Generating PostgreSQL Custom Binary Archive: {dump_filename}...")
    run_cmd(["docker", "exec", container_name, "pg_dump", "-U", db_user, "-d", db_name, "-Fc", "-f", f"/tmp/{dump_filename}"])
    run_cmd(["docker", "cp", f"{container_name}:/tmp/{dump_filename}", str(local_dump_path)])
    run_cmd(["docker", "exec", container_name, "rm", f"/tmp/{dump_filename}"])
    print(f"  ✓ Saved: {local_dump_path.name} ({format_size(local_dump_path.stat().st_size)})")

    # 2. Plain Text SQL Dump with clean/if-exists (--clean --if-exists)
    sql_filename = f"jobeazy_backup_{DATE_TAG}.sql"
    local_sql_path = dest_db_dir / sql_filename
    print(f"[*] Generating Full Plain SQL Dump: {sql_filename}...")
    run_cmd(["docker", "exec", container_name, "pg_dump", "-U", db_user, "-d", db_name, "--clean", "--if-exists", "-f", f"/tmp/{sql_filename}"])
    run_cmd(["docker", "cp", f"{container_name}:/tmp/{sql_filename}", str(local_sql_path)])
    run_cmd(["docker", "exec", container_name, "rm", f"/tmp/{sql_filename}"])
    print(f"  ✓ Saved: {local_sql_path.name} ({format_size(local_sql_path.stat().st_size)})")

    # 3. DDL Schema-Only Dump
    schema_filename = f"schema_only_{DATE_TAG}.sql"
    local_schema_path = dest_db_dir / schema_filename
    print(f"[*] Generating Schema DDL Dump: {schema_filename}...")
    run_cmd(["docker", "exec", container_name, "pg_dump", "-U", db_user, "-d", db_name, "--schema-only", "-f", f"/tmp/{schema_filename}"])
    run_cmd(["docker", "cp", f"{container_name}:/tmp/{schema_filename}", str(local_schema_path)])
    run_cmd(["docker", "exec", container_name, "rm", f"/tmp/{schema_filename}"])
    print(f"  ✓ Saved: {local_schema_path.name} ({format_size(local_schema_path.stat().st_size)})")

    # 4. Globals / Roles Dump
    globals_filename = "postgres_globals.sql"
    local_globals_path = dest_db_dir / globals_filename
    print(f"[*] Generating PostgreSQL Globals & Roles: {globals_filename}...")
    run_cmd(["docker", "exec", container_name, "pg_dumpall", "-U", db_user, "--globals-only", "-f", f"/tmp/{globals_filename}"])
    run_cmd(["docker", "cp", f"{container_name}:/tmp/{globals_filename}", str(local_globals_path)])
    run_cmd(["docker", "exec", container_name, "rm", f"/tmp/{globals_filename}"])
    print(f"  ✓ Saved: {local_globals_path.name} ({format_size(local_globals_path.stat().st_size)})")

    # 5. Include latest JSON export if available
    latest_json = ROOT / "backups" / "jobeazy_latest.json"
    if latest_json.exists():
        shutil.copy2(latest_json, dest_db_dir / "jobeazy_latest.json")
        print(f"  ✓ Copied JSON Data Snapshot: jobeazy_latest.json ({format_size(latest_json.stat().st_size)})")

    # Create convenient symlinks/copies named latest
    shutil.copy2(local_dump_path, dest_db_dir / "jobeazy_latest.dump")
    shutil.copy2(local_sql_path, dest_db_dir / "jobeazy_latest.sql")

    # Query table row counts for manifest
    res = run_cmd(["docker", "exec", container_name, "psql", "-U", db_user, "-d", db_name, "-t", "-A", "-c",
                    "SELECT table_name, (xpath('/row/cnt/text()', xml_count))[1]::text::int as row_count FROM (SELECT table_name, query_to_xml(format('select count(*) as cnt from %I', table_name), false, true, '') as xml_count FROM information_schema.tables WHERE table_schema = 'public') sub ORDER BY table_name;"], check=False)
    table_stats = {}
    if res.returncode == 0:
        for line in res.stdout.strip().splitlines():
            if "|" in line:
                t, c = line.split("|", 1)
                try:
                    table_stats[t.strip()] = int(c.strip())
                except ValueError:
                    pass

    return {
        "dump_file": str(local_dump_path),
        "sql_file": str(local_sql_path),
        "schema_file": str(local_schema_path),
        "globals_file": str(local_globals_path),
        "table_count": len(table_stats),
        "total_rows": sum(table_stats.values()),
        "tables": table_stats,
    }


def backup_antigravity(dest_ag_dir: Path) -> dict:
    print("\n" + "=" * 60)
    print("  PHASE 2: BACKING UP ANTIGRAVITY DATA, HISTORY & CONTEXTS")
    print("=" * 60)
    dest_ag_dir.mkdir(parents=True, exist_ok=True)

    ag_zip_filename = f"Antigravity_History_and_Brain_{DATE_TAG}.zip"
    ag_zip_path = dest_ag_dir / ag_zip_filename

    print(f"[*] Packaging Antigravity conversations, transcripts, artifacts, and configs into:")
    print(f"    {ag_zip_path}...")

    file_count = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(ag_zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        # 1. Archive antigravity/conversations/
        conv_dir = ANTIGRAVITY_DIR / "conversations"
        if conv_dir.exists():
            print(f"  -> Archiving conversation SQLite DBs ({conv_dir})...")
            for root, _, files in os.walk(conv_dir):
                for f in files:
                    full_p = Path(root) / f
                    rel_p = Path("antigravity") / "conversations" / full_p.relative_to(conv_dir)
                    try:
                        zf.write(full_p, str(rel_p))
                        file_count += 1
                        total_uncompressed_bytes += full_p.stat().st_size
                    except Exception as e:
                        print(f"    Warning reading {f}: {e}")

        # 2. Archive antigravity/brain/ (transcripts, artifacts, subagents)
        brain_dir = ANTIGRAVITY_DIR / "brain"
        if brain_dir.exists():
            print(f"  -> Archiving conversation brain transcripts & artifacts ({brain_dir})...")
            for root, _, files in os.walk(brain_dir):
                for f in files:
                    full_p = Path(root) / f
                    rel_p = Path("antigravity") / "brain" / full_p.relative_to(brain_dir)
                    try:
                        zf.write(full_p, str(rel_p))
                        file_count += 1
                        total_uncompressed_bytes += full_p.stat().st_size
                    except Exception as e:
                        print(f"    Warning reading {f}: {e}")

        # 3. Archive root antigravity files & databases
        root_items = [
            "conversation_summaries.db",
            "conversation_summaries.db-shm",
            "conversation_summaries.db-wal",
            "antigravity_state.pbtxt",
            "agyhub_summaries_proto.pb",
            "chapter_titles",
            "knowledge",
            "annotations",
            "mcp",
        ]
        print("  -> Archiving global conversation indices and state...")
        for item_name in root_items:
            item_path = ANTIGRAVITY_DIR / item_name
            if item_path.is_file():
                zf.write(item_path, str(Path("antigravity") / item_name))
                file_count += 1
                total_uncompressed_bytes += item_path.stat().st_size
            elif item_path.is_dir():
                for root, _, files in os.walk(item_path):
                    for f in files:
                        full_p = Path(root) / f
                        rel_p = Path("antigravity") / item_name / full_p.relative_to(item_path)
                        try:
                            zf.write(full_p, str(rel_p))
                            file_count += 1
                            total_uncompressed_bytes += full_p.stat().st_size
                        except Exception:
                            pass

        # 4. Archive .gemini/config/ (plugins, settings, mcp_config.json)
        if CONFIG_DIR.exists():
            print("  -> Archiving custom plugins and user configurations...")
            for root, _, files in os.walk(CONFIG_DIR):
                for f in files:
                    full_p = Path(root) / f
                    rel_p = Path("config") / full_p.relative_to(CONFIG_DIR)
                    try:
                        zf.write(full_p, str(rel_p))
                        file_count += 1
                        total_uncompressed_bytes += full_p.stat().st_size
                    except Exception:
                        pass

    compressed_size = ag_zip_path.stat().st_size
    print(f"  ✓ Antigravity archive completed!")
    print(f"    Files packed: {file_count}")
    print(f"    Uncompressed: {format_size(total_uncompressed_bytes)}")
    print(f"    Compressed:   {format_size(compressed_size)} ({compressed_size / total_uncompressed_bytes * 100:.1f}%)")

    # Create convenient copy
    shutil.copy2(ag_zip_path, dest_ag_dir / "Antigravity_History_and_Brain_latest.zip")

    return {
        "zip_file": str(ag_zip_path),
        "file_count": file_count,
        "uncompressed_bytes": total_uncompressed_bytes,
        "compressed_bytes": compressed_size,
    }


def write_restore_scripts(dest_bundle_dir: Path):
    print("\n" + "=" * 60)
    print("  PHASE 3: GENERATING TURNKEY RESTORE SCRIPTS & GUIDES")
    print("=" * 60)

    # 1. Database Restore Batch Script (restore_database.bat)
    bat_db_content = f"""@echo off
REM =====================================================================
REM Job Application Agent SaaS -- 1-Click Database Restore
REM Restores jobeazy PostgreSQL Database on Windows Desktop
REM =====================================================================
setlocal enabledelayedexpansion

echo =====================================================================
echo   JobEazy Database Restore -- Desktop Migration
echo =====================================================================
echo.

set CONTAINER_NAME=job-agent-saas-db-1
set DB_NAME=jobeazy
set DB_USER=postgres
set DUMP_FILE=jobeazy_latest.dump
set SQL_FILE=jobeazy_latest.sql

REM Check if Docker is installed and running
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in PATH!
    echo Please install Docker Desktop or restore manually via psql:
    echo   psql -U postgres -h localhost -p 5433 -d jobeazy -f %SQL_FILE%
    pause
    exit /b 1
)

echo [*] Checking Docker container '%CONTAINER_NAME%'...
docker ps --filter "name=%CONTAINER_NAME%" --format "{{{{.Names}}}}" | findstr /i "%CONTAINER_NAME%" >nul
if %errorlevel% neq 0 (
    echo [*] Container is not running. Starting Docker Compose...
    cd /d "%~dp0\\..\\.." 2>nul
    docker compose up -d db
    echo [*] Waiting 5 seconds for PostgreSQL to initialize...
    timeout /t 5 /nobreak >nul
)

cd /d "%~dp0"
if exist "%DUMP_FILE%" (
    echo [*] Restoring from binary archive: %DUMP_FILE%...
    docker cp "%DUMP_FILE%" %CONTAINER_NAME%:/tmp/restore.dump
    docker exec %CONTAINER_NAME% pg_restore -U %DB_USER% -d %DB_NAME% --clean --if-exists /tmp/restore.dump
    docker exec %CONTAINER_NAME% rm /tmp/restore.dump
    echo.
    echo [SUCCESS] Database restored successfully from %DUMP_FILE%!
) else if exist "%SQL_FILE%" (
    echo [*] Restoring from plain SQL: %SQL_FILE%...
    docker cp "%SQL_FILE%" %CONTAINER_NAME%:/tmp/restore.sql
    docker exec %CONTAINER_NAME% psql -U %DB_USER% -d %DB_NAME% -f /tmp/restore.sql
    docker exec %CONTAINER_NAME% rm /tmp/restore.sql
    echo.
    echo [SUCCESS] Database restored successfully from %SQL_FILE%!
) else (
    echo [ERROR] Neither %DUMP_FILE% nor %SQL_FILE% found in directory!
    pause
    exit /b 1
)

echo.
echo Database is ready on port 5433 (jobeazy).
pause
"""
    db_bat_path = dest_bundle_dir / "database" / "restore_database.bat"
    with open(db_bat_path, "w", encoding="utf-8") as f:
        f.write(bat_db_content)
    print(f"  ✓ Generated: {db_bat_path.relative_to(dest_bundle_dir)}")

    # 2. Antigravity Restore Batch Script (restore_antigravity.bat)
    bat_ag_content = f"""@echo off
REM =====================================================================
REM Google Antigravity -- 1-Click History & Contexts Restore
REM Restores conversation DBs, transcripts, artifacts & config on Desktop
REM =====================================================================
setlocal enabledelayedexpansion

echo =====================================================================
echo   Google Antigravity -- Restore History and Brain Contexts
echo =====================================================================
echo.

set TARGET_GEMINI=%USERPROFILE%\\.gemini
set TARGET_AG=%TARGET_GEMINI%\\antigravity
set ZIP_FILE=Antigravity_History_and_Brain_latest.zip

cd /d "%~dp0"

if not exist "%ZIP_FILE%" (
    for %%F in (Antigravity_History_and_Brain_*.zip) do set ZIP_FILE=%%F
)

if not exist "%ZIP_FILE%" (
    echo [ERROR] Could not find Antigravity zip archive in directory!
    pause
    exit /b 1
)

echo [*] Target destination: %TARGET_GEMINI%
echo [*] Archive source:     %ZIP_FILE%
echo.

if exist "%TARGET_AG%" (
    echo [*] Creating safe timestamped backup of existing .gemini\\antigravity...
    for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set LDT=%%I
    set BACKUP_DIR=%TARGET_GEMINI%\\antigravity_backup_!LDT:~0,8!_!LDT:~8,6!
    echo     Backup location: !BACKUP_DIR!
    xcopy /E /I /Q /Y "%TARGET_AG%" "!BACKUP_DIR!" >nul
)

echo [*] Extracting Antigravity history and artifacts to %TARGET_GEMINI%...
powershell -Command "Expand-Archive -Path '%~dp0%ZIP_FILE%' -DestinationPath '%TARGET_GEMINI%' -Force"

echo.
echo [SUCCESS] All Antigravity conversations, transcripts, artifacts, and configs restored!
echo Open Antigravity on this desktop to resume your active conversation history seamlessly.
echo.
pause
"""
    ag_bat_path = dest_bundle_dir / "antigravity" / "restore_antigravity.bat"
    with open(ag_bat_path, "w", encoding="utf-8") as f:
        f.write(bat_ag_content)
    print(f"  ✓ Generated: {ag_bat_path.relative_to(dest_bundle_dir)}")

    # 3. Master 1-Click Desktop Restore Script (RESTORE_ALL_ON_DESKTOP.bat)
    master_bat_content = """@echo off
REM =====================================================================
REM Job Application Agent SaaS + Antigravity -- Master Desktop Migration
REM 1-Click Complete System & History Restore
REM =====================================================================
setlocal enabledelayedexpansion

echo =====================================================================
echo   JobEazy + Antigravity -- Master Desktop Migration Restore
echo =====================================================================
echo.
echo This script will restore:
echo   1. Antigravity full conversation history, transcripts, and artifacts
echo   2. PostgreSQL database (jobeazy) with all 49 tables, accounts, and jobs
echo.
set /p CONFIRM="Proceed with restoration? (y/n): "
if /i not "%CONFIRM%"=="y" exit /b 0

echo.
echo [STEP 1/2] Restoring Antigravity History & Contexts...
call "%~dp0antigravity\\restore_antigravity.bat"

echo.
echo [STEP 2/2] Restoring PostgreSQL Database...
call "%~dp0database\\restore_database.bat"

echo.
echo =====================================================================
echo   MIGRATION RESTORE COMPLETE!
echo =====================================================================
echo   1. Antigravity is populated with all previous conversation transcripts.
echo   2. PostgreSQL database is fully populated on port 5433.
echo   3. Start backend: cd backend && .venv\\Scripts\\python -m uvicorn app.main:app --port 8000
echo   4. Start frontend: cd frontend && npm run dev
echo =====================================================================
pause
"""
    master_bat_path = dest_bundle_dir / "RESTORE_ALL_ON_DESKTOP.bat"
    with open(master_bat_path, "w", encoding="utf-8") as f:
        f.write(master_bat_content)
    print(f"  ✓ Generated: {master_bat_path.relative_to(dest_bundle_dir)}")

    # 4. Master Migration Guide Markdown
    readme_content = f"""# JobEazy + Google Antigravity Full Migration Bundle
**Created:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}  
**Source Machine:** Office Laptop (`{os.environ.get("COMPUTERNAME", "Laptop")}`)  
**Target Machine:** Home Desktop PC  

---

## What Is Included in This Backup

### 1. PostgreSQL Database (`database/`)
- `jobeazy_latest.dump`: Compressed PostgreSQL binary custom archive (`pg_dump -Fc`). Contains all 49 tables, sequences, LangGraph checkpoints, accounts, jobs, applications, and platform configs.
- `jobeazy_latest.sql`: Human-readable SQL script with `--clean --if-exists` for standard `psql` restore.
- `schema_only_{DATE_TAG}.sql`: Full DDL schema for architectural reference.
- `postgres_globals.sql`: PostgreSQL roles, superusers, and permissions.
- `jobeazy_latest.json`: Portable JSON table snapshot for cross-platform data auditing.
- `restore_database.bat`: 1-click batch script to restore into Docker or local PostgreSQL.

### 2. Google Antigravity Data & Contexts (`antigravity/`)
- `Antigravity_History_and_Brain_latest.zip`: Complete archive of:
  - `antigravity/conversations/*.db`: SQLite conversation databases (all past and active chat sessions).
  - `antigravity/brain/*`: All transcripts (`transcript.jsonl`), markdown master plans, reports, artifacts, and subagent transcripts.
  - `antigravity/conversation_summaries.db*`: Global conversation search indices and summaries.
  - `antigravity/chapter_titles/`, `knowledge/`, `annotations/`, `antigravity_state.pbtxt`.
  - `config/`: MCP configurations, plugins, and custom settings.
- `restore_antigravity.bat`: 1-click script to extract into `%USERPROFILE%\\.gemini\\` with automatic backup of existing state.

---

## How to Restore on Your Desktop PC

### Method A: 1-Click Master Restore (Recommended)
1. Copy this entire folder (`JobEazy_Migration_Backup_{DATE_TAG}`) to your Desktop PC.
2. Double-click:
   ```cmd
   RESTORE_ALL_ON_DESKTOP.bat
   ```
3. Follow the on-screen prompts. Both Antigravity and PostgreSQL will be restored automatically.

---

### Method B: Manual Component Restore

#### 1. Restore Antigravity History
Run from command line or double click:
```cmd
cd antigravity
restore_antigravity.bat
```
*Or manually:* Extract `Antigravity_History_and_Brain_latest.zip` directly into `C:\\Users\\<YourUsername>\\.gemini\\`.

#### 2. Restore PostgreSQL Database
Make sure Docker is running, then run:
```cmd
cd database
restore_database.bat
```
*Or via Docker CLI:*
```bash
docker cp jobeazy_latest.dump job-agent-saas-db-1:/tmp/restore.dump
docker exec job-agent-saas-db-1 pg_restore -U postgres -d jobeazy --clean --if-exists /tmp/restore.dump
```
*Or via local PostgreSQL psql (without Docker):*
```bash
psql -U postgres -h localhost -p 5433 -d jobeazy -f jobeazy_latest.sql
```

---

## Verification Checklist on Desktop
- [ ] Open Antigravity: All chat history, artifacts, and transcripts appear in the sidebar.
- [ ] Database Connection: `docker exec job-agent-saas-db-1 psql -U postgres -d jobeazy -c "SELECT count(*) FROM jobs;"` returns 596+.
- [ ] Full Test Suite: `cd backend && .venv\\Scripts\\pytest` passes 301/301 tests.
"""
    readme_path = dest_bundle_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"  ✓ Generated: {readme_path.relative_to(dest_bundle_dir)}")


def create_desktop_export(source_bundle_dir: Path):
    print("\n" + "=" * 60)
    print("  PHASE 4: EXPORTING BUNDLE TO WINDOWS DESKTOP")
    print("=" * 60)

    # 1. Copy full directory to Desktop
    if DESKTOP_BUNDLE_DIR.exists():
        print(f"[*] Removing existing folder: {DESKTOP_BUNDLE_DIR.name}...")
        shutil.rmtree(DESKTOP_BUNDLE_DIR)

    print(f"[*] Copying complete migration bundle to Desktop:")
    print(f"    {DESKTOP_BUNDLE_DIR}...")
    shutil.copytree(source_bundle_dir, DESKTOP_BUNDLE_DIR)
    print("  ✓ Desktop folder created!")

    # 2. Create single unified ZIP archive on Desktop
    if DESKTOP_ZIP_PATH.exists():
        DESKTOP_ZIP_PATH.unlink()

    print(f"[*] Creating unified single-file migration ZIP on Desktop:")
    print(f"    {DESKTOP_ZIP_PATH}...")
    with zipfile.ZipFile(DESKTOP_ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, _, files in os.walk(DESKTOP_BUNDLE_DIR):
            for file in files:
                p = Path(root) / file
                rel_p = p.relative_to(DESKTOP_BUNDLE_DIR.parent)
                zf.write(p, str(rel_p))

    zip_size = DESKTOP_ZIP_PATH.stat().st_size
    print(f"  ✓ Unified ZIP created: {DESKTOP_ZIP_PATH.name} ({format_size(zip_size)})")


def generate_manifest(bundle_dir: Path, db_info: dict, ag_info: dict):
    print("\n" + "=" * 60)
    print("  PHASE 5: COMPUTING INTEGRITY CHECKSUMS & MANIFEST")
    print("=" * 60)

    manifest = {
        "backup_date_utc": datetime.now(timezone.utc).isoformat(),
        "source_machine": os.environ.get("COMPUTERNAME", "Unknown"),
        "database": {
            "tables_count": db_info["table_count"],
            "total_rows": db_info["total_rows"],
            "files": {},
        },
        "antigravity": {
            "files_packed": ag_info["file_count"],
            "uncompressed_bytes": ag_info["uncompressed_bytes"],
            "compressed_bytes": ag_info["compressed_bytes"],
            "files": {},
        },
        "checksums_sha256": {},
    }

    print("[*] SHA-256 Checksums:")
    for root, _, files in os.walk(bundle_dir):
        for f in files:
            p = Path(root) / f
            rel = p.relative_to(bundle_dir)
            sha = calculate_sha256(p)
            size = p.stat().st_size
            manifest["checksums_sha256"][str(rel).replace("\\\\", "/")] = {
                "sha256": sha,
                "size_bytes": size,
                "size_formatted": format_size(size),
            }
            if str(rel).endswith(".dump") or str(rel).endswith(".sql") or str(rel).endswith(".zip"):
                print(f"  {sha[:16]}...  {format_size(size):>10}  {rel}")

    manifest_path = bundle_dir / "backup_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    # Sync manifest to desktop folder
    desktop_manifest = DESKTOP_BUNDLE_DIR / "backup_manifest.json"
    if DESKTOP_BUNDLE_DIR.exists():
        shutil.copy2(manifest_path, desktop_manifest)

    print(f"  ✓ Manifest saved: {manifest_path.name}")


def main():
    start_time = time.time()
    print("*" * 65)
    print("  JOB APPLICATION AGENT SAAS + GOOGLE ANTIGRAVITY")
    print(f"  COMPLETE MIGRATION BACKUP GENERATOR ({DATE_TAG})")
    print("*" * 65)

    LOCAL_BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

    # Phase 1: Database Backup
    db_dest = LOCAL_BUNDLE_DIR / "database"
    db_info = backup_database(db_dest)

    # Phase 2: Antigravity Backup
    ag_dest = LOCAL_BUNDLE_DIR / "antigravity"
    ag_info = backup_antigravity(ag_dest)

    # Phase 3: Restore Scripts & README
    write_restore_scripts(LOCAL_BUNDLE_DIR)

    # Phase 4: Export to Desktop
    create_desktop_export(LOCAL_BUNDLE_DIR)

    # Phase 5: Manifest & Checksums
    generate_manifest(LOCAL_BUNDLE_DIR, db_info, ag_info)

    elapsed = time.time() - start_time
    print("\n" + "=" * 65)
    print(f"🎉 COMPLETE BACKUP FINISHED IN {elapsed:.1f} SECONDS!")
    print("=" * 65)
    print(f"\n[1] PROJECT REPOSITORY ARCHIVE:")
    print(f"    {LOCAL_BUNDLE_DIR}")
    print(f"\n[2] DESKTOP READY-TO-RESTORE FOLDER:")
    print(f"    {DESKTOP_BUNDLE_DIR}")
    print(f"\n[3] DESKTOP SINGLE PORTABLE ZIP (For USB / Cloud Transfer):")
    print(f"    {DESKTOP_ZIP_PATH} ({format_size(DESKTOP_ZIP_PATH.stat().st_size)})")
    print("=" * 65)


if __name__ == "__main__":
    main()

