from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from .models import Todo


def is_writer_or_admin(user):
    return user.groups.filter(name__in=['writer', 'Writer', 'admin', 'Admin']).exists()


@login_required
def todo_list(request):
    can_edit = is_writer_or_admin(request.user)
    columns = [
        ('OPEN', 'Open', Todo.objects.filter(status='OPEN')),
        ('PLANNING', 'Planning', Todo.objects.filter(status='PLANNING')),
        ('ONGOING', 'Ongoing', Todo.objects.filter(status='ONGOING')),
        ('CLOSED', 'Closed', Todo.objects.filter(status='CLOSED')),
    ]
    return render(request, 'todos/todo_list.html', {
        'columns': columns,
        'can_edit': can_edit,
    })


@login_required
@user_passes_test(is_writer_or_admin)
def todo_create(request):
    users = User.objects.all().order_by('first_name', 'last_name', 'username')
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            todo = Todo.objects.create(text=text, owner=request.user)
            assigned_ids = request.POST.getlist('assigned_users')
            if assigned_ids:
                todo.assigned_users.set(assigned_ids)
        return redirect('todo_list')
    return render(request, 'todos/todo_form.html', {'users': users})


@login_required
def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    user = request.user
    is_privileged = is_writer_or_admin(user)
    is_assigned = todo.assigned_users.filter(pk=user.pk).exists()
    is_owner = todo.owner == user

    # Only owner, assigned users, and writers/admins can access
    if not (is_privileged or is_assigned or is_owner):
        return redirect('todo_list')

    # Assigned-only users can only change status
    status_only = is_assigned and not is_privileged and not is_owner

    users = User.objects.all().order_by('first_name', 'last_name', 'username')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Todo.STATUS_CHOICES):
            todo.status = new_status

        if not status_only:
            new_text = request.POST.get('text')
            if new_text:
                todo.text = new_text
            assigned_ids = request.POST.getlist('assigned_users')
            todo.assigned_users.set(assigned_ids)

        todo.save()
        return redirect('todo_list')

    return render(request, 'todos/todo_edit.html', {
        'todo': todo,
        'users': users,
        'status_only': status_only,
    })


@login_required
def user_search(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 1:
        return JsonResponse([], safe=False)

    users = User.objects.filter(
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(username__icontains=q)
    )[:20]

    results = [
        {
            'id': u.pk,
            'first_name': u.first_name or '',
            'last_name': u.last_name or '',
            'username': u.username,
            'display': f"{u.first_name} {u.last_name} ({u.username})".strip(),
        }
        for u in users
    ]
    return JsonResponse(results, safe=False)
