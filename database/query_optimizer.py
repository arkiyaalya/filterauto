# Modified by @Shadowedtomb and @Hail_Arka
# Query Optimizer Module for Bot Optimization Enhancement

import asyncio
import logging
from typing import List, Dict, Any, Tuple, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import OperationFailure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QueryOptimizer:
    """
    Query optimizer for efficient database operations.
    
    Responsibilities:
    - Create and manage database indexes
    - Execute parallel queries across multiple databases
    - Implement result limiting and field projection
    - Optimize query patterns for performance
    """
    
    def __init__(self, db_manager=None):
        """
        Initialize QueryOptimizer.
        
        Args:
            db_manager: Optional DatabaseManager instance for accessing connection pool
        """
        self.db_manager = db_manager
        self.default_limit = 50  # Maximum results per database query
        self.default_projection = {
            'file_id': 1,
            'file_name': 1,
            'file_size': 1,
            'caption': 1,
            '_id': 0  # Exclude MongoDB's internal _id field
        }
    
    async def create_indexes(
        self,
        client: AsyncIOMotorClient,
        db_name: str,
        collection_name: str
    ) -> None:
        """
        Create optimized indexes on a database collection.
        
        Creates the following indexes:
        - Single-field index on file_name
        - Compound index on (file_name, file_size)
        - Single-field index on caption
        
        Args:
            client: AsyncIOMotorClient instance
            db_name: Name of the database
            collection_name: Name of the collection
            
        Requirements: 6.1, 6.2
        """
        try:
            db: AsyncIOMotorDatabase = client[db_name]
            collection = db[collection_name]
            
            # Create single-field index on file_name
            await collection.create_index(
                [("file_name", 1)],
                background=True,
                name="idx_file_name"
            )
            logger.info(f"Created index on file_name for {db_name}.{collection_name}")
            
            # Create compound index on (file_name, file_size)
            await collection.create_index(
                [("file_name", 1), ("file_size", 1)],
                background=True,
                name="idx_file_name_size"
            )
            logger.info(f"Created compound index on (file_name, file_size) for {db_name}.{collection_name}")
            
            # Create single-field index on caption
            await collection.create_index(
                [("caption", 1)],
                background=True,
                name="idx_caption"
            )
            logger.info(f"Created index on caption for {db_name}.{collection_name}")
            
        except OperationFailure as e:
            logger.error(f"Failed to create indexes for {db_name}.{collection_name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error creating indexes for {db_name}.{collection_name}: {e}")
    
    async def parallel_query(
        self,
        clients: List[AsyncIOMotorClient],
        db_name: str,
        collection_name: str,
        filter_dict: Dict[str, Any],
        limit: int = 50,
        projection: Optional[Dict[str, int]] = None,
        skip: int = 0,
        sort_field: Optional[str] = None,
        sort_order: int = -1
    ) -> List[Dict[str, Any]]:
        """
        Execute query in parallel across multiple databases.
        
        Uses asyncio.gather() to query all databases simultaneously,
        then merges and returns the combined results.
        
        Args:
            clients: List of AsyncIOMotorClient instances
            db_name: Name of the database
            collection_name: Name of the collection
            filter_dict: MongoDB filter criteria
            limit: Maximum results per database (default: 50)
            projection: Fields to include in results (default: file_id, file_name, file_size, caption)
            skip: Number of documents to skip
            sort_field: Field to sort by (default: None for natural order)
            sort_order: Sort order (1 for ascending, -1 for descending)
            
        Returns:
            Combined list of documents from all databases
            
        Requirements: 2.5, 6.3, 6.4, 6.5
        """
        if not clients:
            logger.warning("No database clients provided for parallel query")
            return []
        
        # Use default projection if none provided
        if projection is None:
            projection = self.default_projection
        
        # Ensure limit doesn't exceed maximum
        limit = min(limit, self.default_limit)
        
        # Create query tasks for each database
        tasks = []
        for client in clients:
            task = self._query_single_database(
                client=client,
                db_name=db_name,
                collection_name=collection_name,
                filter_dict=filter_dict,
                limit=limit,
                projection=projection,
                skip=skip,
                sort_field=sort_field,
                sort_order=sort_order
            )
            tasks.append(task)
        
        # Execute all queries in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Merge results and handle exceptions
        merged_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Query failed for database client {i}: {result}")
            elif isinstance(result, list):
                merged_results.extend(result)
            else:
                logger.warning(f"Unexpected result type from database client {i}: {type(result)}")
        
        return merged_results
    
    async def _query_single_database(
        self,
        client: AsyncIOMotorClient,
        db_name: str,
        collection_name: str,
        filter_dict: Dict[str, Any],
        limit: int,
        projection: Dict[str, int],
        skip: int,
        sort_field: Optional[str],
        sort_order: int
    ) -> List[Dict[str, Any]]:
        """
        Execute query on a single database.
        
        Internal method used by parallel_query to query individual databases.
        
        Args:
            client: AsyncIOMotorClient instance
            db_name: Name of the database
            collection_name: Name of the collection
            filter_dict: MongoDB filter criteria
            limit: Maximum results
            projection: Fields to include
            skip: Number of documents to skip
            sort_field: Field to sort by
            sort_order: Sort order
            
        Returns:
            List of documents from this database
        """
        try:
            db: AsyncIOMotorDatabase = client[db_name]
            collection = db[collection_name]
            
            # Build cursor with filter and projection
            cursor = collection.find(filter_dict, projection)
            
            # Apply sorting
            if sort_field:
                cursor = cursor.sort(sort_field, sort_order)
            else:
                # Use natural order for faster queries
                cursor = cursor.sort('$natural', sort_order)
            
            # Apply skip and limit
            cursor = cursor.skip(skip).limit(limit)
            
            # Execute query and convert to list
            results = await cursor.to_list(length=limit)
            
            return results
            
        except Exception as e:
            logger.error(f"Error querying database {db_name}.{collection_name}: {e}")
            # Return exception to be handled by parallel_query
            raise
    
    async def search_files(
        self,
        clients: List[AsyncIOMotorClient],
        db_name: str,
        collection_name: str,
        query: str,
        offset: int = 0,
        limit: int = 50,
        use_caption_filter: bool = False
    ) -> Tuple[List[Dict[str, Any]], int, int]:
        """
        Execute optimized search across all databases with pagination.
        
        Args:
            clients: List of AsyncIOMotorClient instances
            db_name: Name of the database
            collection_name: Name of the collection
            query: Search query string
            offset: Starting offset for pagination
            limit: Maximum results per database
            use_caption_filter: Whether to search in caption field as well
            
        Returns:
            Tuple of (files, next_offset, total_results)
            
        Requirements: 6.3, 6.4, 6.6
        """
        import re
        
        # Build regex pattern from query
        query = query.strip()
        if not query:
            raw_pattern = '.'
        elif ' ' not in query:
            raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
        else:
            raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')
        
        try:
            regex = re.compile(raw_pattern, flags=re.IGNORECASE)
        except re.error:
            logger.error(f"Invalid regex pattern: {raw_pattern}")
            regex = query
        
        # Build filter criteria
        filter_dict = {'file_name': regex}
        if use_caption_filter:
            filter_dict = {'$or': [{'file_name': regex}, {'caption': regex}]}
        
        # Execute parallel query
        files = await self.parallel_query(
            clients=clients,
            db_name=db_name,
            collection_name=collection_name,
            filter_dict=filter_dict,
            limit=limit,
            skip=offset
        )
        
        # Count total results across all databases
        total_results = await self._count_total_results(
            clients=clients,
            db_name=db_name,
            collection_name=collection_name,
            filter_dict=filter_dict
        )
        
        # Calculate next offset for pagination
        next_offset = 0 if (offset + len(files)) >= total_results else (offset + len(files))
        
        return files, next_offset, total_results
    
    async def _count_total_results(
        self,
        clients: List[AsyncIOMotorClient],
        db_name: str,
        collection_name: str,
        filter_dict: Dict[str, Any]
    ) -> int:
        """
        Count total matching documents across all databases.
        
        Args:
            clients: List of AsyncIOMotorClient instances
            db_name: Name of the database
            collection_name: Name of the collection
            filter_dict: MongoDB filter criteria
            
        Returns:
            Total count of matching documents
        """
        tasks = []
        for client in clients:
            task = self._count_single_database(
                client=client,
                db_name=db_name,
                collection_name=collection_name,
                filter_dict=filter_dict
            )
            tasks.append(task)
        
        # Execute all count operations in parallel
        counts = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Sum up counts, handling exceptions
        total = 0
        for i, count in enumerate(counts):
            if isinstance(count, Exception):
                logger.error(f"Count failed for database client {i}: {count}")
            elif isinstance(count, int):
                total += count
        
        return total
    
    async def _count_single_database(
        self,
        client: AsyncIOMotorClient,
        db_name: str,
        collection_name: str,
        filter_dict: Dict[str, Any]
    ) -> int:
        """
        Count documents in a single database.
        
        Args:
            client: AsyncIOMotorClient instance
            db_name: Name of the database
            collection_name: Name of the collection
            filter_dict: MongoDB filter criteria
            
        Returns:
            Count of matching documents
        """
        try:
            db: AsyncIOMotorDatabase = client[db_name]
            collection = db[collection_name]
            count = await collection.count_documents(filter_dict)
            return count
        except Exception as e:
            logger.error(f"Error counting documents in {db_name}.{collection_name}: {e}")
            raise
