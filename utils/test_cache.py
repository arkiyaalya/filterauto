"""
Unit tests for the Cache System Module

Tests cover:
- TTL cache functionality
- Get/set operations for all cache types
- Cache invalidation with pattern matching
- Statistics tracking (hits, misses, hit rate)
- Concurrent access handling
"""

import pytest
import asyncio
from typing import Dict, List
from utils.cache import CacheManager, get_cache_manager


class TestCacheManager:
    """Test suite for CacheManager class"""
    
    @pytest.fixture
    def cache_manager(self):
        """Create a fresh CacheManager instance for each test"""
        return CacheManager()
    
    # Search Results Cache Tests
    
    @pytest.mark.asyncio
    async def test_search_cache_set_and_get(self, cache_manager):
        """Test setting and getting search results from cache"""
        query = "test movie"
        results = [
            {"file_id": "1", "file_name": "test1.mp4"},
            {"file_id": "2", "file_name": "test2.mp4"}
        ]
        
        # Set cache
        await cache_manager.set_search_results(query, results)
        
        # Get cache
        cached_results = await cache_manager.get_search_results(query)
        
        assert cached_results is not None
        assert len(cached_results) == 2
        assert cached_results[0]["file_id"] == "1"
        assert cached_results[1]["file_name"] == "test2.mp4"
    
    @pytest.mark.asyncio
    async def test_search_cache_miss(self, cache_manager):
        """Test cache miss for non-existent search query"""
        result = await cache_manager.get_search_results("nonexistent query")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_search_cache_with_pagination(self, cache_manager):
        """Test search cache with different offset and limit values"""
        query = "test"
        results_page1 = [{"file_id": "1"}]
        results_page2 = [{"file_id": "2"}]
        
        # Cache different pages
        await cache_manager.set_search_results(query, results_page1, offset=0, limit=50)
        await cache_manager.set_search_results(query, results_page2, offset=50, limit=50)
        
        # Retrieve different pages
        page1 = await cache_manager.get_search_results(query, offset=0, limit=50)
        page2 = await cache_manager.get_search_results(query, offset=50, limit=50)
        
        assert page1[0]["file_id"] == "1"
        assert page2[0]["file_id"] == "2"
    
    # User Settings Cache Tests
    
    @pytest.mark.asyncio
    async def test_user_settings_cache(self, cache_manager):
        """Test setting and getting user settings from cache"""
        user_id = 12345
        settings = {"language": "en", "notifications": True}
        
        await cache_manager.set_user_settings(user_id, settings)
        cached_settings = await cache_manager.get_user_settings(user_id)
        
        assert cached_settings is not None
        assert cached_settings["language"] == "en"
        assert cached_settings["notifications"] is True
    
    @pytest.mark.asyncio
    async def test_user_settings_cache_miss(self, cache_manager):
        """Test cache miss for non-existent user"""
        result = await cache_manager.get_user_settings(99999)
        assert result is None
    
    # Group Settings Cache Tests
    
    @pytest.mark.asyncio
    async def test_group_settings_cache(self, cache_manager):
        """Test setting and getting group settings from cache"""
        group_id = -100123456789
        settings = {"welcome_message": "Hello!", "auto_delete": 300}
        
        await cache_manager.set_group_settings(group_id, settings)
        cached_settings = await cache_manager.get_group_settings(group_id)
        
        assert cached_settings is not None
        assert cached_settings["welcome_message"] == "Hello!"
        assert cached_settings["auto_delete"] == 300
    
    @pytest.mark.asyncio
    async def test_group_settings_cache_miss(self, cache_manager):
        """Test cache miss for non-existent group"""
        result = await cache_manager.get_group_settings(-100999999999)
        assert result is None
    
    # File Metadata Cache Tests
    
    @pytest.mark.asyncio
    async def test_file_metadata_cache(self, cache_manager):
        """Test setting and getting file metadata from cache"""
        file_id = "abc123"
        metadata = {
            "file_name": "movie.mp4",
            "file_size": 1024000,
            "caption": "Great movie"
        }
        
        await cache_manager.set_file_metadata(file_id, metadata)
        cached_metadata = await cache_manager.get_file_metadata(file_id)
        
        assert cached_metadata is not None
        assert cached_metadata["file_name"] == "movie.mp4"
        assert cached_metadata["file_size"] == 1024000
    
    @pytest.mark.asyncio
    async def test_file_metadata_cache_miss(self, cache_manager):
        """Test cache miss for non-existent file"""
        result = await cache_manager.get_file_metadata("nonexistent")
        assert result is None
    
    # Cache Invalidation Tests
    
    @pytest.mark.asyncio
    async def test_invalidate_with_exact_pattern(self, cache_manager):
        """Test cache invalidation with exact pattern match"""
        # Add some cache entries
        await cache_manager.set_user_settings(123, {"test": "data"})
        await cache_manager.set_user_settings(456, {"test": "data"})
        
        # Invalidate specific user
        count = await cache_manager.invalidate("user_settings:123")
        
        assert count == 1
        assert await cache_manager.get_user_settings(123) is None
        assert await cache_manager.get_user_settings(456) is not None
    
    @pytest.mark.asyncio
    async def test_invalidate_with_wildcard_pattern(self, cache_manager):
        """Test cache invalidation with wildcard pattern"""
        # Add multiple search results
        await cache_manager.set_search_results("movie", [{"id": "1"}])
        await cache_manager.set_search_results("film", [{"id": "2"}])
        await cache_manager.set_user_settings(123, {"test": "data"})
        
        # Invalidate all search results
        count = await cache_manager.invalidate("search:*")
        
        assert count == 2
        assert await cache_manager.get_search_results("movie") is None
        assert await cache_manager.get_search_results("film") is None
        assert await cache_manager.get_user_settings(123) is not None
    
    @pytest.mark.asyncio
    async def test_invalidate_file(self, cache_manager):
        """Test file-specific invalidation"""
        file_id = "test123"
        
        # Add file metadata and search results
        await cache_manager.set_file_metadata(file_id, {"name": "test.mp4"})
        await cache_manager.set_search_results("test", [{"file_id": file_id}])
        
        # Invalidate file
        await cache_manager.invalidate_file(file_id)
        
        # Both file metadata and search results should be invalidated
        assert await cache_manager.get_file_metadata(file_id) is None
        assert await cache_manager.get_search_results("test") is None
    
    @pytest.mark.asyncio
    async def test_invalidate_user(self, cache_manager):
        """Test user-specific invalidation"""
        user_id = 12345
        
        await cache_manager.set_user_settings(user_id, {"test": "data"})
        await cache_manager.invalidate_user(user_id)
        
        assert await cache_manager.get_user_settings(user_id) is None
    
    @pytest.mark.asyncio
    async def test_invalidate_group(self, cache_manager):
        """Test group-specific invalidation"""
        group_id = -100123456789
        
        await cache_manager.set_group_settings(group_id, {"test": "data"})
        await cache_manager.invalidate_group(group_id)
        
        assert await cache_manager.get_group_settings(group_id) is None
    
    @pytest.mark.asyncio
    async def test_clear_all(self, cache_manager):
        """Test clearing all caches"""
        # Add entries to all caches
        await cache_manager.set_search_results("test", [{"id": "1"}])
        await cache_manager.set_user_settings(123, {"test": "data"})
        await cache_manager.set_group_settings(-100123, {"test": "data"})
        await cache_manager.set_file_metadata("file1", {"name": "test.mp4"})
        
        # Clear all
        await cache_manager.clear_all()
        
        # All caches should be empty
        assert await cache_manager.get_search_results("test") is None
        assert await cache_manager.get_user_settings(123) is None
        assert await cache_manager.get_group_settings(-100123) is None
        assert await cache_manager.get_file_metadata("file1") is None
    
    # Statistics Tests
    
    @pytest.mark.asyncio
    async def test_statistics_tracking(self, cache_manager):
        """Test that cache hits and misses are tracked correctly"""
        # Perform some cache operations
        await cache_manager.set_search_results("test", [{"id": "1"}])
        
        # Hit
        await cache_manager.get_search_results("test")
        
        # Miss
        await cache_manager.get_search_results("nonexistent")
        
        # Get stats
        stats = cache_manager.get_stats()
        
        assert stats['search']['hits'] == 1
        assert stats['search']['misses'] == 1
        assert stats['search']['requests'] == 2
        assert stats['search']['hit_rate'] == 50.0
    
    @pytest.mark.asyncio
    async def test_statistics_multiple_cache_types(self, cache_manager):
        """Test statistics across multiple cache types"""
        # Add and retrieve from different caches
        await cache_manager.set_user_settings(123, {"test": "data"})
        await cache_manager.get_user_settings(123)  # Hit
        await cache_manager.get_user_settings(456)  # Miss
        
        await cache_manager.set_file_metadata("file1", {"name": "test"})
        await cache_manager.get_file_metadata("file1")  # Hit
        
        stats = cache_manager.get_stats()
        
        assert stats['user_settings']['hits'] == 1
        assert stats['user_settings']['misses'] == 1
        assert stats['file_metadata']['hits'] == 1
        assert stats['file_metadata']['misses'] == 0
        
        # Check totals
        assert stats['total']['hits'] == 2
        assert stats['total']['misses'] == 1
        assert stats['total']['requests'] == 3
    
    @pytest.mark.asyncio
    async def test_reset_stats(self, cache_manager):
        """Test resetting statistics without clearing cache"""
        # Add cache entry and access it
        await cache_manager.set_search_results("test", [{"id": "1"}])
        await cache_manager.get_search_results("test")
        
        # Reset stats
        cache_manager.reset_stats()
        
        # Stats should be reset
        stats = cache_manager.get_stats()
        assert stats['search']['hits'] == 0
        assert stats['search']['misses'] == 0
        
        # But cache should still have data
        assert await cache_manager.get_search_results("test") is not None
    
    @pytest.mark.asyncio
    async def test_get_cache_info(self, cache_manager):
        """Test getting cache configuration information"""
        info = cache_manager.get_cache_info()
        
        assert 'search_cache' in info
        assert 'user_settings_cache' in info
        assert 'group_settings_cache' in info
        assert 'file_metadata_cache' in info
        
        # Check search cache info
        assert info['search_cache']['maxsize'] == 1000
        assert info['search_cache']['ttl'] == 300
        assert info['search_cache']['current_size'] == 0
        
        # Check user settings cache info
        assert info['user_settings_cache']['maxsize'] == 500
        assert info['user_settings_cache']['ttl'] == 600
    
    # TTL Tests
    
    @pytest.mark.asyncio
    async def test_ttl_expiration(self, cache_manager):
        """Test that cache entries expire after TTL"""
        # Create a cache manager with very short TTL for testing
        import cachetools
        test_cache = cachetools.TTLCache(maxsize=10, ttl=1)  # 1 second TTL
        cache_manager.search_cache = test_cache
        
        # Add entry
        await cache_manager.set_search_results("test", [{"id": "1"}])
        
        # Should be available immediately
        result = await cache_manager.get_search_results("test")
        assert result is not None
        
        # Wait for TTL to expire
        await asyncio.sleep(1.5)
        
        # Should be expired now
        result = await cache_manager.get_search_results("test")
        assert result is None
    
    # Concurrent Access Tests
    
    @pytest.mark.asyncio
    async def test_concurrent_access(self, cache_manager):
        """Test that concurrent cache operations are thread-safe"""
        async def set_and_get(user_id: int):
            settings = {"user_id": user_id, "data": f"test_{user_id}"}
            await cache_manager.set_user_settings(user_id, settings)
            result = await cache_manager.get_user_settings(user_id)
            return result
        
        # Run multiple concurrent operations
        tasks = [set_and_get(i) for i in range(100)]
        results = await asyncio.gather(*tasks)
        
        # All operations should succeed
        assert len(results) == 100
        for i, result in enumerate(results):
            assert result is not None
            assert result["user_id"] == i
    
    # Edge Cases
    
    @pytest.mark.asyncio
    async def test_empty_search_results(self, cache_manager):
        """Test caching empty search results"""
        await cache_manager.set_search_results("no results", [])
        result = await cache_manager.get_search_results("no results")
        
        assert result is not None
        assert len(result) == 0
    
    @pytest.mark.asyncio
    async def test_large_cache_entry(self, cache_manager):
        """Test caching large data structures"""
        large_results = [{"file_id": str(i), "data": "x" * 1000} for i in range(50)]
        
        await cache_manager.set_search_results("large query", large_results)
        result = await cache_manager.get_search_results("large query")
        
        assert result is not None
        assert len(result) == 50
    
    @pytest.mark.asyncio
    async def test_special_characters_in_keys(self, cache_manager):
        """Test cache keys with special characters"""
        special_query = "test:query*with[special]chars"
        results = [{"id": "1"}]
        
        await cache_manager.set_search_results(special_query, results)
        result = await cache_manager.get_search_results(special_query)
        
        assert result is not None
        assert len(result) == 1


class TestGlobalCacheManager:
    """Test suite for global cache manager singleton"""
    
    def test_get_cache_manager_singleton(self):
        """Test that get_cache_manager returns the same instance"""
        manager1 = get_cache_manager()
        manager2 = get_cache_manager()
        
        assert manager1 is manager2
    
    @pytest.mark.asyncio
    async def test_global_cache_manager_persistence(self):
        """Test that global cache manager persists data across calls"""
        manager1 = get_cache_manager()
        await manager1.set_user_settings(123, {"test": "data"})
        
        manager2 = get_cache_manager()
        result = await manager2.get_user_settings(123)
        
        assert result is not None
        assert result["test"] == "data"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
