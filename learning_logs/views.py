from django.shortcuts import render, get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    """Página principal do app"""
    return render(request, 'learning_logs/index.html')

@login_required 
def topics(request):
    """Mostra todos os assuntos."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics' : topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Mostra um único assunto e todas as suas entradas."""
    topic = Topic.objects.get(id = topic_id)
       
    # Garante que o assunto perntece ao usuário que esta acessando
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona novo assunto"""
    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco
        form = TopicForm()
    else: 
        # Dados de POST; submetidos processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse('topics'))
    
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Adiciona nova entrada a um assunto"""
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco
        form = EntryForm()
    else: 
        # Dados de POST; submetidos processa os dados
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    
    context = {'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404
    
    if request.method!= 'POST':
        # preenche com a entrada atual
        form = EntryForm(instance=entry)
    else:
        #Processa os dados do Post submetido
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    
    context = {'entry' : entry, 'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    """Exclui uma entrada existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404
    
    task = get_object_or_404(Entry, pk=entry_id)
    task.delete()
    
    context = {'entry' : entry, 'topic' : topic, 'task' : task}
    return HttpResponseRedirect(reverse('topic', args=[topic.id]))

@login_required
def delete_topic(request, topic_id):
    """Exclui um tópico existente"""
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404
    
    task = get_object_or_404(Topic, pk=topic_id)
    task.delete()
    
    context = {'topic' : topic, 'task' : task}
    return HttpResponseRedirect(reverse('topics', args=[]))