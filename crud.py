from sqlalchemy.orm import Session
import models, schemas

# Fetch all records
def get_errors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ErrorLog).all()

# Create a new record
def create_error(db: Session, error: schemas.ErrorCreate):
    db_error = models.ErrorLog(
        error_code=error.error_code, 
        description=error.description
    )
    db.add(db_error)
    db.commit()
    db.refresh(db_error)
    return db_error

# Update an existing record
def update_error(db: Session, error_id: int, updated_data: schemas.ErrorCreate):
    # Find the record by its primary key (ID)
    db_error = db.query(models.ErrorLog).filter(models.ErrorLog.id == error_id).first()
    
    if db_error:
        # Update fields with new data
        db_error.error_code = updated_data.error_code
        db_error.description = updated_data.description
        db.commit()      # Save changes to SQL Server
        db.refresh(db_error)
    return db_error

# Delete a record
def delete_error(db: Session, error_id: int):
    db_error = db.query(models.ErrorLog).filter(models.ErrorLog.id == error_id).first()
    if db_error:
        db.delete(db_error)
        db.commit()
        return True
    return False