import json
from unittest.mock import MagicMock, patch

import pytest

from tasks.tasks.mail_gen_data_registerer import MailGenDataRegisterer


@pytest.fixture
def mail_gen_data_registerer():
    """Fixture for MailGenDataRegisterer."""
    return MailGenDataRegisterer()

@patch('tasks.tasks.mail_gen_data_registerer.boto3.client')
def test_run_valid_message(mock_boto_client, mail_gen_data_registerer):
    """Test valid message processing."""
    mock_sqs = MagicMock()
    mock_boto_client.return_value = mock_sqs

    # メッセージを受信するようにモックを設定
    mock_sqs.receive_message.return_value = {
        'Messages': [{
            'Body': json.dumps({
                'mail_gen_log_id': 1,
                'job_type': 1,  # JOB_TYPE_CANDIDATE_PROFILE
                'candidate_id': 2,
                'candidate_profile': {'name': 'John Doe'}
            }),
            'ReceiptHandle': 'abc123'
        }]
    }

    with patch.object(mail_gen_data_registerer, 'error_log_handler') as mock_error_log, \
            patch('tasks.jobs.candidate_profile_updater.CandidateProfileUpdater.update') as mock_update:

        mail_gen_data_registerer.run()

        # 正しいメッセージが受信されていることを確認
        mock_sqs.receive_message.assert_called_once()
        # CandidateProfileUpdaterのupdateが呼ばれていることを確認
        mock_update.assert_called_once()
        # エラーログが呼ばれていないことを確認
        mock_error_log.assert_not_called()


@patch('tasks.tasks.mail_gen_data_registerer.boto3.client')
def test_run_invalid_message(mock_boto_client, mail_gen_data_registerer):
    """Test invalid message processing with missing mail_gen_log_id."""
    mock_sqs = MagicMock()
    mock_boto_client.return_value = mock_sqs

    # 不正なメッセージ（mail_gen_log_idがない）を受信するようにモックを設定
    mock_sqs.receive_message.return_value = {
        'Messages': [{
            'Body': json.dumps({
                'job_type': 1,  # JOB_TYPE_CANDIDATE_PROFILE
                'candidate_id': 2,
                'candidate_profile': {'name': 'John Doe'}
            }),
            'ReceiptHandle': 'abc123'
        }]
    }

    with patch.object(mail_gen_data_registerer, 'error_log_handler') as mock_error_log:
        mail_gen_data_registerer.run()

        # 正しいメッセージが受信されていることを確認
        mock_sqs.receive_message.assert_called_once()
        # エラーログが呼ばれていることを確認
        mock_error_log.assert_called_once_with(error_message="no mail_gen_log_id")


@patch('tasks.tasks.mail_gen_data_registerer.boto3.client')
def test_run_invalid_job_type(mock_boto_client, mail_gen_data_registerer):
    """Test invalid job_type processing."""
    mock_sqs = MagicMock()
    mock_boto_client.return_value = mock_sqs

    # 不正なJOB_TYPE（存在しないJOB_TYPE）を受信するようにモックを設定
    mock_sqs.receive_message.return_value = {
        'Messages': [{
            'Body': json.dumps({
                'mail_gen_log_id': 1,
                'job_type': 999,  # 不正なjob_type
                'candidate_id': 2,
                'candidate_profile': {'name': 'John Doe'}
            }),
            'ReceiptHandle': 'abc123'
        }]
    }

    with patch.object(mail_gen_data_registerer, 'error_log_handler') as mock_error_log:
        mail_gen_data_registerer.run()

        # 正しいメッセージが受信されていることを確認
        mock_sqs.receive_message.assert_called_once()
        # エラーログが「invalid job_type」で呼ばれていることを確認
        mock_error_log.assert_called_once_with(error_message="invalid job_type")


@patch('tasks.tasks.mail_gen_data_registerer.boto3.client')
def test_run_no_messages(mock_boto_client, mail_gen_data_registerer):
    """Test processing when no messages are received."""
    mock_sqs = MagicMock()
    mock_boto_client.return_value = mock_sqs

    # メッセージがない場合
    mock_sqs.receive_message.return_value = {
        'Messages': []
    }

    with patch.object(mail_gen_data_registerer, 'error_log_handler') as mock_error_log:
        mail_gen_data_registerer.run()

        # メッセージ受信が呼ばれていることを確認
        mock_sqs.receive_message.assert_called_once()
        # エラーログが呼ばれていないことを確認
        mock_error_log.assert_not_called()


@patch('tasks.tasks.mail_gen_data_registerer.boto3.client')
def test_meil_gen_option_updater(mock_boto_client, mail_gen_data_registerer):
    """Test processing for JOB_TYPE_GEN_MAIL_OPTION."""
    mock_sqs = MagicMock()
    mock_boto_client.return_value = mock_sqs

    # メッセージがない場合
    mock_sqs.receive_message.return_value = {
        'Messages': [{
            'Body': json.dumps({
            "mail_gen_log_id": 2,
            "job_type": 4,
            "empathy_emotion": 1,
            "mail_structure": 1
            }),
            'ReceiptHandle': 'abc123'
        }]
    }
    with patch.object(mail_gen_data_registerer, 'error_log_handler') as mock_error_log, \
            patch('tasks.jobs.gen_mail_option_updater') as mock_update:

        mail_gen_data_registerer.run()

        # 正しいメッセージが受信されていることを確認
        mock_sqs.receive_message.assert_called_once()
        # CandidateProfileUpdaterのupdateが呼ばれていることを確認
        mock_update.assert_called_once()
        # エラーログが呼ばれていないことを確認
        mock_error_log.assert_not_called()
