from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Proposal
from calls_app.models import GrantCall, GrantResponse


# Admin: List all proposals for a specific grant call
@staff_member_required
def admin_proposal_list(request):
    grant_call_id = request.GET.get('grant_call')
    status = request.GET.get('status')

    proposals = Proposal.objects.all()

    if grant_call_id:
        proposals = proposals.filter(grant_call_id=grant_call_id)

    if status:
        proposals = proposals.filter(status=status)

    grant_calls = GrantCall.objects.all()
    return render(request, 'proposals_app/admin_proposal_list.html', {
        'proposals': proposals,
        'grant_calls': grant_calls,
        'selected_grant_call': grant_call_id,
        'selected_status': status,
    })


# Admin: View proposal details
@staff_member_required
def admin_proposal_detail(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    responses = GrantResponse.objects.filter(grant_call=proposal.grant_call, user=proposal.applicant)
    return render(request, 'proposals_app/admin_proposal_detail.html', {
        'proposal': proposal,
        'responses': responses,
    })


# Applicant: List saved and submitted proposals
@login_required
def proposal_list(request):
    proposals = Proposal.objects.filter(applicant=request.user)
    return render(request, 'proposals_app/proposal_list.html', {'proposals': proposals})


# Applicant: View proposal details
@login_required
def proposal_detail(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, applicant=request.user)
    responses = GrantResponse.objects.filter(grant_call=proposal.grant_call, user=request.user)
    return render(request, 'proposals_app/proposal_detail.html', {
        'proposal': proposal,
        'responses': responses,
    })