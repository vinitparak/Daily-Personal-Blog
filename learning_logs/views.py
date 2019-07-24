from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
	return render(request, 'learning_logs/index.html')

@login_required	
def topics(request):
	"""show all topics"""
	topics = Topic.objects.order_by('date_added')
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required	
def topic(request, topic_id):
	"""Show a single topic  and all its entires"""
	topic =  Topic.objects.get(id=topic_id)
	#make sure topic belons to the current user.
	if topic.owner != request.user:
		raise Http404

	entires = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entires': entires}
	return render(request, 'learning_logs/topic.html', context)	

@login_required	
def new_topic(request):
	"""Add a new topic"""
	if request.method != 'POST':
		form = TopicForm()
		# post data submittedl create a blank form
	else:
		# post data submtted; process data
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner =  request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))		

	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required		
def new_entry(request, topic_id):
	"""Add a new entry for a particular topic"""
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		form = EntryForm()
	else:
		#post data submitted ;process data
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

	context = {'topic': topic, 'form': form}	
	return render(request, 'learning_logs/new_entry.html', context)	

@login_required
def edit_entry(request, entry_id):
	"""Edit an exiting entry"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		#initial request, pre-fill form with the current entry.
		form = EntryForm(instance=entry)
	else:
		#post data submitted; process data
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)


























