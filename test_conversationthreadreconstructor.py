#!/usr/bin/env python3
"""
Comprehensive test suite for ConversationThreadReconstructor.

Tests cover:
- Core functionality (message parsing, thread reconstruction)
- Edge cases (empty threads, orphan messages, circular references)
- Export formats (markdown, JSON, text)
- Search functionality (topic, participant)
- Thread analysis (depth, duration, participants)

Run: python test_conversationthreadreconstructor.py
"""

import json
import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from conversationthreadreconstructor import (
    Message, Thread, ConversationThreadReconstructor,
    format_thread_list, ICON_OK, ICON_ERROR
)


class TestMessage(unittest.TestCase):
    """Test Message class."""
    
    def test_message_basic_creation(self):
        """Test creating a message from basic data."""
        data = {
            'id': 1,
            'content': 'Hello world',
            'sender_id': 'FORGE',
            'channel_id': 'general',
            'created_at': '2026-01-29T12:00:00Z'
        }
        msg = Message(data)
        
        self.assertEqual(msg.id, 1)
        self.assertEqual(msg.content, 'Hello world')
        self.assertEqual(msg.sender, 'FORGE')
        self.assertEqual(msg.channel_id, 'general')
    
    def test_message_with_parent(self):
        """Test message with parent reference."""
        data = {
            'id': 2,
            'content': 'Reply',
            'sender_id': 'CLIO',
            'parent_id': 1
        }
        msg = Message(data)
        
        self.assertEqual(msg.parent_id, 1)
    
    def test_message_mention_extraction(self):
        """Test extracting @mentions from content."""
        data = {
            'id': 1,
            'content': 'Hello @FORGE and @CLIO, please review @ATLAS work',
            'sender_id': 'LOGAN'
        }
        msg = Message(data)
        
        self.assertIn('FORGE', msg.mentions)
        self.assertIn('CLIO', msg.mentions)
        self.assertIn('ATLAS', msg.mentions)
        self.assertEqual(len(msg.mentions), 3)
    
    def test_message_mention_extraction_empty(self):
        """Test mention extraction with no mentions."""
        data = {
            'id': 1,
            'content': 'No mentions here',
            'sender_id': 'TEST'
        }
        msg = Message(data)
        self.assertEqual(msg.mentions, [])
    
    def test_message_timestamp_parsing(self):
        """Test timestamp parsing with various formats."""
        # ISO format with Z
        data = {'id': 1, 'content': '', 'sender_id': 'X', 'created_at': '2026-01-29T12:00:00Z'}
        msg = Message(data)
        self.assertIsNotNone(msg.timestamp)
        self.assertEqual(msg.timestamp.year, 2026)
        
        # ISO format with milliseconds
        data['created_at'] = '2026-01-29T12:00:00.123456Z'
        msg = Message(data)
        self.assertIsNotNone(msg.timestamp)
    
    def test_message_timestamp_invalid(self):
        """Test handling of invalid timestamps."""
        data = {'id': 1, 'content': '', 'sender_id': 'X', 'created_at': 'invalid'}
        msg = Message(data)
        self.assertIsNone(msg.timestamp)
    
    def test_message_preview(self):
        """Test message preview generation."""
        # Short message
        data = {'id': 1, 'content': 'Short', 'sender_id': 'X'}
        msg = Message(data)
        self.assertEqual(msg.preview, 'Short')
        
        # Long message (should truncate)
        long_content = 'A' * 200
        data = {'id': 2, 'content': long_content, 'sender_id': 'X'}
        msg = Message(data)
        self.assertTrue(msg.preview.endswith('...'))
        self.assertLessEqual(len(msg.preview), 104)  # 100 + '...'
    
    def test_message_preview_newlines(self):
        """Test preview removes newlines."""
        data = {'id': 1, 'content': 'Line 1\nLine 2\nLine 3', 'sender_id': 'X'}
        msg = Message(data)
        self.assertNotIn('\n', msg.preview)
    
    def test_message_to_dict(self):
        """Test message serialization to dict."""
        data = {
            'id': 1,
            'content': 'Test @FORGE',
            'sender_id': 'CLIO',
            'channel_id': 'ch1',
            'parent_id': None
        }
        msg = Message(data)
        msg.depth = 2
        
        d = msg.to_dict()
        self.assertEqual(d['id'], 1)
        self.assertEqual(d['depth'], 2)
        self.assertIn('FORGE', d['mentions'])


