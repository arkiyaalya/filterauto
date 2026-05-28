"""
Simple validation script for cache system

This script performs basic validation of the cache system without requiring pytest.
Run with: python validate_cache.py
"""

import asyncio
import sys
from cache import CacheManager, get_cache_manager


async def validate_cache_system():
    """Run basic validation tests on the cache system"""
    
    print("=" * 60)
    print("Cache System Validation")
    print("=" * 60)
    
    cache = CacheManager()
    passed = 0
    failed = 0
    
    # Test 1: Search cache set and get
    print("\n[Test 1] Search cache set and get...")
    try:
        await cache.set_search_results("test query", [{"id": "1", "name": "test.mp4"}])
        result = await cache.get_search_results("test query")
        assert result is not None
        assert len(result) == 1
        assert result[0]["id"] == "1"
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 2: Cache miss
    print("\n[Test 2] Cache miss for non-existent key...")
    try:
        result = await cache.get_search_results("nonexistent")
        assert result is None
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 3: User settings cache
    print("\n[Test 3] User settings cache...")
    try:
        await cache.set_user_settings(12345, {"language": "en", "notifications": True})
        result = await cache.get_user_settings(12345)
        assert result is not None
        assert result["language"] == "en"
        assert result["notifications"] is True
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 4: Group settings cache
    print("\n[Test 4] Group settings cache...")
    try:
        await cache.set_group_settings(-100123456, {"welcome": "Hello!", "auto_delete": 300})
        result = await cache.get_group_settings(-100123456)
        assert result is not None
        assert result["welcome"] == "Hello!"
        assert result["auto_delete"] == 300
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 5: File metadata cache
    print("\n[Test 5] File metadata cache...")
    try:
        await cache.set_file_metadata("file123", {"name": "movie.mp4", "size": 1024000})
        result = await cache.get_file_metadata("file123")
        assert result is not None
        assert result["name"] == "movie.mp4"
        assert result["size"] == 1024000
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 6: Cache invalidation with exact pattern
    print("\n[Test 6] Cache invalidation with exact pattern...")
    try:
        await cache.set_user_settings(111, {"test": "data1"})
        await cache.set_user_settings(222, {"test": "data2"})
        count = await cache.invalidate("user_settings:111")
        assert count == 1
        assert await cache.get_user_settings(111) is None
        assert await cache.get_user_settings(222) is not None
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 7: Cache invalidation with wildcard
    print("\n[Test 7] Cache invalidation with wildcard...")
    try:
        await cache.set_search_results("movie", [{"id": "1"}])
        await cache.set_search_results("film", [{"id": "2"}])
        count = await cache.invalidate("search:*")
        assert count >= 2  # At least the two we just added
        assert await cache.get_search_results("movie") is None
        assert await cache.get_search_results("film") is None
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 8: Statistics tracking
    print("\n[Test 8] Statistics tracking...")
    try:
        # Reset stats first
        cache.reset_stats()
        
        # Perform operations
        await cache.set_search_results("stats test", [{"id": "1"}])
        await cache.get_search_results("stats test")  # Hit
        await cache.get_search_results("nonexistent")  # Miss
        
        stats = cache.get_stats()
        assert stats['search']['hits'] == 1
        assert stats['search']['misses'] == 1
        assert stats['search']['requests'] == 2
        assert stats['search']['hit_rate'] == 50.0
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 9: Clear all caches
    print("\n[Test 9] Clear all caches...")
    try:
        await cache.set_search_results("clear test", [{"id": "1"}])
        await cache.set_user_settings(999, {"test": "data"})
        await cache.clear_all()
        assert await cache.get_search_results("clear test") is None
        assert await cache.get_user_settings(999) is None
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 10: Cache info
    print("\n[Test 10] Cache info...")
    try:
        info = cache.get_cache_info()
        assert 'search_cache' in info
        assert 'user_settings_cache' in info
        assert 'group_settings_cache' in info
        assert 'file_metadata_cache' in info
        assert info['search_cache']['maxsize'] == 1000
        assert info['search_cache']['ttl'] == 300
        assert info['user_settings_cache']['ttl'] == 600
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 11: Global singleton
    print("\n[Test 11] Global singleton pattern...")
    try:
        manager1 = get_cache_manager()
        manager2 = get_cache_manager()
        assert manager1 is manager2
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 12: Pagination support
    print("\n[Test 12] Pagination support...")
    try:
        await cache.set_search_results("page test", [{"id": "1"}], offset=0, limit=50)
        await cache.set_search_results("page test", [{"id": "2"}], offset=50, limit=50)
        
        page1 = await cache.get_search_results("page test", offset=0, limit=50)
        page2 = await cache.get_search_results("page test", offset=50, limit=50)
        
        assert page1[0]["id"] == "1"
        assert page2[0]["id"] == "2"
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 13: File invalidation
    print("\n[Test 13] File-specific invalidation...")
    try:
        file_id = "test_file_123"
        await cache.set_file_metadata(file_id, {"name": "test.mp4"})
        await cache.set_search_results("file search", [{"file_id": file_id}])
        
        await cache.invalidate_file(file_id)
        
        assert await cache.get_file_metadata(file_id) is None
        assert await cache.get_search_results("file search") is None
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 14: Empty results caching
    print("\n[Test 14] Empty results caching...")
    try:
        await cache.set_search_results("empty query", [])
        result = await cache.get_search_results("empty query")
        assert result is not None
        assert len(result) == 0
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Test 15: TTL expiration
    print("\n[Test 15] TTL expiration (short TTL test)...")
    try:
        import cachetools
        # Create a cache with very short TTL for testing
        test_cache = cachetools.TTLCache(maxsize=10, ttl=1)
        cache.search_cache = test_cache
        
        await cache.set_search_results("ttl test", [{"id": "1"}])
        result1 = await cache.get_search_results("ttl test")
        assert result1 is not None
        
        # Wait for TTL to expire
        await asyncio.sleep(1.5)
        
        result2 = await cache.get_search_results("ttl test")
        assert result2 is None
        print("✅ PASSED")
        passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    print(f"Total Tests: {passed + failed}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed / (passed + failed) * 100):.1f}%")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 All tests passed! Cache system is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(validate_cache_system())
    sys.exit(exit_code)
