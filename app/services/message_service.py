from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.message import Message
from app.utils.logger import logger
from app.utils.exceptions import DatabaseError, ValidationError


class MessageService:
    """Service layer for message management operations"""
    
    @staticmethod
    def create_message(data: Dict[str, Any]) -> Message:
        """Create a new message from contact form"""
        try:
            # Validate required fields
            if not data.get('name') or len(data['name'].strip()) < 2:
                raise ValidationError("Name must be at least 2 characters long")
            
            if not data.get('email') or not MessageService._validate_email(data['email']):
                raise ValidationError("Please provide a valid email address")
            
            if not data.get('message') or len(data['message'].strip()) < 10:
                raise ValidationError("Message must be at least 10 characters long")
            
            message = Message(
                name=data['name'].strip(),
                email=data['email'].strip(),
                subject=data.get('subject', 'No Subject').strip(),
                message=data['message'].strip(),
                ip_address=data.get('ip_address'),
                user_agent=data.get('user_agent')
            )
            
            db.session.add(message)
            db.session.commit()
            
            logger.info(f"New message from {message.name} ({message.email})")
            return message
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error creating message: {str(e)}")
            raise DatabaseError("Failed to save message")
        except Exception as e:
            logger.error(f"Error creating message: {str(e)}")
            raise
    
    @staticmethod
    def get_all_messages(status: str = 'all') -> List[Message]:
        """Get all messages with optional status filter"""
        try:
            query = Message.query
            if status != 'all':
                query = query.filter_by(status=status)
            return query.order_by(Message.created_at.desc()).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching messages: {str(e)}")
            raise DatabaseError("Failed to fetch messages")
    
    @staticmethod
    def get_message_by_id(message_id: int) -> Optional[Message]:
        """Get a single message by ID"""
        try:
            return Message.query.get(message_id)
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching message {message_id}: {str(e)}")
            raise DatabaseError("Failed to fetch message")
    
    @staticmethod
    def mark_as_read(message_id: int) -> bool:
        """Mark a message as read"""
        try:
            message = Message.query.get(message_id)
            if not message:
                raise ValidationError("Message not found")
            
            message.status = 'read'
            message.read_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Marked message {message_id} as read")
            return True
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error marking message as read: {str(e)}")
            raise DatabaseError("Failed to mark message as read")
        except Exception as e:
            logger.error(f"Error marking message as read: {str(e)}")
            raise
    
    @staticmethod
    def mark_as_unread(message_id: int) -> bool:
        """Mark a message as unread"""
        try:
            message = Message.query.get(message_id)
            if not message:
                raise ValidationError("Message not found")
            
            message.status = 'unread'
            message.read_at = None
            db.session.commit()
            
            logger.info(f"Marked message {message_id} as unread")
            return True
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error marking message as unread: {str(e)}")
            raise DatabaseError("Failed to mark message as unread")
        except Exception as e:
            logger.error(f"Error marking message as unread: {str(e)}")
            raise
    
    @staticmethod
    def delete_message(message_id: int) -> bool:
        """Delete a message"""
        try:
            message = Message.query.get(message_id)
            if not message:
                raise ValidationError("Message not found")
            
            db.session.delete(message)
            db.session.commit()
            
            logger.info(f"Deleted message from {message.name}")
            return True
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error deleting message: {str(e)}")
            raise DatabaseError("Failed to delete message")
        except Exception as e:
            logger.error(f"Error deleting message: {str(e)}")
            raise
    
    @staticmethod
    def get_unread_count() -> int:
        """Get count of unread messages"""
        try:
            return Message.query.filter_by(status='unread').count()
        except SQLAlchemyError as e:
            logger.error(f"Database error getting unread count: {str(e)}")
            return 0
    
    @staticmethod
    def get_recent_messages(limit: int = 5) -> List[Message]:
        """Get recent messages"""
        try:
            return Message.query.order_by(
                Message.created_at.desc()
            ).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error getting recent messages: {str(e)}")
            return []
    
    @staticmethod
    def get_message_stats(days: int = 30) -> Dict[str, Any]:
        """Get message statistics for the last N days"""
        try:
            since_date = datetime.utcnow() - timedelta(days=days)
            
            total = Message.query.filter(Message.created_at >= since_date).count()
            unread = Message.query.filter(
                Message.created_at >= since_date,
                Message.status == 'unread'
            ).count()
            
            # Get daily counts for the last week
            daily_stats = []
            for i in range(7):
                date = datetime.utcnow() - timedelta(days=i)
                count = Message.query.filter(
                    db.func.date(Message.created_at) == date.date()
                ).count()
                daily_stats.append({
                    'date': date.date().isoformat(),
                    'count': count
                })
            
            return {
                'total': total,
                'unread': unread,
                'read': total - unread,
                'daily_stats': daily_stats
            }
        except SQLAlchemyError as e:
            logger.error(f"Database error getting message stats: {str(e)}")
            raise DatabaseError("Failed to get message statistics")
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def export_messages(format: str = 'json') -> str:
        """Export messages in specified format"""
        try:
            messages = Message.query.order_by(Message.created_at.desc()).all()
            
            if format.lower() == 'json':
                import json
                return json.dumps([msg.to_dict() for msg in messages], indent=2)
            elif format.lower() == 'csv':
                import csv
                import io
                
                output = io.StringIO()
                writer = csv.writer(output)
                
                # Header
                writer.writerow(['ID', 'Name', 'Email', 'Subject', 'Message', 'Status', 'Created At'])
                
                # Data
                for msg in messages:
                    writer.writerow([
                        msg.id,
                        msg.name,
                        msg.email,
                        msg.subject,
                        msg.message,
                        msg.status,
                        msg.created_at.isoformat() if msg.created_at else ''
                    ])
                
                return output.getvalue()
            else:
                raise ValidationError("Unsupported export format")
                
        except Exception as e:
            logger.error(f"Error exporting messages: {str(e)}")
            raise DatabaseError("Failed to export messages")
