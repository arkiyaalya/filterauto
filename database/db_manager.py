"""
Database Manager Module

This module provides dynamic database connection pool management for the VJ-FILTER-BOT.
It supports unlimited MongoDB connections with runtime addition/removal capabilities.
"""

import asyncio
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)


class ConfigValidationError(Exception):
    """Exception raised when configuration validation fails"""
    pass


class ConnectionStatus(Enum):
    """Enum representing the status of a database connection"""
    ACTIVE = "active"
    FAILED = "failed"
    CONNECTING = "connecting"
    DISABLED = "disabled"


@dataclass
class DatabaseConnection:
    """Represents a single MongoDB connection"""
    name: str
    uri: str
    client: Optional[AsyncIOMotorClient]
    status: ConnectionStatus
    last_check: datetime
    retry_count: int
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "uri": self.uri,
            "status": self.status.value,
            "last_check": self.last_check.isoformat(),
            "retry_count": self.retry_count,
            "error_message": self.error_message
        }


class ConnectionPool:
    """Manages multiple database connections"""
    
    def __init__(self):
        self.connections: Dict[str, DatabaseConnection] = {}
    
    def add_connection(self, connection: DatabaseConnection) -> bool:
        """Add a connection to the pool"""
        try:
            self.connections[connection.name] = connection
            logger.info(f"Added connection '{connection.name}' to pool")
            return True
        except Exception as e:
            logger.error(f"Failed to add connection '{connection.name}': {e}")
            return False
    
    def remove_connection(self, name: str) -> bool:
        """Remove a connection from the pool"""
        if name in self.connections:
            del self.connections[name]
            logger.info(f"Removed connection '{name}' from pool")
            return True
        logger.warning(f"Connection '{name}' not found in pool")
        return False
    
    def get_connection(self, name: str) -> Optional[DatabaseConnection]:
        """Get a connection by name"""
        return self.connections.get(name)
    
    def get_active_connections(self) -> List[DatabaseConnection]:
        """Get all active connections"""
        return [
            conn for conn in self.connections.values()
            if conn.status == ConnectionStatus.ACTIVE
        ]
    
    def get_all_connections(self) -> List[DatabaseConnection]:
        """Get all connections regardless of status"""
        return list(self.connections.values())


