from django.shortcuts import render, redirect
from .models import Candidate, Voter


def home(request):
    candidates = Candidate.objects.all()
    return render(request, 'voting/home.html',
                  {'candidates': candidates})


def vote(request):
    if request.method == 'POST':
        voter_id = request.POST.get('voter_id')
        candidate_id = request.POST.get('candidate')

        try:
            voter = Voter.objects.get(voter_id=voter_id)
        except Voter.DoesNotExist:
            return render(request, 'voting/vote.html',
                          {'error': 'Invalid Voter ID'})

        if voter.has_voted:
            return render(request, 'voting/vote.html',
                          {'error': 'You have already voted!'})

        candidate = Candidate.objects.get(id=candidate_id)

        candidate.votes += 1
        candidate.save()

        voter.has_voted = True
        voter.save()

        return redirect('results')

    candidates = Candidate.objects.all()

    return render(request, 'voting/vote.html',
                  {'candidates': candidates})


def results(request):
    candidates = Candidate.objects.all().order_by('-votes')

    return render(request, 'voting/results.html',
                  {'candidates': candidates})