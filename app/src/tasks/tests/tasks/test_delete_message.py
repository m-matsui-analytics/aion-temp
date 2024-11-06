from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tasks.tasks.delete_message import (
    DeleteMessage,
)

TEST_DATA_DIR = Path("src/tasks/tests/data/")

@pytest.mark.django_db
def test_delete_message():
    """Test delete message."""
    delete_message = DeleteMessage()
    delete_message.run()

# @pytest.fixture
# def content_analysis_result_registerer():
#     """Fixture for ContentAnalysisResultRegisterer."""
#     return DeleteMessage()

# @pytest.mark.django_db
# @patch("tasks.tasks.content_anaysis_result_registerer.boto3.client")
# def test_run_valid_message(mock_boto_client, content_analysis_result_registerer):
#     """Test valid message processing."""
#     mock_sqs = MagicMock()
#     mock_boto_client.return_value = mock_sqs

#     with Path.open(f"{TEST_DATA_DIR}/content_analysis_result/success.json") as f:
#         message_body = f.read()

#     # メッセージを受信するようにモックを設定
#     mock_sqs.receive_message.return_value = {
#         'Messages': [{
#             'Body': message_body,
#             'ReceiptHandle': 'abc123'
#         }]
#     }

#     with patch.object(content_analysis_result_registerer, 'error_log_handler') as mock_error_log:
#     #         patch('tasks.jobs.candidate_profile_updater.CandidateProfileUpdater.update') as mock_update:

#         content_analysis_result_registerer.run()

#         # 正しいメッセージが受信されていることを確認
#         mock_sqs.receive_message.assert_called_once()
#         # CandidateProfileUpdaterのupdateが呼ばれていることを確認
#         # エラーログが呼ばれていないことを確認
#         mock_error_log.assert_not_called()

