from django.shortcuts import render, get_object_or_404
from .models import Question, Choice, Submission

def submit(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("question_"):
                question_id = key.split("_")[1]
                question = Question.objects.get(id=question_id)
                choice = Choice.objects.get(id=value)

                Submission.objects.create(
                    question=question,
                    selected_choice=choice
                )

        return render(request, "result.html")

def show_exam_result(request):
    submissions = Submission.objects.all()
    score = 0

    for sub in submissions:
        if sub.selected_choice.is_correct:
            score += 1

    return render(request, "result.html", {
        "score": score,
        "total": submissions.count()
    })