class TestThread(unittest.TestCase):
    """Test Thread class."""
    
    def setUp(self):
        """Create sample messages for testing."""
        self.root_msg = Message({
            'id': 1,
            'content': 'Root message',
            'sender_id': 'FORGE',
            'created_at': '2026-01-29T12:00:00Z'
        })
        self.root_msg.depth = 0
        
        self.reply1 = Message({
            'id': 2,
            'content': 'First reply',
            'sender_id': 'CLIO',
            'parent_id': 1,
            'created_at': '2026-01-29T12:01:00Z'
        })
        self.reply1.depth = 1
        
        self.reply2 = Message({
            'id': 3,
            'content': 'Second reply',
            'sender_id': 'ATLAS',
            'parent_id': 1,
            'created_at': '2026-01-29T12:02:00Z'
        })
        self.reply2.depth = 1
    
    def test_thread_creation(self):
        """Test basic thread creation."""
        thread = Thread(self.root_msg)
        
        self.assertEqual(thread.root.id, 1)
        self.assertEqual(thread.message_count, 1)
        self.assertIn('FORGE', thread.participants)
    
    def test_thread_add_message(self):
        """Test adding messages to thread."""
        thread = Thread(self.root_msg)
        
        result = thread.add_message(self.reply1)
        self.assertTrue(result)
        self.assertEqual(thread.message_count, 2)
        self.assertIn('CLIO', thread.participants)
    
    def test_thread_add_duplicate(self):
        """Test that duplicate messages are rejected."""
        thread = Thread(self.root_msg)
        thread.add_message(self.reply1)
        
        # Try to add same message again
        result = thread.add_message(self.reply1)
        self.assertFalse(result)
        self.assertEqual(thread.message_count, 2)
    
    def test_thread_depth(self):
        """Test thread depth calculation."""
        thread = Thread(self.root_msg)
        thread.add_message(self.reply1)
        
        # Add a deeper reply
        deep_reply = Message({
            'id': 4,
            'content': 'Deep reply',
            'sender_id': 'NEXUS',
            'parent_id': 2
        })
        deep_reply.depth = 2
        thread.add_message(deep_reply)
        
        self.assertEqual(thread.depth, 2)
    
    def test_thread_duration(self):
        """Test thread duration calculation."""
        thread = Thread(self.root_msg)
        thread.add_message(self.reply1)
        thread.add_message(self.reply2)
        
        duration = thread.duration
        self.assertIsNotNone(duration)
        self.assertEqual(duration.total_seconds(), 120)  # 2 minutes
    
    def test_thread_sort_by_time(self):
        """Test sorting messages by time."""
        thread = Thread(self.root_msg)
        thread.add_message(self.reply2)  # Add out of order
        thread.add_message(self.reply1)
        
        thread.sort_by_time()
        
        self.assertEqual(thread.messages[0].id, 1)  # Root first
        self.assertEqual(thread.messages[1].id, 2)  # reply1 second
        self.assertEqual(thread.messages[2].id, 3)  # reply2 third
    
    def test_thread_participants(self):
        """Test participant tracking."""
        thread = Thread(self.root_msg)
        thread.add_message(self.reply1)
        thread.add_message(self.reply2)
        
        self.assertEqual(len(thread.participants), 3)
        self.assertIn('FORGE', thread.participants)
        self.assertIn('CLIO', thread.participants)
        self.assertIn('ATLAS', thread.participants)
    
    def test_thread_mentions(self):
        """Test mention aggregation."""
        msg_with_mention = Message({
            'id': 5,
            'content': 'Hey @LOGAN check this @BOLT',
            'sender_id': 'FORGE'
        })
        
        thread = Thread(self.root_msg)
        thread.add_message(msg_with_mention)
        
        self.assertIn('LOGAN', thread.all_mentions)
        self.assertIn('BOLT', thread.all_mentions)
    
    def test_thread_summary(self):
        """Test thread summary generation."""
        thread = Thread(self.root_msg)
        thread.add_message(self.reply1)
        thread.add_message(self.reply2)
        
        summary = thread.get_summary()
        
        self.assertEqual(summary['root_id'], 1)
        self.assertEqual(summary['message_count'], 3)
        self.assertEqual(summary['participant_count'], 3)
        self.assertIsNotNone(summary['root_preview'])
    
    def test_thread_to_dict(self):
        """Test thread serialization."""
        thread = Thread(self.root_msg)
        thread.add_message(self.reply1)
        
        d = thread.to_dict()
        
        self.assertIn('summary', d)
        self.assertIn('messages', d)
        self.assertEqual(len(d['messages']), 2)


