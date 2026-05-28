"""
UI Renderer Module

This module provides UI rendering utilities for the VJ-FILTER-BOT,
including search results formatting, button layout organization,
and admin panel rendering.

Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.6, 9.1, 9.2, 9.3, 9.6
"""

from typing import List, Dict, Tuple, Any
from pyrogram.types import InlineKeyboardButton
from utils.text_formatter import TextFormatter


class UIRenderer:
    """
    Renders UI components with consistent formatting and layout.
    
    Features:
    - Search results formatting with small caps
    - Button layout organization (max 2 per row)
    - File details rendering
    - Admin panel rendering
    - Pagination support
    """
    
    def __init__(self, formatter: TextFormatter = None):
        """
        Initialize UI renderer.
        
        Args:
            formatter: TextFormatter instance (creates new one if not provided)
        """
        self.formatter = formatter or TextFormatter()
    
    async def render_search_results(
        self,
        files: List[Dict],
        query: str,
        offset: int,
        total: int
    ) -> Tuple[str, List[List[InlineKeyboardButton]]]:
        """
        Render search results message and button layout.
        
        Args:
            files: List of file dictionaries
            query: Search query string
            offset: Current result offset
            total: Total number of results
            
        Returns:
            Tuple of (message_text, button_layout)
        """
        # Format title with small caps
        title = self.formatter.to_small_caps(f"Search Results for: {query}")
        
        # Build message
        lines = [f"<b>{title}</b>", ""]
        
        # Add result count
        showing_from = offset + 1
        showing_to = min(offset + len(files), total)
        count_text = self.formatter.to_small_caps(f"Showing {showing_from}-{showing_to} of {total} results")
        lines.append(count_text)
        lines.append("─" * 30)
        lines.append("")
        
        message_text = '\n'.join(lines)
        
        # Create button layout (max 2 buttons per row)
        button_layout = self._create_button_layout(files)
        
        # Add pagination buttons if needed
        if total > 50:
            pagination_buttons = self._create_pagination_buttons(query, offset, total)
            if pagination_buttons:
                button_layout.append(pagination_buttons)
        
        return message_text, button_layout
    
    def _create_button_layout(self, files: List[Dict]) -> List[List[InlineKeyboardButton]]:
        """
        Create button layout with maximum 2 buttons per row.
        
        Args:
            files: List of file dictionaries
            
        Returns:
            List of button rows
        """
        buttons = []
        row = []
        
        for file in files:
            # Format button text
            button_text = self.formatter.format_button_text(file.get('file_name', 'File'))
            
            # Truncate if too long
            if len(button_text) > 30:
                button_text = button_text[:27] + "..."
            
            # Create button
            button = InlineKeyboardButton(
                text=button_text,
                callback_data=f"file_{file.get('file_id', '')}"
            )
            
            row.append(button)
            
            # Add row when it has 2 buttons
            if len(row) == 2:
                buttons.append(row)
                row = []
        
        # Add remaining button if any
        if row:
            buttons.append(row)
        
        return buttons
    
    def _create_pagination_buttons(
        self,
        query: str,
        offset: int,
        total: int
    ) -> List[InlineKeyboardButton]:
        """
        Create pagination buttons (Previous/Next).
        
        Args:
            query: Search query
            offset: Current offset
            total: Total results
            
        Returns:
            List of pagination buttons
        """
        buttons = []
        
        # Previous button
        if offset > 0:
            prev_text = self.formatter.format_button_text("◀️ Previous")
            buttons.append(InlineKeyboardButton(
                text=prev_text,
                callback_data=f"prev_{offset-50}_{query}"
            ))
        
        # Next button
        if offset + 50 < total:
            next_text = self.formatter.format_button_text("Next ▶️")
            buttons.append(InlineKeyboardButton(
                text=next_text,
                callback_data=f"next_{offset+50}_{query}"
            ))
        
        return buttons if buttons else []
    
    async def render_file_details(self, file: Dict) -> str:
        """
        Render detailed file information.
        
        Args:
            file: File dictionary with metadata
            
        Returns:
            Formatted file details string
        """
        # Use TextFormatter to format file info
        file_info = self.formatter.format_file_info(file)
        
        # Add visual separator
        separator = "─" * 30
        
        # Build message
        title = self.formatter.to_small_caps("File Details")
        message = f"<b>{title}</b>\n{separator}\n\n{file_info}"
        
        return message
    
    async def render_admin_panel(self, stats: Dict) -> str:
        """
        Render admin statistics panel.
        
        Args:
            stats: Dictionary containing performance metrics
                   Expected keys: response_time, cache_hit_rate, 
                                 connection_count, memory_usage
            
        Returns:
            Formatted admin panel string
        """
        lines = []
        
        # Title
        title = self.formatter.to_small_caps("Admin Statistics Panel")
        lines.append(f"<b>{title}</b>")
        lines.append("═" * 35)
        lines.append("")
        
        # Performance Metrics
        if 'response_time' in stats:
            label = self.formatter.to_small_caps("Average Response Time")
            value = f"{stats['response_time']:.2f}s"
            lines.append(f"⚡ {label}: <code>{value}</code>")
        
        if 'cache_hit_rate' in stats:
            label = self.formatter.to_small_caps("Cache Hit Rate")
            value = f"{stats['cache_hit_rate']:.1f}%"
            lines.append(f"📊 {label}: <code>{value}</code>")
        
        lines.append("")
        
        # Database Metrics
        if 'connection_count' in stats:
            label = self.formatter.to_small_caps("Active Connections")
            value = stats['connection_count']
            lines.append(f"🔗 {label}: <code>{value}</code>")
        
        if 'database_status' in stats:
            label = self.formatter.to_small_caps("Database Status")
            status = stats['database_status']
            status_emoji = "✅" if status == "healthy" else "⚠️"
            lines.append(f"{status_emoji} {label}: <code>{status}</code>")
        
        lines.append("")
        
        # System Metrics
        if 'memory_usage' in stats:
            label = self.formatter.to_small_caps("Memory Usage")
            value = f"{stats['memory_usage']:.1f} MB"
            lines.append(f"💾 {label}: <code>{value}</code>")
        
        if 'uptime' in stats:
            label = self.formatter.to_small_caps("Uptime")
            value = stats['uptime']
            lines.append(f"⏱️ {label}: <code>{value}</code>")
        
        # Apply blockquote formatting to important metrics
        message = '\n'.join(lines)
        
        return message
    
    async def render_database_list(self, databases: List[Dict]) -> str:
        """
        Render list of database connections.
        
        Args:
            databases: List of database connection dictionaries
                      Expected keys: name, uri, status, last_check
            
        Returns:
            Formatted database list string
        """
        lines = []
        
        # Title
        title = self.formatter.to_small_caps("Database Connections")
        lines.append(f"<b>{title}</b>")
        lines.append("═" * 35)
        lines.append("")
        
        if not databases:
            no_db_text = self.formatter.to_small_caps("No databases configured")
            lines.append(f"<i>{no_db_text}</i>")
        else:
            for i, db in enumerate(databases, 1):
                # Database name
                name = db.get('name', 'Unknown')
                lines.append(f"<b>{i}. {name}</b>")
                
                # Status
                status = db.get('status', 'unknown')
                status_emoji = "✅" if status == "active" else "❌"
                status_label = self.formatter.to_small_caps("Status")
                lines.append(f"   {status_emoji} {status_label}: <code>{status}</code>")
                
                # Masked URI
                uri = db.get('uri', '')
                masked_uri = self._mask_uri(uri)
                uri_label = self.formatter.to_small_caps("URI")
                lines.append(f"   🔗 {uri_label}: <code>{masked_uri}</code>")
                
                # Last check
                if 'last_check' in db:
                    check_label = self.formatter.to_small_caps("Last Check")
                    lines.append(f"   ⏰ {check_label}: <code>{db['last_check']}</code>")
                
                lines.append("")
        
        # Total count
        total_label = self.formatter.to_small_caps(f"Total: {len(databases)} database(s)")
        active_count = sum(1 for db in databases if db.get('status') == 'active')
        active_label = self.formatter.to_small_caps(f"{active_count} active")
        lines.append(f"<b>{total_label}</b> ({active_label})")
        
        return '\n'.join(lines)
    
    @staticmethod
    def _mask_uri(uri: str) -> str:
        """
        Mask database URI for security (show only last 4 characters).
        
        Args:
            uri: Full database URI
            
        Returns:
            Masked URI string
        """
        if len(uri) <= 4:
            return "****"
        return "..." + uri[-4:]
    
    async def render_cache_stats(self, cache_stats: Dict) -> str:
        """
        Render cache statistics.
        
        Args:
            cache_stats: Dictionary with cache statistics
            
        Returns:
            Formatted cache statistics string
        """
        lines = []
        
        # Title
        title = self.formatter.to_small_caps("Cache Statistics")
        lines.append(f"<b>{title}</b>")
        lines.append("═" * 35)
        lines.append("")
        
        # Overall stats
        if 'total' in cache_stats:
            total = cache_stats['total']
            lines.append(f"<b>{self.formatter.to_small_caps('Overall Performance')}</b>")
            lines.append(f"📊 {self.formatter.to_small_caps('Hit Rate')}: <code>{total.get('hit_rate', 0):.1f}%</code>")
            lines.append(f"✅ {self.formatter.to_small_caps('Hits')}: <code>{total.get('hits', 0)}</code>")
            lines.append(f"❌ {self.formatter.to_small_caps('Misses')}: <code>{total.get('misses', 0)}</code>")
            lines.append("")
        
        # Individual cache stats
        cache_types = ['search', 'user_settings', 'group_settings', 'file_metadata']
        for cache_type in cache_types:
            if cache_type in cache_stats:
                stats = cache_stats[cache_type]
                cache_name = cache_type.replace('_', ' ').title()
                lines.append(f"<b>{self.formatter.to_small_caps(cache_name)}</b>")
                lines.append(f"   📊 {self.formatter.to_small_caps('Hit Rate')}: <code>{stats.get('hit_rate', 0):.1f}%</code>")
                lines.append(f"   📦 {self.formatter.to_small_caps('Size')}: <code>{stats.get('size', 0)}/{stats.get('maxsize', 0)}</code>")
                lines.append("")
        
        return '\n'.join(lines)


# Global UI renderer instance
_ui_renderer: UIRenderer = None


def get_ui_renderer() -> UIRenderer:
    """
    Get the global UI renderer instance.
    
    Returns:
        The global UIRenderer instance
    """
    global _ui_renderer
    if _ui_renderer is None:
        _ui_renderer = UIRenderer()
    return _ui_renderer
