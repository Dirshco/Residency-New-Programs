from database import get_all_programs

programs = get_all_programs()

print(len(programs))

for p in programs[:5]:
    print(
        p.specialty,
        p.program_name,
        p.state,
        p.accreditation_year
    )