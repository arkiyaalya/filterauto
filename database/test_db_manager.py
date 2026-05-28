"""
Unit tests for DatabaseManager

Tests the database connection validation functionality.
"""

import asyncio
import pytest
from unittest.mock import Mock, patch, AsyncMock
from database.db_manager import DatabaseManager, ConnectionStatus


class TestDatabaseConnectionValidation:
    """Test suite for database connection validation"""
    
    @pytest.mark.asyncio
    async def test_validate_connection_success(self):
        """Test successful connection validation"""
        manager = DatabaseManager()
        
        # Mock a successful connection
        with patch('database.db_manager.AsyncIOMotorClient') as mock_client:
            mock_instance = Mock()
            mock_instance.admin.command = AsyncMock(return_value={'ok': 1})
            mock_instance.list_database_names = AsyncMock(return_value=['test_db'])
            mock_instance.close = Mock()
            mock_client.return_value = mock_instance
            
            success, message = await manager.validate_connection("mongodb://localhost:27017")
            
            assert success is True
            assert "successful" in message.lower()
            mock_instance.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_validate_connection_timeout(self):
        """Test connection validation timeout"""
        manager = DatabaseManager()
        
        # Mock a timeout scenario
        with patch('database.db_manager.AsyncIOMotorClient') as mock_client:
            mock_instance = Mock()
            
            async def slow_command(*args, **kwargs):
                await asyncio.sleep(15)  # Longer than 10-second timeout
            
            mock_instance.admin.command = slow_command
            mock_instance.close = Mock()
            mock_client.return_value = mock_instance
            
            success, message = await manager.validate_connection("mongodb://localhost:27017")
            
            assert success is False
            assert "timeout" in message.lower()
            mock_instance.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_validate_connection_no_permissions(self):
        """Test connection validation with no database permissions"""
        manager = DatabaseManager()
        
        # Mock a connection with no accessible databases
        with patch('database.db_manager.AsyncIOMotorClient') as mock_client:
            mock_instance = Mock()
            mock_instance.admin.command = AsyncMock(return_value={'ok': 1})
            mock_instance.list_database_names = AsyncMock(return_value=[])
            mock_instance.close = Mock()
            mock_client.return_value = mock_instance
            
            success, message = await manager.validate_connection("mongodb://localhost:27017")
            
            assert success is False
            assert "permissions" in message.lower()
            mock_instance.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_validate_connection_invalid_uri(self):
        """Test connection validation with invalid URI"""
        manager = DatabaseManager()
        
        # Mock an invalid URI scenario
        with patch('database.db_manager.AsyncIOMotorClient') as mock_client:
            mock_client.side_effect = Exception("Invalid URI format")
            
            success, message = await manager.validate_connection("invalid://uri")
            
            assert success is False
            assert "invalid" in message.lower() or "error" in message.lower()
    
    @pytest.mark.asyncio
    async def test_validate_connection_network_error(self):
        """Test connection validation with network error"""
        manager = DatabaseManager()
        
        # Mock a network error
        with patch('database.db_manager.AsyncIOMotorClient') as mock_client:
            mock_instance = Mock()
            mock_instance.admin.command = AsyncMock(side_effect=Exception("Network unreachable"))
            mock_instance.close = Mock()
            mock_client.return_value = mock_instance
            
            success, message = await manager.validate_connection("mongodb://unreachable:27017")
            
            assert success is False
            assert "failed" in message.lower()
            mock_instance.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_add_database_with_validation(self):
        """Test adding a database with validation"""
        manager = DatabaseManager()
        
        # Mock successful validation and connection
        with patch('database.db_manager.AsyncIOMotorClient') as mock_client:
            mock_instance = Mock()
            mock_instance.admin.command = AsyncMock(return_value={'ok': 1})
            mock_instance.list_database_names = AsyncMock(return_value=['test_db'])
            mock_instance.close = Mock()
            mock_client.return_value = mock_instance
            
            with patch.object(manager, 'save_config', new_callable=AsyncMock):
                success, message = await manager.add_database("test_db", "mongodb://localhost:27017")
                
                assert success is True
                assert "added successfully" in message.lower()
                
                # Verify connection was added to pool
                conn = manager.pool.get_connection("test_db")
                assert conn is not None
                assert conn.status == ConnectionStatus.ACTIVE
    
    @pytest.mark.asyncio
    async def test_add_database_validation_failure(self):
        """Test adding a database with validation failure"""
        manager = DatabaseManager()
        
        # Mock failed validation
        with patch('database.db_manager.AsyncIOMotorClient') as mock_client:
            mock_instance = Mock()
            mock_instance.admin.command = AsyncMock(side_effect=Exception("Connection refused"))
            mock_instance.close = Mock()
            mock_client.return_value = mock_instance
            
            success, message = await manager.add_database("test_db", "mongodb://invalid:27017")
            
            assert success is False
            assert "failed" in message.lower()
            
            # Verify connection was not added to pool
            conn = manager.pool.get_connection("test_db")
            assert conn is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
