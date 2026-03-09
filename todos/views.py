from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Todo

def is_writer_or_admin(user):
    return user.groups.filter(name__in=['writer', 'Writer', 'admin', 'Admin']).exists()

@login_required
def todo_list(request):
    todos = Todo.objects.all()
    can_edit = is_writer_or_admin(request.user)
    return render(request, 'todos/todo_list.html', {'todos': todos, 'can_edit': can_edit})

@login_required
@user_passes_test(is_writer_or_admin)
def todo_create(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Todo.objects.create(text=text)
        return redirect('todo_list')
    return render(request, 'todos/todo_form.html')

@login_required
@user_passes_test(is_writer_or_admin)
def todo_update_status(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Todo.STATUS_CHOICES):
            todo.status = new_status
            todo.save()
        return redirect('todo_list')
    return render(request, 'todos/todo_status_form.html', {'todo': todo})
