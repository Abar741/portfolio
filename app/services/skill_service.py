from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.skill import Skill
from app.utils.logger import logger
from app.utils.exceptions import DatabaseError, ValidationError


class SkillService:
    """Service layer for skill management operations"""
    
    @staticmethod
    def get_all_skills() -> List[Skill]:
        """Get all skills ordered by percentage"""
        try:
            return Skill.query.order_by(Skill.percentage.desc()).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching skills: {str(e)}")
            raise DatabaseError("Failed to fetch skills")
    
    @staticmethod
    def get_skill_by_id(skill_id: int) -> Optional[Skill]:
        """Get a single skill by ID"""
        try:
            return Skill.query.get(skill_id)
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching skill {skill_id}: {str(e)}")
            raise DatabaseError("Failed to fetch skill")
    
    @staticmethod
    def create_skill(data: Dict[str, Any]) -> Skill:
        """Create a new skill"""
        try:
            # Validate required fields
            if not data.get('name') or len(data['name'].strip()) < 2:
                raise ValidationError("Skill name must be at least 2 characters long")
            
            if not data.get('percentage') or not isinstance(data['percentage'], (int, float)):
                raise ValidationError("Valid percentage is required")
            
            percentage = float(data['percentage'])
            if percentage < 0 or percentage > 100:
                raise ValidationError("Percentage must be between 0 and 100")
            
            # Check for duplicate skill name
            existing_skill = Skill.query.filter_by(name=data['name'].strip()).first()
            if existing_skill:
                raise ValidationError("Skill with this name already exists")
            
            skill = Skill(
                name=data['name'].strip(),
                percentage=percentage,
                category=data.get('category', 'Technical'),
                description=data.get('description', '')
            )
            
            db.session.add(skill)
            db.session.commit()
            
            logger.info(f"Created new skill: {skill.name}")
            return skill
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error creating skill: {str(e)}")
            raise DatabaseError("Failed to create skill")
        except Exception as e:
            logger.error(f"Error creating skill: {str(e)}")
            raise
    
    @staticmethod
    def update_skill(skill_id: int, data: Dict[str, Any]) -> Skill:
        """Update an existing skill"""
        try:
            skill = Skill.query.get(skill_id)
            if not skill:
                raise ValidationError("Skill not found")
            
            # Update fields
            if 'name' in data:
                if len(data['name'].strip()) < 2:
                    raise ValidationError("Skill name must be at least 2 characters long")
                
                # Check for duplicate name (excluding current skill)
                existing_skill = Skill.query.filter(
                    Skill.name == data['name'].strip(),
                    Skill.id != skill_id
                ).first()
                if existing_skill:
                    raise ValidationError("Skill with this name already exists")
                
                skill.name = data['name'].strip()
            
            if 'percentage' in data:
                percentage = float(data['percentage'])
                if percentage < 0 or percentage > 100:
                    raise ValidationError("Percentage must be between 0 and 100")
                skill.percentage = percentage
            
            if 'category' in data:
                skill.category = data['category']
            
            if 'description' in data:
                skill.description = data['description']
            
            db.session.commit()
            
            logger.info(f"Updated skill: {skill.name}")
            return skill
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error updating skill {skill_id}: {str(e)}")
            raise DatabaseError("Failed to update skill")
        except Exception as e:
            logger.error(f"Error updating skill {skill_id}: {str(e)}")
            raise
    
    @staticmethod
    def delete_skill(skill_id: int) -> bool:
        """Delete a skill"""
        try:
            skill = Skill.query.get(skill_id)
            if not skill:
                raise ValidationError("Skill not found")
            
            db.session.delete(skill)
            db.session.commit()
            
            logger.info(f"Deleted skill: {skill.name}")
            return True
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error deleting skill {skill_id}: {str(e)}")
            raise DatabaseError("Failed to delete skill")
        except Exception as e:
            logger.error(f"Error deleting skill {skill_id}: {str(e)}")
            raise
    
    @staticmethod
    def reorder_skills(skill_ids: List[int]) -> bool:
        """Reorder skills based on provided ID list"""
        try:
            skills = Skill.query.filter(Skill.id.in_(skill_ids)).all()
            skill_dict = {skill.id: skill for skill in skills}
            
            for index, skill_id in enumerate(skill_ids):
                if skill_id in skill_dict:
                    # You might want to add an 'order' field to the Skill model
                    # For now, we'll just update the percentage to reflect order
                    skill_dict[skill_id].percentage = 100 - (index * 10)
            
            db.session.commit()
            
            logger.info("Reordered skills")
            return True
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error reordering skills: {str(e)}")
            raise DatabaseError("Failed to reorder skills")
        except Exception as e:
            logger.error(f"Error reordering skills: {str(e)}")
            raise
    
    @staticmethod
    def get_skills_by_category(category: str) -> List[Skill]:
        """Get skills filtered by category"""
        try:
            return Skill.query.filter_by(category=category).order_by(
                Skill.percentage.desc()
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching skills by category {category}: {str(e)}")
            raise DatabaseError("Failed to fetch skills by category")
    
    @staticmethod
    def get_skill_categories() -> List[str]:
        """Get all unique skill categories"""
        try:
            from sqlalchemy import distinct
            categories = db.session.query(distinct(Skill.category)).all()
            return [cat[0] for cat in categories if cat[0]]
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching skill categories: {str(e)}")
            return []
    
    @staticmethod
    def get_skill_stats() -> Dict[str, Any]:
        """Get skill statistics"""
        try:
            total = Skill.query.count()
            avg_percentage = db.session.query(db.func.avg(Skill.percentage)).scalar() or 0
            
            # Get top 5 skills
            top_skills = Skill.query.order_by(Skill.percentage.desc()).limit(5).all()
            
            return {
                'total': total,
                'average_percentage': round(float(avg_percentage), 1),
                'top_skills': [skill.to_dict() for skill in top_skills]
            }
        except SQLAlchemyError as e:
            logger.error(f"Database error getting skill stats: {str(e)}")
            raise DatabaseError("Failed to get skill statistics")
