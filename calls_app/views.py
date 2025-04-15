from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from alerts_app.models import Notification
from .models import GrantCall, GrantQuestion, GrantChoice, GrantResponse
from .forms import GrantCallForm, GrantQuestionForm, GrantChoiceForm, GrantQuestionFormSet, ApplicationForm, GrantChoiceFormSet
from audit_app.models import LogEntry
from proposals_app.models import Proposal


# Grant Call List View with Pagination and Filtering
class GrantCallListView(ListView):
    model = GrantCall
    template_name = "calls_app/grant_call_list.html"
    context_object_name = "grant_calls"
    paginate_by = 10

    def get_queryset(self):
        queryset = GrantCall.objects.all().order_by('-created_at')
        if self.request.user.is_authenticated and self.request.user.role == "applicant":
            queryset = queryset.exclude(status="draft")

        filter_by = self.request.GET.get("filter_by", "").strip()
        value = self.request.GET.get("value", "").strip()
        if filter_by and value:
            if filter_by == "status":
                queryset = queryset.filter(status__icontains=value)
            elif filter_by == "title":
                queryset = queryset.filter(title__icontains=value)
            elif filter_by == "created_by":
                queryset = queryset.filter(created_by__username__icontains=value)

        sort_by = self.request.GET.get("sort_by", "").strip()
        if sort_by == "newest":
            queryset = queryset.order_by("-created_at")
        elif sort_by == "oldest":
            queryset = queryset.order_by("created_at")
        elif sort_by == "budget_high":
            queryset = queryset.order_by("-budget")
        elif sort_by == "budget_low":
            queryset = queryset.order_by("budget")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get("page")

        try:
            grant_calls = paginator.page(page)
        except PageNotAnInteger:
            grant_calls = paginator.page(1)
        except EmptyPage:
            grant_calls = paginator.page(paginator.num_pages)

        context["grant_calls"] = grant_calls
        context["page_obj"] = grant_calls
        context["filter_by"] = self.request.GET.get("filter_by", "")
        context["value"] = self.request.GET.get("value", "")
        context["sort_by"] = self.request.GET.get("sort_by", "")
        return context


# Grant Call Create View
class GrantCallCreateView(LoginRequiredMixin, CreateView):
    model = GrantCall
    form_class = GrantCallForm
    template_name = "calls_app/grant_call_form.html"
    success_url = reverse_lazy("grant_call_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to create a grant call.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["question_formset"] = GrantQuestionFormSet(self.request.POST, instance=self.object)
            context["choice_formsets"] = [
                GrantChoiceFormSet(self.request.POST, instance=question_form.instance, prefix=f"choices_{index}")
                for index, question_form in enumerate(context["question_formset"])
            ]
        else:
            context["question_formset"] = GrantQuestionFormSet(instance=self.object)
            context["choice_formsets"] = [
                GrantChoiceFormSet(instance=question_form.instance, prefix=f"choices_{index}")
                for index, question_form in enumerate(context["question_formset"])
            ]
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        question_formset = context["question_formset"]
        choice_formsets = context["choice_formsets"]

        if form.is_valid() and question_formset.is_valid():
            grant_call = form.save(commit=False)
            grant_call.created_by = self.request.user
            grant_call.save()

            question_formset.instance = grant_call
            questions = question_formset.save()

            for question, choice_formset in zip(questions, choice_formsets):
                if question.question_type == "multiple_choice":
                    choice_formset.instance = question
                    if choice_formset.is_valid():
                        choice_formset.save()

            LogEntry.objects.create(
                user=self.request.user,
                action="Grant Call Created",
                object_repr=str(grant_call),
                change_message=f"Grant call '{grant_call.title}' was created.",
                log_level="INFO",
                source="User",
            )

            Notification.objects.create(
                user=self.request.user,
                notification_type="in_app",
                message=f"Grant call '{grant_call.title}' has been created successfully.",
                is_read=False,
            )

            messages.success(self.request, "Grant call created successfully!")
            return redirect(self.success_url)
        else:
            messages.error(self.request, "There was an error creating the grant call. Please check the form.")
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        context = self.get_context_data()
        question_formset = context["question_formset"]
        return super().form_invalid(form)


# Grant Call Detail View
class GrantCallDetailView(DetailView):
    model = GrantCall
    template_name = "calls_app/grant_call_detail.html"
    context_object_name = "grant_call"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grant_call = self.get_object()

        context["questions"] = grant_call.questions.prefetch_related("choices").all()

        return context


# Grant Call Application View
@login_required
def apply_grant_call(request, pk):
    if request.user.role != 'applicant':
        return HttpResponseForbidden()

    grant_call = get_object_or_404(GrantCall, pk=pk)

    if grant_call.status != 'open':
        messages.error(request, "This grant call is not open for applications.")
        return redirect("grant_call_list")

    proposal, created = Proposal.objects.get_or_create(
        grant_call=grant_call,
        applicant=request.user,
        defaults={
            'title': f"Proposal for {grant_call.title}",
            'description': '',
            'status': 'draft',
        }
    )

    questions = grant_call.questions.all()

    initial_data = {}
    for question in questions:
        try:
            response = GrantResponse.objects.get(question=question, user=request.user, grant_call=grant_call)
            initial_data[f'question_{question.id}_response'] = response.response
            initial_data[f'question_{question.id}_file'] = response.file
        except GrantResponse.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, questions=questions, initial=initial_data)
        if form.is_valid():
            for question in questions:
                response_text = form.cleaned_data.get(f'question_{question.id}_response')
                response_file = form.cleaned_data.get(f'question_{question.id}_file')
                response, created = GrantResponse.objects.get_or_create(
                    question=question,
                    user=request.user,
                    grant_call=grant_call,
                )
                response.response = response_text
                if response_file:
                    response.file = response_file
                response.is_final_submission = 'submit' in request.POST
                response.save()

            if 'submit' in request.POST:
                proposal.status = 'submitted'
                messages.success(request, f"You have successfully submitted your application for the grant call: {grant_call.title}")
            else:
                messages.success(request, "Your progress has been saved. You can return to complete your application later.")
            proposal.description = form.cleaned_data.get('description', proposal.description)
            proposal.save()

            if 'submit' in request.POST:
                Notification.objects.create(
                    user=request.user,
                    notification_type="in_app",
                    message=f"You have successfully submitted your application for the grant call: '{grant_call.title}'.",
                    is_read=False,
                )
                return redirect("grant_call_list")
            else:
                return redirect("apply_grant_call", pk=grant_call.pk)
    else:
        form = ApplicationForm(questions=questions, initial=initial_data)

    return render(request, 'calls_app/apply_grant_call.html', {
        'grant_call': grant_call,
        'form': form,
        'proposal': proposal,
    })


