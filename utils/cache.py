"""
Cache System Module

This module implements an in-memory caching system with TTL (Time To Live) support
for the VJ-FILTER-BOT. It provides caching for search results, user settings,
group settings, and file metadata to reduce database load and improve response times.

Requirements: 1.7, 7.1, 7.2, 7.3, 7.4, 7.5, 9.3
"""

import asyncio
import re
from typing import Any, Dict, List, Optional
from datetime import datetime
from cachetools import TTLCache
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Manages multiple TTL-based caches for different data types.
    
    Provides async methods for get/set operations, cache invalidation with pattern
    matching, and statistics tracking (hits, misses, size).
    """
    
    def __init__(self):
        """
        Initialize cache manager with separate TTL caches for different data types.
        
        Cache configurations:
        - search_cache: 1000 items, 300s TTL (5 minutes)
        - user_settings_cache: 500 items, 600s TTL (10 minutes)
        - group_settings_cache: 500 items, 600s TTL (10 minutes)
        - file_metadata_cache: 2000 items, 300s TTL (5 minutes)
        """
        # Initialize TTL caches with specified sizes and TTL values
        self.search_cache = TTLCache(maxsize=1000, ttl=300)  # 5 minutes
        self.user_settings_cache = TTLCache(maxsize=500, ttl=600)  # 10 minutes
        self.group_settings_cache = TTLCache(maxsize=500, ttl=600)  # 10 minutes
        self.file_metadata_cache = TTLCache(maxsize=2000, ttl=300)  # 5 minutes
        
        # Statistics tracking
        self._stats = {
            'search': {'hits': 0, 'misses': 0},
            'user_settings': {'hits': 0, 'misses': 0},
            'group_settings': {'hits': 0, 'misses': 0},
            'file_metadata': {'hits': 0, 'misses': 0}
        }
        
        # Lock for thread-safe operations
        self._lock = asyncio.Lock()
        
        logger.info("CacheManager initialized with TTL caches")
    
    # Search Results Cache Methods
    
    async def get_search_results(self, query: str, offset: int = 0, limit: int = 50) -> Optional[List[Dict]]:
        """
        Get cached search results.
        
        Args:
            query: The search query string
            offset: Result offset for pagination
            limit: Maximum number of results
            
        Returns:
            List of file dictionaries if cached, None if not found or expired
        """
        key = self._make_search_key(query, offset, limit)
        async with self._lock:
            try:
                value = self.search_cache.get(key)
                if value is not None:
                    self._stats['search']['hits'] += 1
                    logger.debug(f"Cache HIT for search key: {key}")
                    return value
                else:
                    self._stats['search']['misses'] += 1
                    logger.debug(f"Cache MISS for search key: {key}")
                    return None
            except Exception as e:
                logger.error(f"Error getting search cache: {e}")
                self._stats['search']['misses'] += 1
                return None
    
    async def set_search_results(self, query: str, value: List[Dict], offset: int = 0, limit: int = 50) -> None:
        """
        Cache search results.
        
        Args:
            query: The search query string
            value: List of file dictionaries to cache
            offset: Result offset for pagination
            limit: Maximum number of results
        """
        key = self._make_search_key(query, offset, limit)
        async with self._lock:
            try:
                self.search_cache[key] = value
                logger.debug(f"Cached search results for key: {key} ({len(value)} items)")
            except Exception as e:
                logger.error(f"Error setting search cache: {e}")
    
    @staticmethod
    def _make_search_key(query: str, offset: int, limit: int) -> str:
        """Generate cache key for search results."""
        return f"search:{query}:{offset}:{limit}"
    
    # User Settings Cache Methods
    
    async def get_user_settings(self, user_id: int) -> Optional[Dict]:
        """
        Get cached user settings.
        
        Args:
            user_id: The Telegram user ID
            
        Returns:
            User settings dictionary if cached, None if not found or expired
        """
        key = self._make_user_settings_key(user_id)
        async with self._lock:
            try:
                value = self.user_settings_cache.get(key)
                if value is not None:
                    self._stats['user_settings']['hits'] += 1
                    logger.debug(f"Cache HIT for user settings: {user_id}")
                    return value
                else:
                    self._stats['user_settings']['misses'] += 1
                    logger.debug(f"Cache MISS for user settings: {user_id}")
                    return None
            except Exception as e:
                logger.error(f"Error getting user settings cache: {e}")
                self._stats['user_settings']['misses'] += 1
                return None
    
    async def set_user_settings(self, user_id: int, value: Dict) -> None:
        """
        Cache user settings.
        
        Args:
            user_id: The Telegram user ID
            value: User settings dictionary to cache
        """
        key = self._make_user_settings_key(user_id)
        async with self._lock:
            try:
                self.user_settings_cache[key] = value
                logger.debug(f"Cached user settings for user: {user_id}")
            except Exception as e:
                logger.error(f"Error setting user settings cache: {e}")
    
    @staticmethod
    def _make_user_settings_key(user_id: int) -> str:
        """Generate cache key for user settings."""
        return f"user_settings:{user_id}"
    
    # Group Settings Cache Methods
    
    async def get_group_settings(self, group_id: int) -> Optional[Dict]:
        """
        Get cached group settings.
        
        Args:
            group_id: The Telegram group/chat ID
            
        Returns:
            Group settings dictionary if cached, None if not found or expired
        """
        key = self._make_group_settings_key(group_id)
        async with self._lock:
            try:
                value = self.group_settings_cache.get(key)
                if value is not None:
                    self._stats['group_settings']['hits'] += 1
                    logger.debug(f"Cache HIT for group settings: {group_id}")
                    return value
                else:
                    self._stats['group_settings']['misses'] += 1
                    logger.debug(f"Cache MISS for group settings: {group_id}")
                    return None
            except Exception as e:
                logger.error(f"Error getting group settings cache: {e}")
                self._stats['group_settings']['misses'] += 1
                return None
    
    async def set_group_settings(self, group_id: int, value: Dict) -> None:
        """
        Cache group settings.
        
        Args:
            group_id: The Telegram group/chat ID
            value: Group settings dictionary to cache
        """
        key = self._make_group_settings_key(group_id)
        async with self._lock:
            try:
                self.group_settings_cache[key] = value
                logger.debug(f"Cached group settings for group: {group_id}")
            except Exception as e:
                logger.error(f"Error setting group settings cache: {e}")
    
    @staticmethod
    def _make_group_settings_key(group_id: int) -> str:
        """Generate cache key for group settings."""
        return f"group_settings:{group_id}"
    
    # File Metadata Cache Methods
    
    async def get_file_metadata(self, file_id: str) -> Optional[Dict]:
        """
        Get cached file metadata.
        
        Args:
            file_id: The unique file identifier
            
        Returns:
            File metadata dictionary if cached, None if not found or expired
        """
        key = self._make_file_metadata_key(file_id)
        async with self._lock:
            try:
                value = self.file_metadata_cache.get(key)
                if value is not None:
                    self._stats['file_metadata']['hits'] += 1
                    logger.debug(f"Cache HIT for file metadata: {file_id}")
                    return value
                else:
                    self._stats['file_metadata']['misses'] += 1
                    logger.debug(f"Cache MISS for file metadata: {file_id}")
                    return None
            except Exception as e:
                logger.error(f"Error getting file metadata cache: {e}")
                self._stats['file_metadata']['misses'] += 1
                return None
    
    async def set_file_metadata(self, file_id: str, value: Dict) -> None:
        """
        Cache file metadata.
        
        Args:
            file_id: The unique file identifier
            value: File metadata dictionary to cache
        """
        key = self._make_file_metadata_key(file_id)
        async with self._lock:
            try:
                self.file_metadata_cache[key] = value
                logger.debug(f"Cached file metadata for file: {file_id}")
            except Exception as e:
                logger.error(f"Error setting file metadata cache: {e}")
    
    @staticmethod
    def _make_file_metadata_key(file_id: str) -> str:
        """Generate cache key for file metadata."""
        return f"file:{file_id}"
    
    # Cache Invalidation Methods
    
    async def invalidate(self, pattern: str) -> int:
        """
        Invalidate cache entries matching a pattern.
        
        Supports wildcards and regex patterns for flexible invalidation.
        
        Args:
            pattern: Pattern to match cache keys (supports * wildcard and regex)
            
        Returns:
            Number of cache entries invalidated
        """
        async with self._lock:
            count = 0
            
            # Convert wildcard pattern to regex
            regex_pattern = pattern.replace('*', '.*')
            regex = re.compile(regex_pattern)
            
            # Invalidate matching entries in all caches
            for cache_name, cache in [
                ('search', self.search_cache),
                ('user_settings', self.user_settings_cache),
                ('group_settings', self.group_settings_cache),
                ('file_metadata', self.file_metadata_cache)
            ]:
                keys_to_delete = [key for key in cache.keys() if regex.match(str(key))]
                for key in keys_to_delete:
                    try:
                        del cache[key]
                        count += 1
                    except KeyError:
                        pass  # Key already expired or deleted
            
            logger.info(f"Invalidated {count} cache entries matching pattern: {pattern}")
            return count
    
    async def invalidate_file(self, file_id: str) -> None:
        """
        Invalidate all cache entries related to a specific file.
        
        This includes:
        - File metadata cache
        - Search results that might contain this file
        
        Args:
            file_id: The unique file identifier
        """
        await self.invalidate(f"file:{file_id}")
        # Also invalidate all search results as they might contain this file
        await self.invalidate("search:*")
        logger.info(f"Invalidated all cache entries for file: {file_id}")
    
    async def invalidate_user(self, user_id: int) -> None:
        """
        Invalidate all cache entries related to a specific user.
        
        Args:
            user_id: The Telegram user ID
        """
        await self.invalidate(f"user_settings:{user_id}")
        logger.info(f"Invalidated cache entries for user: {user_id}")
    
    async def invalidate_group(self, group_id: int) -> None:
        """
        Invalidate all cache entries related to a specific group.
        
        Args:
            group_id: The Telegram group/chat ID
        """
        await self.invalidate(f"group_settings:{group_id}")
        logger.info(f"Invalidated cache entries for group: {group_id}")
    
    async def clear_all(self) -> None:
        """
        Clear all caches.
        
        This removes all cached data from all cache types.
        """
        async with self._lock:
            self.search_cache.clear()
            self.user_settings_cache.clear()
            self.group_settings_cache.clear()
            self.file_metadata_cache.clear()
            logger.info("Cleared all caches")
    
    # Statistics Methods
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary containing:
            - hits: Number of cache hits per cache type
            - misses: Number of cache misses per cache type
            - hit_rate: Cache hit rate percentage per cache type
            - size: Current number of items in each cache
            - total_hits: Total hits across all caches
            - total_misses: Total misses across all caches
            - total_hit_rate: Overall hit rate percentage
        """
        stats = {
            'search': self._get_cache_stats('search', self.search_cache),
            'user_settings': self._get_cache_stats('user_settings', self.user_settings_cache),
            'group_settings': self._get_cache_stats('group_settings', self.group_settings_cache),
            'file_metadata': self._get_cache_stats('file_metadata', self.file_metadata_cache)
        }
        
        # Calculate totals
        total_hits = sum(s['hits'] for s in stats.values())
        total_misses = sum(s['misses'] for s in stats.values())
        total_requests = total_hits + total_misses
        
        stats['total'] = {
            'hits': total_hits,
            'misses': total_misses,
            'requests': total_requests,
            'hit_rate': (total_hits / total_requests * 100) if total_requests > 0 else 0.0
        }
        
        return stats
    
    def _get_cache_stats(self, cache_type: str, cache: TTLCache) -> Dict[str, Any]:
        """
        Get statistics for a specific cache.
        
        Args:
            cache_type: Type of cache (for stats lookup)
            cache: The TTLCache instance
            
        Returns:
            Dictionary with hits, misses, hit_rate, and size
        """
        hits = self._stats[cache_type]['hits']
        misses = self._stats[cache_type]['misses']
        total = hits + misses
        hit_rate = (hits / total * 100) if total > 0 else 0.0
        
        return {
            'hits': hits,
            'misses': misses,
            'requests': total,
            'hit_rate': hit_rate,
            'size': len(cache),
            'maxsize': cache.maxsize,
            'ttl': cache.ttl
        }
    
    def reset_stats(self) -> None:
        """
        Reset all statistics counters to zero.
        
        This does not clear the caches, only the hit/miss counters.
        """
        for cache_type in self._stats:
            self._stats[cache_type]['hits'] = 0
            self._stats[cache_type]['misses'] = 0
        logger.info("Reset cache statistics")
    
    def get_cache_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get detailed information about all caches.
        
        Returns:
            Dictionary with cache configuration and current state
        """
        return {
            'search_cache': {
                'maxsize': self.search_cache.maxsize,
                'ttl': self.search_cache.ttl,
                'current_size': len(self.search_cache),
                'description': 'Search results cache'
            },
            'user_settings_cache': {
                'maxsize': self.user_settings_cache.maxsize,
                'ttl': self.user_settings_cache.ttl,
                'current_size': len(self.user_settings_cache),
                'description': 'User settings cache'
            },
            'group_settings_cache': {
                'maxsize': self.group_settings_cache.maxsize,
                'ttl': self.group_settings_cache.ttl,
                'current_size': len(self.group_settings_cache),
                'description': 'Group settings cache'
            },
            'file_metadata_cache': {
                'maxsize': self.file_metadata_cache.maxsize,
                'ttl': self.file_metadata_cache.ttl,
                'current_size': len(self.file_metadata_cache),
                'description': 'File metadata cache'
            }
        }


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """
    Get the global cache manager instance.
    
    Creates the instance on first call (singleton pattern).
    
    Returns:
        The global CacheManager instance
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager
