from datetime import date, timedelta


def update_streak(user_profile):
    today = date.today()
    yesterday = today - timedelta(days=1)

    # 1. Якщо активність вже була сьогодні — нічого не робимо
    if user_profile.last_activity_date == today:
        return user_profile.current_streak

    # 2. Якщо остання активність була вчора — інкрементуємо (збільшуємо)
    if user_profile.last_activity_date == yesterday:
        user_profile.current_streak += 1
    else:
        # 3. Якщо активність була давніше ніж учора — скидаємо на 1
        user_profile.current_streak = 1

    user_profile.last_activity_date = today
    user_profile.save()

    return user_profile.current_streak