def life_in_weeks(age):
    max_remaining_years = 90*52
    remaining_years = max_remaining_years - (age*52)
    print(f"You have {remaining_years} weeks left.")

life_in_weeks(42)