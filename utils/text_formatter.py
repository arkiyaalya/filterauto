"""
Text Formatter Module

This module provides text formatting utilities for the VJ-FILTER-BOT,
including Unicode small caps conversion, Telegram markdown formatting,
and code block preservation.

Requirements: 4.1, 4.3, 4.4, 4.5, 4.6, 4.7
"""

import re
from typing import Dict


class TextFormatter:
    """
    Provides static methods for text formatting and conversion.
    
    Features:
    - Unicode small caps conversion (A-Z → ᴀ-ᴢ)
    - Telegram markdown formatting (italic, blockquote, expandable, code)
    - Code block preservation
    - Button text formatting
    - File info formatting
    """
    
    # Unicode small caps mapping (A-Z → ᴀ-ᴢ)
    SMALL_CAPS_MAP: Dict[str, str] = {
        'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ғ', 'G': 'ɢ', 'H': 'ʜ',
        'I': 'ɪ', 'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 'O': 'ᴏ', 'P': 'ᴘ',
        'Q': 'ǫ', 'R': 'ʀ', 'S': 's', 'T': 'ᴛ', 'U': 'ᴜ', 'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x',
        'Y': 'ʏ', 'Z': 'ᴢ',
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ'
    }
    
    @staticmethod
    def to_small_caps(text: str) -> str:
        """
        Convert ASCII letters to Unicode small caps.
        
        Preserves numbers, punctuation, special characters, and emojis.
        
        Args:
            text: Input text to convert
            
        Returns:
            Text with ASCII letters converted to small caps
            
        Example:
            >>> TextFormatter.to_small_caps("Hello World 123!")
            'ʜᴇʟʟᴏ ᴡᴏʀʟᴅ 123!'
        """
        if not text:
            return text
        
        result = []
        for char in text:
            # Convert if it's in the mapping, otherwise keep original
            result.append(TextFormatter.SMALL_CAPS_MAP.get(char, char))
        
        return ''.join(result)
    
    @staticmethod
    def format_message(text: str, style: str = "italic") -> str:
        """
        Apply Telegram markdown formatting to text.
        
        Supported styles:
        - "italic": Italic text
        - "blockquote": Blockquote formatting
        - "expandable": Expandable quote (for long messages)
        - "code": Inline code formatting
        
        Args:
            text: Text to format
            style: Formatting style to apply
            
        Returns:
            Formatted text with Telegram markdown
            
        Example:
            >>> TextFormatter.format_message("Important notice", "blockquote")
            '<blockquote>Important notice</blockquote>'
        """
        if not text:
            return text
        
        if style == "italic":
            return f"<i>{text}</i>"
        elif style == "blockquote":
            return f"<blockquote>{text}</blockquote>"
        elif style == "expandable":
            return f"<blockquote expandable>{text}</blockquote>"
        elif style == "code":
            return f"<code>{text}</code>"
        else:
            return text
    
    @staticmethod
    def preserve_code_blocks(text: str) -> tuple[str, list[str]]:
        """
        Extract code blocks from text to preserve them during transformation.
        
        Detects code block markers (```, `) and extracts the content.
        
        Args:
            text: Text containing potential code blocks
            
        Returns:
            Tuple of (text_with_placeholders, list_of_code_blocks)
            
        Example:
            >>> text = "Hello `code` world"
            >>> TextFormatter.preserve_code_blocks(text)
            ('Hello __CODE_0__ world', ['code'])
        """
        code_blocks = []
        
        # Pattern for triple backticks
        triple_pattern = r'```[\s\S]*?```'
        # Pattern for single backticks
        single_pattern = r'`[^`]+`'
        
        # Extract triple backtick blocks first
        def replace_triple(match):
            code_blocks.append(match.group(0))
            return f"__CODE_{len(code_blocks)-1}__"
        
        text = re.sub(triple_pattern, replace_triple, text)
        
        # Extract single backtick blocks
        def replace_single(match):
            code_blocks.append(match.group(0))
            return f"__CODE_{len(code_blocks)-1}__"
        
        text = re.sub(single_pattern, replace_single, text)
        
        return text, code_blocks
    
    @staticmethod
    def restore_code_blocks(text: str, code_blocks: list[str]) -> str:
        """
        Restore code blocks to text after transformation.
        
        Args:
            text: Text with code block placeholders
            code_blocks: List of original code blocks
            
        Returns:
            Text with code blocks restored
        """
        for i, block in enumerate(code_blocks):
            text = text.replace(f"__CODE_{i}__", block)
        
        return text
    
    @staticmethod
    def format_button_text(text: str) -> str:
        """
        Format button text with small caps.
        
        Ensures consistent formatting across all buttons.
        
        Args:
            text: Button text to format
            
        Returns:
            Formatted button text in small caps
            
        Example:
            >>> TextFormatter.format_button_text("Next Page")
            'ɴᴇxᴛ ᴘᴀɢᴇ'
        """
        return TextFormatter.to_small_caps(text)
    
    @staticmethod
    def format_file_info(file: Dict) -> str:
        """
        Format file metadata with clear labels and consistent spacing.
        
        Args:
            file: Dictionary containing file metadata
                  Expected keys: file_name, file_size, caption (optional)
            
        Returns:
            Formatted file information string
            
        Example:
            >>> file = {"file_name": "movie.mp4", "file_size": 1024000}
            >>> TextFormatter.format_file_info(file)
            '📂 ғɪʟᴇ ɴᴀᴍᴇ: movie.mp4\\n⚙️ sɪᴢᴇ: 1000.00 KB'
        """
        lines = []
        
        # File name
        if 'file_name' in file:
            file_name = file['file_name']
            lines.append(f"📂 {TextFormatter.to_small_caps('File Name')}: {file_name}")
        
        # File size
        if 'file_size' in file:
            size = file['file_size']
            size_str = TextFormatter._format_file_size(size)
            lines.append(f"⚙️ {TextFormatter.to_small_caps('Size')}: {size_str}")
        
        # Caption (if available)
        if 'caption' in file and file['caption']:
            caption = file['caption']
            lines.append(f"📝 {TextFormatter.to_small_caps('Caption')}: {caption}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def _format_file_size(size_bytes: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes: File size in bytes
            
        Returns:
            Formatted size string (e.g., "1.5 MB")
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    
    @staticmethod
    def format_with_code_preservation(text: str, apply_small_caps: bool = True) -> str:
        """
        Apply formatting while preserving code blocks.
        
        This is a convenience method that combines code block preservation
        with small caps conversion.
        
        Args:
            text: Text to format
            apply_small_caps: Whether to apply small caps conversion
            
        Returns:
            Formatted text with code blocks preserved
        """
        # Extract code blocks
        text_without_code, code_blocks = TextFormatter.preserve_code_blocks(text)
        
        # Apply small caps if requested
        if apply_small_caps:
            text_without_code = TextFormatter.to_small_caps(text_without_code)
        
        # Restore code blocks
        return TextFormatter.restore_code_blocks(text_without_code, code_blocks)


# Convenience function for global access
def format_text(text: str, style: str = None, small_caps: bool = False) -> str:
    """
    Convenience function for text formatting.
    
    Args:
        text: Text to format
        style: Optional Telegram markdown style
        small_caps: Whether to convert to small caps
        
    Returns:
        Formatted text
    """
    if small_caps:
        text = TextFormatter.format_with_code_preservation(text, apply_small_caps=True)
    
    if style:
        text = TextFormatter.format_message(text, style)
    
    return text
