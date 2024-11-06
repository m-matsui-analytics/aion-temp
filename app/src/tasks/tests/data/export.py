##########################################################
# Test用データをExportするためのモジュール
##########################################################

import json

from pathlib import Path


TEST_DATA_DIR = Path("tasks/tests/data/")

class IdealCandidateMatchData():
    """
    マッチング結果のテストデータ    
    """

    @staticmethod
    def no_error() -> dict:
        """正常系のテストデータ"""
        with Path.open(f"{TEST_DATA_DIR}/ideal_candidate_match/no_error.json") as f:
            return json.load(f)

    @staticmethod
    def ideal_candidate_id_is_not_int() -> dict:
        """ideal_candidate_idがないテストデータ"""
        with Path.open(f"{TEST_DATA_DIR}/ideal_candidate_match/ideal_candidate_id_is_not_int.json") as f:
            return json.load(f)
