import csv
import random
import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms import widgets
from django.shortcuts import redirect, get_object_or_404




# Create your views here.
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, \
    FormView
from extra_views import UpdateWithInlinesView
from form_utils.forms import BetterModelForm
from form_utils.widgets import ImageWidget
from events.forms import DescriptionForm, EventImageInline, TransportForm, \
    UploadEventsForm
from events.models import Event, Application, Participation
from teams.models import Team


class EventMixin(View):
    def get_success_url(self):
        return reverse("event", kwargs=self.kwargs)


class HTML5Input(widgets.Input):
    def __init__(self, type, attrs):
        self.input_type = type
        super(HTML5Input, self).__init__(attrs)


def featuredevent():
    try:
        random_idx = random.randint(0, Event.objects.filter(scope="international",
                                                            start_date__gt=datetime
                                                            .date.today()).exclude(
            category='recruitment').count() - 1)
        random_event = Event.objects.filter(scope="international",
                                            start_date__gt=datetime.date.today())
        .exclude(
            category='recruitment')[random_idx]
    except:
        random_event = Event.objects.filter(category="workshop").latest('start_date')
    return random_event


class AddEvents(FormView):
    form_class = UploadEventsForm

    def form_valid(self, form):
        self.handle_events(self.request.FILES['file'])
        return super(AddEvents, self).form_valid(form)

    def handle_events(self, f):
        eventreader = csv.reader(f)
        for event in eventreader:
            t_oc = Team.objects.get(name=event[5])
            new_event = Event.objects.create(
                name=event[0] + "tempobject" + random.randint(500),
                deadline=event[1],
                start_date=event[2],
                end_date=event[3],
                category=event[4],
                description=event[6],
                summary=event[7],
                scope=event[8],
                max_participants=event[9],
            )
            new_event.save()
            new_event.organizers = self.request.user
            new_event.organizing_comittee = t_oc

            if new_event.category == "training":
                new_event.name = event[0] + "-" + str(new_event.start_date)
            else:
                new_event.name = event[0]
            new_event.save()


class InternationalEvents(ListView):
    model = Event

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InternationalEvents, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        events = context['object_list'].filter(scope="international")
        context['active_list'] = []
        context['pending_list'] = []
        context['over_list'] = []
        for event in events:
            try:
                if event.deadline:
                    if event.deadline > timezone.now():
                        context['active_list'].append(event)
                    if event.deadline < timezone.now() and event.end_date > timezone\
                            .now() \
                            .date():
                        context['pending_list'].append(event)
                if event.end_date < timezone.now().date():
                    context['over_list'].append(event)
            except:
                pass
        return context


def confirm_event(request, slug):
    try:
        pa = Participation.objects.get(target__slug=slug, participant=request.user)
    except:
        return redirect(reverse('event', kwargs={'slug': slug}))
    pa.confirmed = True
    pa.confirmation = 0
    pa.save()
    return redirect(reverse('event', kwargs={'slug': slug}))


class EventDetail(DetailView):
    model = Event
    template_name = "events/event_detail.html"

    def get_context_data(self, **kwargs):

        context = super(EventDetail, self).get_context_data(**kwargs)
        try:
            context['participation'] = Participation.objects.get(
                target__slug=self.kwargs['slug'], participant=self.request.user)
        except:
            context['participation'] = None
        return context


class ApplyToEvent(CreateView):
    model = Application
    template_name = 'events/application_form.html'

    def get_context_data(self, **kwargs):
        context = super(ApplyToEvent, self).get_context_data(**kwargs)
        context['object'] = Event.objects.get(slug=self.kwargs['slug'])
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            Application.objects.get(
                applicant=request.user,
                target=Event.objects.get(slug=self.kwargs['slug']))
            return redirect(self.get_success_url())
        except:
            return super(ApplyToEvent, self).dispatch(request, *args, **kwargs)


    def get_success_url(self):
        return reverse('event', kwargs=self.kwargs)

    def form_valid(self, form):
        application = form.save(commit=False)
        application.applicant = self.request.user
        application.target = Event.objects.get(slug=self.kwargs['slug'])
        application.save()
        messages.add_message(
            self.request,
            messages.INFO,
            'Thank you for your application. You will be notified upon acceptance.')
        return redirect(self.get_success_url())


class UpdateTransport(UpdateView):
    form_class = TransportForm
    template_name = 'events/transportation_form.html'

    def get_object(self, queryset=None):
        return Participation.objects.get(applicant=self.request.user,
                                         target=Event.objects.get(
                                             slug=self.kwargs['slug'])).transportation


class FillInTransport(CreateView):
    form_class = TransportForm
    template_name = 'events/transportation_form.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FillInTransport, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['object'] = Event.objects.get(slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        if not self.request.user.tshirt_size or not self.request.user.profile_picture:
            return redirect(reverse('event', kwargs=self.kwargs))
        pax = get_object_or_404(Participation, participant=self.request.user,
                                target__slug=self.kwargs['slug'])
        trans = form.save()
        pax.transportation = trans
        pax.save()
        messages.add_message(
            self.request,
            messages.INFO,
            'Thank you for filling in your transportation details.')
        return redirect(reverse('event', kwargs=self.kwargs))


class ChangeDetails(EventMixin, UpdateView):
    template_name = 'teams/change_details_form.html'
    model = Event
    fields = (
        'name', 'participation_fee', 'start_date', 'end_date', 'deadline', 'location',
        'scope', 'category')


class ChangeDescription(EventMixin, UpdateView):
    template_name = 'events/description_form.html'
    form_class = DescriptionForm
    model = Event


class EventImageForm(BetterModelForm):
    class Meta:
        model = Event
        fields = ('thumbnail',)
        widgets = {
            'thumbnail': ImageWidget()
        }


class EventImages(EventMixin, UpdateWithInlinesView):
    model = Event
    template_name = 'events/event_images_form.html'
    form_class = EventImageForm
    #    widgets= {'thumbnail': ImageWidget()}
    inlines = [EventImageInline]
