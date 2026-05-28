"""
Unit tests for the TextFormatter module

Tests the small caps conversion functionality and character preservation.
"""

import pytest
from text_formatter import TextFormatter


class TestTextFormatter:
    """Test suite for TextFormatter class"""
    
    def test_to_small_caps_basic_uppercase(self):
        """Test conversion of basic uppercase letters"""
        result = TextFormatter.to_small_caps("HELLO")
        assert result == "ʜᴇʟʟᴏ"
    
    def test_to_small_caps_basic_lowercase(self):
        """Test conversion of basic lowercase letters"""
        result = TextFormatter.to_small_caps("hello")
        assert result == "ʜᴇʟʟᴏ"
    
    def test_to_small_caps_mixed_case(self):
        """Test conversion of mixed case letters"""
        result = TextFormatter.to_small_caps("Hello World")
        assert result == "ʜᴇʟʟᴏ ᴡᴏʀʟᴅ"
    
    def test_to_small_caps_preserves_numbers(self):
        """Test that numbers are preserved during conversion"""
        result = TextFormatter.to_small_caps("Test123")
        assert result == "ᴛᴇsᴛ123"
        
        result = TextFormatter.to_small_caps("File Size: 456 MB")
        assert result == "ғɪʟᴇ sɪᴢᴇ: 456 ᴍʙ"
    
    def test_to_small_caps_preserves_punctuation(self):
        """Test that punctuation is preserved during conversion"""
        result = TextFormatter.to_small_caps("Hello, World!")
        assert result == "ʜᴇʟʟᴏ, ᴡᴏʀʟᴅ!"
        
        result = TextFormatter.to_small_caps("Test: ABC; DEF.")
        assert result == "ᴛᴇsᴛ: ᴀʙᴄ; ᴅᴇғ."
    
    def test_to_small_caps_preserves_special_characters(self):
        """Test that special characters are preserved during conversion"""
        result = TextFormatter.to_small_caps("Test_File-Name@123")
        assert result == "ᴛᴇsᴛ_ғɪʟᴇ-ɴᴀᴍᴇ@123"
        
        result = TextFormatter.to_small_caps("Price: $100 (USD)")
        assert result == "ᴘʀɪᴄᴇ: $100 (ᴜsᴅ)"
    
    def test_to_small_caps_preserves_spaces(self):
        """Test that spaces are preserved during conversion"""
        result = TextFormatter.to_small_caps("Multiple   Spaces")
        assert result == "ᴍᴜʟᴛɪᴘʟᴇ   sᴘᴀᴄᴇs"
    
    def test_to_small_caps_empty_string(self):
        """Test conversion of empty string"""
        result = TextFormatter.to_small_caps("")
        assert result == ""
    
    def test_to_small_caps_only_numbers(self):
        """Test string with only numbers"""
        result = TextFormatter.to_small_caps("123456")
        assert result == "123456"
    
    def test_to_small_caps_only_punctuation(self):
        """Test string with only punctuation"""
        result = TextFormatter.to_small_caps("!@#$%^&*()")
        assert result == "!@#$%^&*()"
    
    def test_to_small_caps_all_letters(self):
        """Test conversion of all alphabet letters"""
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        
        result_upper = TextFormatter.to_small_caps(uppercase)
        result_lower = TextFormatter.to_small_caps(lowercase)
        
        # Both should produce the same small caps output
        assert result_upper == result_lower
        
        # Verify specific mappings
        assert result_upper == "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    
    def test_to_small_caps_unicode_preservation(self):
        """Test that existing Unicode characters are preserved"""
        result = TextFormatter.to_small_caps("Test 😊 Emoji")
        assert result == "ᴛᴇsᴛ 😊 ᴇᴍᴏᴊɪ"
    
    def test_to_small_caps_newlines_and_tabs(self):
        """Test that newlines and tabs are preserved"""
        result = TextFormatter.to_small_caps("Line1\nLine2\tTab")
        assert result == "ʟɪɴᴇ1\nʟɪɴᴇ2\tᴛᴀʙ"
    
    def test_to_small_caps_real_world_example(self):
        """Test with a real-world bot message example"""
        message = "File Name: Movie.mp4\nSize: 1.5 GB\nQuality: HD"
        result = TextFormatter.to_small_caps(message)
        expected = "ғɪʟᴇ ɴᴀᴍᴇ: ᴍᴏᴠɪᴇ.ᴍᴘ4\nsɪᴢᴇ: 1.5 ɢʙ\nǫᴜᴀʟɪᴛʏ: ʜᴅ"
        assert result == expected
    
    def test_small_caps_map_completeness(self):
        """Test that SMALL_CAPS_MAP contains all required mappings"""
        # Check uppercase letters
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            assert char in TextFormatter.SMALL_CAPS_MAP
        
        # Check lowercase letters
        for char in "abcdefghijklmnopqrstuvwxyz":
            assert char in TextFormatter.SMALL_CAPS_MAP
        
        # Verify map has exactly 52 entries (26 uppercase + 26 lowercase)
        assert len(TextFormatter.SMALL_CAPS_MAP) == 52


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
