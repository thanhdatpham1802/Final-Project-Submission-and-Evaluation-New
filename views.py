from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Question, Choice, Submission


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # giả lập enrollment (nếu chưa có auth)
    enrollment = Enrollment.objects.filter(course=course).first()

    selected_ids = []
    for key, value in request.POST.items():
        if key.startswith('question_'):
            selected_ids.append(int(value))

    # tạo submission
    submission = Submission.objects.create(enrollment=enrollment)

    # gắn các choice đã chọn
    submission.choices.set(selected_ids)
    submission.save()

    # redirect sang result
    return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    total_score = 0
    possible_score = 0

    questions = Question.objects.filter(lesson__course=course)

    for question in questions:
        possible_score += 1

        selected_choices = submission.choices.filter(question=question)
        all_choices = question.choice_set.all()

        if question.is_get_score(selected_choices):
            total_score += 1

    grade = (total_score / possible_score) * 100 if possible_score > 0 else 0

    return render(request, 'exam_result_bootstrap.html', {
        'course': course,
        'submission': submission,
        'grade': grade,
        'total_score': total_score,
        'possible_score': possible_score,
    })
