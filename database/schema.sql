/*
schema.sql

SQLite schema for Residency-New-Programs database.

Tracks newly accredited:
- Internal Medicine
- Family Medicine
- Pediatrics

Years:
- 2025
- 2026
*/


CREATE TABLE IF NOT EXISTS programs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,


    specialty TEXT NOT NULL,


    program_name TEXT NOT NULL,


    institution TEXT,


    city TEXT,


    state TEXT,


    region TEXT,


    accreditation_year INTEGER,


    accreditation_date DATE,


    accreditation_status TEXT
        DEFAULT 'Initial Accreditation',


    first_match_cycle TEXT,


    residency_start TEXT,


    program_type TEXT,


    hospital_beds INTEGER,


    teaching_hospital BOOLEAN
        DEFAULT 0,


    j1_sponsorship TEXT,


    h1b_sponsorship TEXT,


    img_friendly TEXT,


    ecfmg_required BOOLEAN
        DEFAULT 1,


    usce_required TEXT,


    step2_requirement TEXT,


    website TEXT,


    freida_url TEXT,


    eras_url TEXT,


    program_director TEXT,


    coordinator TEXT,


    coordinator_email TEXT,


    notes TEXT,


    last_updated TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,


    UNIQUE(
        program_name,
        specialty,
        state
    )

);



CREATE INDEX IF NOT EXISTS idx_specialty

ON programs(
    specialty
);



CREATE INDEX IF NOT EXISTS idx_state

ON programs(
    state
);



CREATE INDEX IF NOT EXISTS idx_accreditation_year

ON programs(
    accreditation_year
);