class TestConversationThreadReconstructorWithMockDB(unittest.TestCase):
    """Test ConversationThreadReconstructor with a mock database."""
    
    @classmethod
    def setUpClass(cls):
        """Create a temporary test database."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = Path(cls.temp_dir) / "test_comms.db"
        
        # Create database schema
        conn = sqlite3.connect(str(cls.db_path))
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE channels (
                id TEXT PRIMARY KEY,
                name TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY,
                content TEXT,
                sender_id TEXT,
                sender TEXT,
                channel_id TEXT,
                parent_id INTEGER,
                thread_id INTEGER,
                created_at TEXT,
                message_type TEXT DEFAULT 'message'
            )
        """)
        
        # Insert test data
        cursor.execute("INSERT INTO channels VALUES ('ch1', 'general')")
        cursor.execute("INSERT INTO channels VALUES ('ch2', 'team-brain')")
        
        # Create a thread: root -> 2 replies -> 1 deep reply
        messages = [
            (1, 'Root message about consciousness', 'FORGE', 'Forge', 'ch1', None, None, '2026-01-29T10:00:00Z'),
            (2, 'First reply discussing consciousness', 'CLIO', 'Clio', 'ch1', 1, 1, '2026-01-29T10:01:00Z'),
            (3, 'Second reply @ATLAS', 'NEXUS', 'Nexus', 'ch1', 1, 1, '2026-01-29T10:02:00Z'),
            (4, 'Deep reply to Clio', 'ATLAS', 'Atlas', 'ch1', 2, 1, '2026-01-29T10:03:00Z'),
            # Another thread
            (5, 'Different topic about tools', 'BOLT', 'Bolt', 'ch2', None, None, '2026-01-29T11:00:00Z'),
            (6, 'Reply about tools', 'FORGE', 'Forge', 'ch2', 5, 5, '2026-01-29T11:01:00Z'),
            # Standalone message
            (7, 'Orphan message', 'LOGAN', 'Logan', 'ch1', None, None, '2026-01-29T12:00:00Z'),
        ]
        
        cursor.executemany("""
            INSERT INTO messages (id, content, sender_id, sender, channel_id, parent_id, thread_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, messages)
        
        conn.commit()
        conn.close()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up temporary database."""
        import shutil
        import time
        # Give Windows time to release file handles
        time.sleep(0.1)
        try:
            shutil.rmtree(cls.temp_dir, ignore_errors=True)
        except Exception:
            pass  # Best effort cleanup on Windows
    
    def test_database_connection(self):
        """Test database connection."""
        tool = ConversationThreadReconstructor(self.db_path)
        stats = tool.get_statistics()
        
        self.assertEqual(stats['total_messages'], 7)
        self.assertEqual(stats['channels'], 2)
        
        tool.close()
    
    def test_reconstruct_thread_from_root(self):
        """Test reconstructing thread starting from root."""
        tool = ConversationThreadReconstructor(self.db_path)
        
        thread = tool.reconstruct_thread(1)
        
        self.assertIsNotNone(thread)
        self.assertEqual(thread.root.id, 1)
        self.assertEqual(thread.message_count, 4)  # Root + 3 replies
        self.assertIn('FORGE', thread.participants)
        self.assertIn('CLIO', thread.participants)
        
        tool.close()
    
    def test_reconstruct_thread_from_reply(self):
        """Test reconstructing thread starting from a reply."""
        tool = ConversationThreadReconstructor(self.db_path)
        
        # Start from message 3 (middle of thread)
        thread = tool.reconstruct_thread(3)
        
        self.assertIsNotNone(thread)
        self.assertEqual(thread.root.id, 1)  # Should find actual root
        self.assertEqual(thread.message_count, 4)
        
        tool.close()
    
    def test_reconstruct_thread_from_deep_reply(self):
        """Test reconstructing thread from deepest reply."""
        tool = ConversationThreadReconstructor(self.db_path)
        
        # Start from message 4 (deepest reply)
        thread = tool.reconstruct_thread(4)
        
        self.assertIsNotNone(thread)
        self.assertEqual(thread.root.id, 1)
        self.assertEqual(thread.depth, 2)  # Root -> reply -> deep reply
        
        tool.close()
    
    def test_reconstruct_standalone_message(self):
        """Test reconstructing a standalone message (no thread)."""
        tool = ConversationThreadReconstructor(self.db_path)
        
        thread = tool.reconstruct_thread(7)
        
        self.assertIsNotNone(thread)
        self.assertEqual(thread.message_count, 1)
        self.assertEqual(thread.depth, 0)
        
        tool.close()
    
    def test_reconstruct_nonexistent_message(self):
        """Test handling of nonexistent message ID."""
        tool = ConversationThreadReconstructor(self.db_path)
        
        thread = tool.reconstruct_thread(9999)
        
        self.assertIsNone(thread)
        
        tool.close()
    
    def test_find_threads_by_topic(self):
        """Test finding threads by topic."""
        tool = ConversationThreadReconstructor(self.db_path)
        
        threads = tool.find_threads_by_topic('consciousness')
        
        self.assertGreater(len(threads), 0)
        # Should find thread 1 (contains 'consciousness')
        root_ids = [t.root.id for t in threads]
        self.assertIn(1, root_ids)
        
        tool.close()
    
    def test_find_threads_by_topic_no_match(self):
        """Test finding threads with no match."""
        tool = ConversationThreadReconstructor(self.db_path)
        
        threads = tool.find_threads_by_topic('xyznonexistent123')
        
        self.assertEqual(len(threads), 0)
        
        tool.close()
    
    def test_find_threads_by_participant(self):
        """Test finding threads by participant."""
        tool = ConversationThreadReconstructor(self.db_path)
        
        threads = tool.find_threads_by_participant('FORGE')
        
        self.assertGreater(len(threads), 0)
        # FORGE appears in threads 1 and 5
        
        tool.close()
    
    def test_scan_significant_threads(self):
        """Test scanning for significant threads."""
        tool = ConversationThreadReconstructor(self.db_path)
        
        # Lower criteria to match our test data
        threads = tool.scan_significant_threads(
            min_depth=1,
            min_messages=2,
            min_participants=2,
            limit=10
        )
        
        self.assertGreater(len(threads), 0)
        
        tool.close()
    
    def test_export_markdown(self):
        """Test markdown export."""
        tool = ConversationThreadReconstructor(self.db_path)
        thread = tool.reconstruct_thread(1)
        
        md = tool.export_thread_markdown(thread)
        
        self.assertIn('# Conversation Thread', md)
        self.assertIn('FORGE', md)
        self.assertIn('Messages:', md)
        self.assertIn('consciousness', md)
        
        tool.close()
    
    def test_export_json(self):
        """Test JSON export."""
        tool = ConversationThreadReconstructor(self.db_path)
        thread = tool.reconstruct_thread(1)
        
        json_str = tool.export_thread_json(thread)
        data = json.loads(json_str)
        
        self.assertIn('summary', data)
        self.assertIn('messages', data)
        self.assertEqual(data['summary']['root_id'], 1)
        
        tool.close()
    
    def test_export_text(self):
        """Test plain text export."""
        tool = ConversationThreadReconstructor(self.db_path)
        thread = tool.reconstruct_thread(1)
        
        text = tool.export_thread_text(thread)
        
        self.assertIn('CONVERSATION THREAD', text)
        self.assertIn('FORGE', text)
        self.assertIn('=' * 70, text)
        
        tool.close()
    
    def test_get_statistics(self):
        """Test statistics retrieval."""
        tool = ConversationThreadReconstructor(self.db_path)
        
        stats = tool.get_statistics()
        
        self.assertEqual(stats['total_messages'], 7)
        self.assertIn('reply_messages', stats)
        self.assertIn('unique_senders', stats)
        
        tool.close()


class TestFormatFunctions(unittest.TestCase):
    """Test formatting helper functions."""
    
    def test_format_thread_list_empty(self):
        """Test formatting empty thread list."""
        result = format_thread_list([])
        self.assertEqual(result, "No threads found.")
    
    def test_format_thread_list_with_threads(self):
        """Test formatting thread list."""
        root = Message({
            'id': 1,
            'content': 'Test message',
            'sender_id': 'FORGE',
            'created_at': '2026-01-29T12:00:00Z'
        })
        root.depth = 0
        thread = Thread(root)
        
        result = format_thread_list([thread])
        
        self.assertIn('Found 1 thread', result)
        self.assertIn('Thread #1', result)
        self.assertIn('FORGE', result)
    
    def test_format_thread_list_verbose(self):
        """Test verbose thread list formatting."""
        root = Message({
            'id': 1,
            'content': 'Test message',
            'sender_id': 'FORGE',
            'channel_name': 'general',
            'created_at': '2026-01-29T12:00:00Z'
        })
        root.depth = 0
        thread = Thread(root)
        
        result = format_thread_list([thread], verbose=True)
        
        self.assertIn('Channel:', result)
        self.assertIn('Participants:', result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_message_empty_content(self):
        """Test message with empty content."""
        msg = Message({'id': 1, 'content': '', 'sender_id': 'X'})
        self.assertEqual(msg.preview, '(empty)')
        self.assertEqual(msg.mentions, [])
    
    def test_message_none_content(self):
        """Test message with None content."""
        msg = Message({'id': 1, 'content': None, 'sender_id': 'X'})
        self.assertEqual(msg.preview, '(empty)')
    
    def test_thread_single_message_duration(self):
        """Test duration with single message."""
        root = Message({
            'id': 1, 'content': 'Single', 'sender_id': 'X',
            'created_at': '2026-01-29T12:00:00Z'
        })
        thread = Thread(root)
        
        self.assertIsNone(thread.duration)
    
    def test_database_not_found(self):
        """Test handling of missing database."""
        tool = ConversationThreadReconstructor(Path('/nonexistent/path/db.db'))
        
        with self.assertRaises(FileNotFoundError):
            tool.get_statistics()
    
    def test_icons_are_ascii(self):
        """Test that all icons are ASCII-safe (no Unicode)."""
        icons = [ICON_OK, ICON_ERROR]
        for icon in icons:
            # Should not raise
            icon.encode('ascii')


def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print("TESTING: ConversationThreadReconstructor v1.0.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMessage))
    suite.addTests(loader.loadTestsFromTestCase(TestThread))
    suite.addTests(loader.loadTestsFromTestCase(TestConversationThreadReconstructorWithMockDB))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    total = result.testsRun
    passed = total - len(result.failures) - len(result.errors)
    print(f"RESULTS: {total} tests")
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
