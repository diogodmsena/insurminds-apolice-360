import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from backend.app.models.policy_schema import DnoPolicyData
from backend.app.models.comparison_schema import ComparisonResult
from backend.app.config import DB_PATH
import logging

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS policies (
                id TEXT PRIMARY KEY,
                policy_number TEXT,
                insurer_name TEXT,
                policyholder TEXT,
                lmg_amount REAL,
                lmg_currency TEXT,
                start_date TEXT,
                end_date TEXT,
                validation_status TEXT,
                confidence_score REAL,
                data_json TEXT,
                created_at TEXT
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS comparisons (
                id TEXT PRIMARY KEY,
                policy_ids TEXT,
                summary TEXT,
                data_json TEXT,
                created_at TEXT
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                policy_ids TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()

    def save_policy(self, policy: DnoPolicyData) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO policies (
                id, policy_number, insurer_name, policyholder,
                lmg_amount, lmg_currency, start_date, end_date,
                validation_status, confidence_score, data_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                policy.id,
                policy.policy_number,
                policy.insurer_name,
                policy.policyholder,
                policy.lmg_amount,
                policy.lmg_currency,
                policy.start_date,
                policy.end_date,
                policy.validation_status,
                policy.extraction_confidence_score,
                policy.model_dump_json(),
                policy.created_at
            ))
            conn.commit()
            logger.info(f"Apólice salva no banco: {policy.id} ({policy.policy_number})")

    def get_policy(self, policy_id: str) -> Optional[DnoPolicyData]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data_json FROM policies WHERE id = ?", (policy_id,))
            row = cursor.fetchone()
            if row:
                return DnoPolicyData.model_validate_json(row["data_json"])
            return None

    def list_policies(self) -> List[DnoPolicyData]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data_json FROM policies ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [DnoPolicyData.model_validate_json(r["data_json"]) for r in rows]

    def delete_policy(self, policy_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM policies WHERE id = ?", (policy_id,))
            conn.commit()
            return cursor.rowcount > 0

    def save_comparison(self, comparison: ComparisonResult) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO comparisons (id, policy_ids, summary, data_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """, (
                comparison.id,
                json.dumps(comparison.policy_ids),
                comparison.executive_verdict,
                comparison.model_dump_json(),
                comparison.created_at
            ))
            conn.commit()

    def get_comparison(self, comparison_id: str) -> Optional[ComparisonResult]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data_json FROM comparisons WHERE id = ?", (comparison_id,))
            row = cursor.fetchone()
            if row:
                return ComparisonResult.model_validate_json(row["data_json"])
            return None

    def list_comparisons(self) -> List[ComparisonResult]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data_json FROM comparisons ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [ComparisonResult.model_validate_json(r["data_json"]) for r in rows]

    def save_chat_message(self, session_id: str, role: str, content: str, policy_ids: List[str]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO chat_messages (session_id, role, content, policy_ids)
            VALUES (?, ?, ?, ?)
            """, (session_id, role, content, json.dumps(policy_ids)))
            conn.commit()

    def get_chat_history(self, session_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role, content, timestamp FROM chat_messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
            rows = cursor.fetchall()
            return [{"role": r["role"], "content": r["content"], "timestamp": r["timestamp"]} for r in rows]
