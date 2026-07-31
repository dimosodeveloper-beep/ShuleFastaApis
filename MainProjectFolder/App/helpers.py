from .models import GradingSystem


def get_grade(score, school):

    grade = GradingSystem.objects.filter(
        school=school,
        min_score__lte=score,
        max_score__gte=score
    ).first()

    if grade:
        return grade.grade

    return "N/A"