class DatabaseManager:
    """High-level database management"""
    
    def __init__(self, config_file: str = None):
        """
        Initialize the DatabaseManager
        
        Args:
            config_file: Path to the configuration file. If None, uses default location.
        """
        self.pool = ConnectionPool()
        if config_file is None:
            # Default config file location
            config_dir = os.path.join(os.getcwd(), ".kiro", "specs", "bot-optimization-enhancement")
            os.makedirs(config_dir, exist_ok=True)
            self.config_file = os.path.join(config_dir, "db_config.json")
        else:
            self.config_file = config_file
        
        self._health_check_task: Optional[asyncio.Task] = None
    
    @staticmethod
    def validate_config_format(config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate the configuration file format
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        try:
            # Check required top-level fields
            if "version" not in config:
                return False, "Missing required field: 'version'"
            
            if "databases" not in config:
                return False, "Missing required field: 'databases'"
            
            if "legacy_mode" not in config:
                return False, "Missing required field: 'legacy_mode'"
            
            # Validate version format
            version = config["version"]
            if not isinstance(version, str):
                return False, "'version' must be a string"
            
            # Validate legacy_mode
            legacy_mode = config["legacy_mode"]
            if not isinstance(legacy_mode, bool):
                return False, "'legacy_mode' must be a boolean"
            
            # Validate databases array
            databases = config["databases"]
            if not isinstance(databases, list):
                return False, "'databases' must be an array"
            
            # Validate each database entry
            for idx, db in enumerate(databases):
                if not isinstance(db, dict):
                    return False, f"Database entry {idx} must be an object"
                
                # Check required fields for each database
                required_fields = ["name", "uri", "type", "added_at", "enabled"]
                for field in required_fields:
                    if field not in db:
                        return False, f"Database entry {idx} missing required field: '{field}'"
                
                # Validate field types
                if not isinstance(db["name"], str):
                    return False, f"Database entry {idx}: 'name' must be a string"
                
                if not isinstance(db["uri"], str):
                    return False, f"Database entry {idx}: 'uri' must be a string"
                
                if not isinstance(db["type"], str):
                    return False, f"Database entry {idx}: 'type' must be a string"
                
                if not isinstance(db["added_at"], str):
                    return False, f"Database entry {idx}: 'added_at' must be a string"
                
                if not isinstance(db["enabled"], bool):
                    return False, f"Database entry {idx}: 'enabled' must be a boolean"
                
                # Validate name format (alphanumeric, underscores, hyphens)
                name = db["name"]
                if not name or not all(c.isalnum() or c in ['_', '-'] for c in name):
                    return False, f"Database entry {idx}: 'name' must contain only alphanumeric characters, underscores, or hyphens"
                
                # Validate URI format (basic check for mongodb:// prefix)
                uri = db["uri"]
                if not uri.startswith("mongodb://") and not uri.startswith("mongodb+srv://"):
                    return False, f"Database entry {idx}: 'uri' must start with 'mongodb://' or 'mongodb+srv://'"
                
                # Validate added_at is ISO format datetime
                try:
                    datetime.fromisoformat(db["added_at"])
                except ValueError:
                    return False, f"Database entry {idx}: 'added_at' must be in ISO format"
            
            return True, "Configuration format is valid"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    async def validate_connection(self, uri: str) -> Tuple[bool, str]:
        """
        Validate a database connection
        
        Tests the connection with a 10-second timeout and verifies database
        permissions and accessibility.
        
        Args:
            uri: MongoDB connection URI
            
        Returns:
            Tuple of (success: bool, error_message: str)
        """
        try:
            # Create a temporary client for validation
            client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=10000)
            
            # Test the connection with 10-second timeout
            async def test_connection():
                try:
                    # Ping the database to verify connection
                    await client.admin.command('ping')
                    
                    # List databases to verify permissions
                    db_list = await client.list_database_names()
                    
                    if not db_list:
                        return False, "No databases accessible - check permissions"
                    
                    return True, "Connection successful"
                    
                except Exception as e:
                    return False, f"Connection test failed: {str(e)}"
            
            # Execute with timeout
            try:
                success, message = await asyncio.wait_for(
                    test_connection(),
                    timeout=10.0
                )
                
                # Close the temporary client
                client.close()
                
                return success, message
                
            except asyncio.TimeoutError:
                client.close()
                return False, "Connection timeout after 10 seconds"
                
        except Exception as e:
            logger.error(f"Connection validation error: {e}")
            return False, f"Invalid URI or connection error: {str(e)}"
    
    async def add_database(self, name: str, uri: str) -> Tuple[bool, str]:
        """
        Add a new database connection
        
        Args:
            name: Unique name for the connection
            uri: MongoDB connection URI
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check if connection already exists
        if self.pool.get_connection(name):
            return False, f"Connection '{name}' already exists"
        
        # Validate the connection
        logger.info(f"Validating connection '{name}'...")
        is_valid, error_msg = await self.validate_connection(uri)
        
        if not is_valid:
            logger.error(f"Connection validation failed for '{name}': {error_msg}")
            return False, error_msg
        
        # Create the connection
        try:
            client = AsyncIOMotorClient(uri)
            connection = DatabaseConnection(
                name=name,
                uri=uri,
                client=client,
                status=ConnectionStatus.ACTIVE,
                last_check=datetime.now(),
                retry_count=0,
                error_message=None
            )
            
            # Add to pool
            if self.pool.add_connection(connection):
                # Save configuration
                await self.save_config()
                logger.info(f"Successfully added database '{name}'")
                return True, f"Database '{name}' added successfully"
            else:
                client.close()
                return False, f"Failed to add connection '{name}' to pool"
                
        except Exception as e:
            logger.error(f"Error adding database '{name}': {e}")
            return False, f"Error adding database: {str(e)}"
    
    async def remove_database(self, name: str) -> Tuple[bool, str]:
        """
        Remove a database connection
        
        Args:
            name: Name of the connection to remove
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        connection = self.pool.get_connection(name)
        
        if not connection:
            return False, f"Connection '{name}' not found"
        
        try:
            # Close the client gracefully
            if connection.client:
                connection.client.close()
                logger.info(f"Closed client for connection '{name}'")
            
            # Remove from pool
            if self.pool.remove_connection(name):
                # Save configuration
                await self.save_config()
                return True, f"Database '{name}' removed successfully"
            else:
                return False, f"Failed to remove connection '{name}'"
                
        except Exception as e:
            logger.error(f"Error removing database '{name}': {e}")
            return False, f"Error removing database: {str(e)}"
    
    async def list_databases(self) -> List[Dict[str, Any]]:
        """
        List all database connections with status
        
        Returns:
            List of dictionaries with connection information
        """
        connections = self.pool.get_all_connections()
        result = []
        
        for conn in connections:
            # Mask URI for security (show only last 4 characters)
            masked_uri = "..." + conn.uri[-4:] if len(conn.uri) > 4 else "****"
            
            result.append({
                "name": conn.name,
                "uri": masked_uri,
                "status": conn.status.value,
                "last_check": conn.last_check.isoformat(),
                "retry_count": conn.retry_count,
                "error_message": conn.error_message
            })
        
        return result
    
    async def get_active_connections(self) -> List[AsyncIOMotorClient]:
        """
        Get all active database clients for querying
        
        Returns:
            List of active Motor clients
        """
        active_conns = self.pool.get_active_connections()
        return [conn.client for conn in active_conns if conn.client is not None]
    
    async def save_config(self) -> None:
        """Save configuration to disk"""
        try:
            connections = self.pool.get_all_connections()
            
            config = {
                "version": "1.0",
                "databases": [
                    {
                        "name": conn.name,
                        "uri": conn.uri,
                        "type": "file",
                        "added_at": conn.last_check.isoformat(),
                        "enabled": conn.status != ConnectionStatus.DISABLED
                    }
                    for conn in connections
                ],
                "legacy_mode": False
            }
            
            # Write to file with restricted permissions
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Set file permissions to 0600 (owner read/write only)
            try:
                os.chmod(self.config_file, 0o600)
            except Exception as e:
                logger.warning(f"Could not set file permissions: {e}")
            
            logger.info(f"Configuration saved to {self.config_file}")
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            raise
    
    async def load_config(self) -> None:
        """Load configuration from disk"""
        try:
            if not os.path.exists(self.config_file):
                logger.info("No configuration file found, starting with empty pool")
                return
            
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            databases = config.get("databases", [])
            logger.info(f"Loading {len(databases)} database connections from config")
            
            for db_config in databases:
                name = db_config["name"]
                uri = db_config["uri"]
                enabled = db_config.get("enabled", True)
                
                if not enabled:
                    logger.info(f"Skipping disabled connection '{name}'")
                    continue
                
                try:
                    # Create client
                    client = AsyncIOMotorClient(uri)
                    
                    # Create connection object
                    connection = DatabaseConnection(
                        name=name,
                        uri=uri,
                        client=client,
                        status=ConnectionStatus.ACTIVE,
                        last_check=datetime.now(),
                        retry_count=0,
                        error_message=None
                    )
                    
                    self.pool.add_connection(connection)
                    logger.info(f"Loaded connection '{name}'")
                    
                except Exception as e:
                    logger.error(f"Failed to load connection '{name}': {e}")
                    # Add as failed connection
                    connection = DatabaseConnection(
                        name=name,
                        uri=uri,
                        client=None,
                        status=ConnectionStatus.FAILED,
                        last_check=datetime.now(),
                        retry_count=0,
                        error_message=str(e)
                    )
                    self.pool.add_connection(connection)
            
            logger.info("Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    async def health_check(self) -> None:
        """
        Background task to check connection health
        Runs every 60 seconds
        """
        while True:
            try:
                await asyncio.sleep(60)
                
                connections = self.pool.get_all_connections()
                logger.debug(f"Running health check on {len(connections)} connections")
                
                for conn in connections:
                    try:
                        if conn.client is None:
                            # Try to reconnect
                            if conn.retry_count < 5:  # Limit retries
                                logger.info(f"Attempting to reconnect '{conn.name}'")
                                is_valid, error_msg = await self.validate_connection(conn.uri)
                                
                                if is_valid:
                                    conn.client = AsyncIOMotorClient(conn.uri)
                                    conn.status = ConnectionStatus.ACTIVE
                                    conn.retry_count = 0
                                    conn.error_message = None
                                    logger.info(f"Reconnected '{conn.name}' successfully")
                                else:
                                    conn.retry_count += 1
                                    conn.error_message = error_msg
                                    logger.warning(f"Reconnection failed for '{conn.name}': {error_msg}")
                            continue
                        
                        # Ping the database
                        await asyncio.wait_for(
                            conn.client.admin.command('ping'),
                            timeout=5.0
                        )
                        
                        # Update status
                        if conn.status != ConnectionStatus.ACTIVE:
                            logger.info(f"Connection '{conn.name}' is now active")
                        
                        conn.status = ConnectionStatus.ACTIVE
                        conn.last_check = datetime.now()
                        conn.retry_count = 0
                        conn.error_message = None
                        
                    except asyncio.TimeoutError:
                        logger.warning(f"Health check timeout for '{conn.name}'")
                        conn.status = ConnectionStatus.FAILED
                        conn.error_message = "Health check timeout"
                        conn.retry_count += 1
                        
                    except Exception as e:
                        logger.error(f"Health check failed for '{conn.name}': {e}")
                        conn.status = ConnectionStatus.FAILED
                        conn.error_message = str(e)
                        conn.retry_count += 1
                
            except Exception as e:
                logger.error(f"Error in health check loop: {e}")
    
    def start_health_check(self) -> None:
        """Start the health check background task"""
        if self._health_check_task is None or self._health_check_task.done():
            self._health_check_task = asyncio.create_task(self.health_check())
            logger.info("Health check task started")
    
    def stop_health_check(self) -> None:
        """Stop the health check background task"""
        if self._health_check_task and not self._health_check_task.done():
            self._health_check_task.cancel()
            logger.info("Health check task stopped")
