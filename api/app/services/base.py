"""
Base service class with common functionality.
"""

from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from app.db.database import Base
from app.schemas import PaginationQuery, PaginationMeta
import math

ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    """Base service class with CRUD operations."""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_direction: str = "asc"
    ) -> List[ModelType]:
        """Get multiple records with filtering and ordering."""
        query = db.query(self.model)
        
        # Apply filters
        if filters:
            filter_conditions = []
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if isinstance(value, list):
                        filter_conditions.append(getattr(self.model, field).in_(value))
                    else:
                        filter_conditions.append(getattr(self.model, field) == value)
            if filter_conditions:
                query = query.filter(and_(*filter_conditions))
        
        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            if order_direction.lower() == "desc":
                query = query.order_by(desc(getattr(self.model, order_by)))
            else:
                query = query.order_by(asc(getattr(self.model, order_by)))
        
        return query.offset(skip).limit(limit).all()
    
    def get_paginated(
        self,
        db: Session,
        pagination: PaginationQuery,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_direction: str = "asc"
    ) -> tuple[List[ModelType], PaginationMeta]:
        """Get paginated records with metadata."""
        # Build base query
        query = db.query(self.model)
        
        # Apply filters
        if filters:
            filter_conditions = []
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if isinstance(value, list):
                        filter_conditions.append(getattr(self.model, field).in_(value))
                    else:
                        filter_conditions.append(getattr(self.model, field) == value)
            if filter_conditions:
                query = query.filter(and_(*filter_conditions))
        
        # Get total count
        total_count = query.count()
        
        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            if order_direction.lower() == "desc":
                query = query.order_by(desc(getattr(self.model, order_by)))
            else:
                query = query.order_by(asc(getattr(self.model, order_by)))
        
        # Apply pagination
        offset = (pagination.page - 1) * pagination.page_size
        items = query.offset(offset).limit(pagination.page_size).all()
        
        # Calculate pagination metadata
        total_pages = math.ceil(total_count / pagination.page_size)
        has_next = pagination.page < total_pages
        has_prev = pagination.page > 1
        
        meta = PaginationMeta(
            page=pagination.page,
            page_size=pagination.page_size,
            total_count=total_count,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )
        
        return items, meta
    
    def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filters."""
        query = db.query(self.model)
        
        if filters:
            filter_conditions = []
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if isinstance(value, list):
                        filter_conditions.append(getattr(self.model, field).in_(value))
                    else:
                        filter_conditions.append(getattr(self.model, field) == value)
            if filter_conditions:
                query = query.filter(and_(*filter_conditions))
        
        return query.count()
    
    def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        """Update an existing record."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> ModelType:
        """Delete a record by ID."""
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
