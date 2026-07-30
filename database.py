"""
database.py

Database manager for Residency-New-Programs project.

Purpose:
- Create and manage SQLite database
- Store newly accredited residency programs
  (Internal Medicine, Family Medicine, Pediatrics)
  from 2025-2026
- Provide CRUD operations
- Prevent duplicate programs

Database:
SQLite + SQLAlchemy

Author:
Residency-New-Programs Project
"""

import os
from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Text,
    UniqueConstraint
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_FOLDER = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_FILE = os.path.join(
    DATABASE_FOLDER,
    "residency.db"
)


# Create database folder if missing

os.makedirs(
    DATABASE_FOLDER,
    exist_ok=True
)


DATABASE_URL = (
    f"sqlite:///{DATABASE_FILE}"
)


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()



# ==========================================================
# DATABASE MODEL
# ==========================================================


class ResidencyProgram(Base):

    """
    Main residency program table.

    Tracks only:
    - Internal Medicine
    - Family Medicine
    - Pediatrics

    Newly accredited:
    - 2025
    - 2026
    """


    __tablename__ = "programs"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    specialty = Column(
        String(50),
        nullable=False
    )


    program_name = Column(
        String(255),
        nullable=False
    )


    institution = Column(
        String(255)
    )


    city = Column(
        String(100)
    )


    state = Column(
        String(50)
    )


    region = Column(
        String(50)
    )


    # Accreditation information

    accreditation_year = Column(
        Integer
    )


    accreditation_date = Column(
        Date
    )


    accreditation_status = Column(
        String(100),
        default="Initial Accreditation"
    )


    first_match_cycle = Column(
        String(50)
    )


    residency_start = Column(
        String(50)
    )


    # Program characteristics


    program_type = Column(
        String(100)
    )


    hospital_beds = Column(
        Integer
    )


    teaching_hospital = Column(
        Boolean,
        default=False
    )


    # IMG information


    j1_sponsorship = Column(
        String(50)
    )


    h1b_sponsorship = Column(
        String(50)
    )


    img_friendly = Column(
        String(50)
    )


    ecfmg_required = Column(
        Boolean,
        default=True
    )


    usce_required = Column(
        String(50)
    )


    step2_requirement = Column(
        String(100)
    )


    # Links


    website = Column(
        Text
    )


    freida_url = Column(
        Text
    )


    eras_url = Column(
        Text
    )


    # Contacts


    program_director = Column(
        String(255)
    )


    coordinator = Column(
        String(255)
    )


    coordinator_email = Column(
        String(255)
    )


    # Notes


    notes = Column(
        Text
    )


    last_updated = Column(
        DateTime,
        default=datetime.utcnow
    )


    __table_args__ = (

        UniqueConstraint(
            "program_name",
            "specialty",
            "state",
            name="unique_program"
        ),

    )



# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================


def create_database():

    """
    Create all database tables.
    """

    Base.metadata.create_all(
        bind=engine
    )



# ==========================================================
# SESSION MANAGEMENT
# ==========================================================


def get_session():

    """
    Returns database session.

    Example:

        db = get_session()

        db.query(ResidencyProgram)

    """

    return SessionLocal()



# ==========================================================
# INSERT PROGRAM
# ==========================================================


def add_program(program_data):

    """
    Add new residency program.

    program_data example:

    {
      "specialty":"Internal Medicine",
      "program_name":"Example Hospital",
      "state":"CA"
    }

    """


    session = get_session()


    try:

        existing = session.query(
            ResidencyProgram
        ).filter_by(

            program_name=
            program_data["program_name"],

            specialty=
            program_data["specialty"],

            state=
            program_data["state"]

        ).first()



        if existing:

            return existing



        program = ResidencyProgram(
            **program_data
        )


        session.add(program)

        session.commit()

        session.refresh(program)


        return program



    except Exception as e:

        session.rollback()

        raise e



    finally:

        session.close()



# ==========================================================
# BULK INSERT
# ==========================================================


def add_programs(program_list):

    """
    Add multiple programs.

    Input:

    [
      {},
      {},
      {}
    ]

    """

    results=[]


    for program in program_list:

        result = add_program(
            program
        )

        results.append(
            result
        )


    return results



# ==========================================================
# QUERY FUNCTIONS
# ==========================================================


def get_all_programs():

    """
    Return all programs.
    """

    session=get_session()


    try:

        return session.query(
            ResidencyProgram
        ).all()


    finally:

        session.close()



def get_programs_by_specialty(
        specialty
):

    """
    Example:

    get_programs_by_specialty(
        "Internal Medicine"
    )

    """


    session=get_session()


    try:

        return session.query(
            ResidencyProgram
        ).filter_by(

            specialty=specialty

        ).all()


    finally:

        session.close()



def get_programs_by_state(
        state
):

    session=get_session()


    try:

        return session.query(
            ResidencyProgram
        ).filter_by(

            state=state

        ).all()


    finally:

        session.close()



# ==========================================================
# UPDATE PROGRAM
# ==========================================================


def update_program(
        program_id,
        updates
):

    """
    Update existing record.

    Example:

    update_program(
        1,
        {
        "j1_sponsorship":"Yes"
        }
    )

    """


    session=get_session()


    try:

        program=session.query(
            ResidencyProgram
        ).filter_by(

            id=program_id

        ).first()



        if not program:

            return None



        for key,value in updates.items():

            setattr(
                program,
                key,
                value
            )


        program.last_updated=datetime.utcnow()


        session.commit()


        return program



    finally:

        session.close()



# ==========================================================
# DELETE
# ==========================================================


def delete_program(
        program_id
):

    session=get_session()


    try:

        program=session.query(
            ResidencyProgram
        ).filter_by(
            id=program_id
        ).first()


        if program:

            session.delete(
                program
            )

            session.commit()

            return True


        return False


    finally:

        session.close()



# ==========================================================
# TEST RUN
# ==========================================================


if __name__ == "__main__":


    create_database()


    print(
        "Residency database created:"
    )

    print(
        DATABASE_FILE
    )