# Toggle Favorite View
@login_required
def toggle_favorite(request, pk):
    if request.user.role != 'applicant':
        return JsonResponse({"error": "You do not have permission to perform this action."}, status=403)

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    grant_call = get_object_or_404(GrantCall, pk=pk)
    if request.user in grant_call.favorited_by.all():
        grant_call.favorited_by.remove(request.user)
        is_favorited = False

        LogEntry.objects.create(
            user=request.user,
            action="Grant Call Unfavorited",
            object_repr=str(grant_call),
            change_message=f"Grant call '{grant_call.title}' was unfavorited.",
            log_level="INFO",
            source="User",
        )
    else:
        grant_call.favorited_by.add(request.user)
        is_favorited = True

        LogEntry.objects.create(
            user=request.user,
            action="Grant Call Favorited",
            object_repr=str(grant_call),
            change_message=f"Grant call '{grant_call.title}' was favorited.",
            log_level="INFO",
            source="User",
        )

    return JsonResponse({"is_favorited": is_favorited})


# Favorite Grant Calls View
class FavoriteGrantCallsView(LoginRequiredMixin, ListView):
    model = GrantCall
    template_name = "calls_app/favorite_grant_calls.html"
    context_object_name = "favorite_grant_calls"

    def get_queryset(self):
        if self.request.user.role != 'applicant':
            return HttpResponseForbidden("You do not have permission to access this page.")
        return GrantCall.objects.filter(favorited_by=self.request.user)
    

# Grant Call Update View
class GrantCallUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GrantCall
    form_class = GrantCallForm
    template_name = "calls_app/grant_call_form.html"
    success_url = reverse_lazy("grant_call_list")

    def test_func(self):
        grant_call = self.get_object()
        return self.request.user.role in ["admin", "org"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grant_call = self.get_object()
        if self.request.POST:
            context["question_formset"] = GrantQuestionFormSet(self.request.POST, instance=grant_call)
        else:
            context["question_formset"] = GrantQuestionFormSet(instance=grant_call)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        question_formset = context["question_formset"]

        # Validate the formset before accessing cleaned_data
        if form.is_valid() and question_formset.is_valid():
            # Debugging: Check each form in the formset after validation
            for i, question_form in enumerate(question_formset):
                print(f"Form {i} data:", question_form.cleaned_data)

            # Save the main GrantCall form
            grant_call = form.save(commit=False)
            grant_call.modified_by = self.request.user
            grant_call.save()

            # Save the formset (questions)
            question_formset.instance = grant_call
            question_formset.save()

            # Log the update
            LogEntry.objects.create(
                user=self.request.user,
                action="Grant Call Updated",
                object_repr=str(grant_call),
                change_message=f"Grant call '{grant_call.title}' was updated.",
                log_level="INFO",
                source="User",
            )

            # Success message and redirect
            messages.success(self.request, "Grant call updated successfully!")
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        question_formset = context["question_formset"]

        # Debugging: Log errors and submitted data
        print("Form invalid. Errors:", form.errors)
        print("Formset invalid. Errors:", question_formset.errors)
        print("Submitted POST data:", self.request.POST)

        return self.render_to_response(self.get_context_data(form=form, question_formset=question_formset))


# Grant Call Delete View
class GrantCallDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GrantCall
    template_name = "calls_app/grant_call_confirm_delete.html"
    success_url = reverse_lazy("grant_call_list")

    def test_func(self):
        return self.request.user.role in ["admin", "org"]

    def form_valid(self, form):
        grant_call = self.get_object()

        LogEntry.objects.create(
            user=self.request.user,
            action="Grant Call Deleted",
            object_repr=str(grant_call),
            change_message=f"Grant call '{grant_call.title}' was deleted.",
            log_level="WARNING",
            source="User",
        )

        Notification.objects.create(
            user=self.request.user,
            notification_type="in_app",
            message=f"Grant call '{grant_call.title}' has been deleted.",
            is_read=False,
        )

        messages.success(self.request, "Grant call deleted successfully!")
        return super().form_valid(form)


# Question Addition View
@login_required
def add_question(request, grant_call_id):
    grant_call = get_object_or_404(GrantCall, id=grant_call_id)
    if request.method == "POST":
        form = GrantQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.grant_call = grant_call
            question.save()
            return redirect("grant_call_detail", pk=grant_call.id)
    else:
        form = GrantQuestionForm()
    return render(request, "calls_app/add_question.html", {"form": form, "grant_call": grant_call})