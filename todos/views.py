from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
import json
from .models import Todo


def is_writer_or_admin(user):
    return user.groups.filter(name__in=['writer', 'Writer', 'admin', 'Admin']).exists()


@login_required
def todo_list(request):
    can_edit = is_writer_or_admin(request.user)
    sort_dir = request.GET.get('sort', 'asc')
    order_prefix = '-' if sort_dir == 'desc' else ''

    columns = [
        ('OPEN', 'Open', Todo.objects.filter(status='OPEN').order_by(f'{order_prefix}priority')),
        ('PLANNING', 'Planning', Todo.objects.filter(status='PLANNING').order_by(f'{order_prefix}priority')),
        ('ONGOING', 'Ongoing', Todo.objects.filter(status='ONGOING').order_by(f'{order_prefix}priority')),
        ('CLOSED', 'Closed', Todo.objects.filter(status='CLOSED').order_by(f'{order_prefix}priority')),
    ]
    return render(request, 'todos/todo_list.html', {
        'columns': columns,
        'can_edit': can_edit,
        'sort_dir': sort_dir,
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


def local_login(request):
    """
    Local login view for non-SAML users.
    Only users who have a usable password can log in.
    """
    if request.user.is_authenticated:
        return redirect('todo_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if user has a usable password (SAML users generally don't)
            if user.has_usable_password():
                auth_login(request, user)
                return redirect('todo_list')
            else:
                messages.error(request, "Access denied. Only local users can use this login page.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'todos/login.html')

@login_required
def update_task_priority(request):
    """
    API endpoint to update task priorities and optionally status (e.g., from drag/drop).
    Expects a POST request with JSON body containing a list of {id: int, priority: int, status: string(optional)}.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    user = request.user
    is_privileged = is_writer_or_admin(user)

    try:
        data = json.loads(request.body)
        if not isinstance(data, list):
            return JsonResponse({'error': 'Expected a JSON array'}, status=400)
        
        updated_count = 0
        for item in data:
            task_id = item.get('id')
            priority = item.get('priority')
            new_status = item.get('status')

            if task_id is None or priority is None:
                continue

            try:
                todo = Todo.objects.get(id=task_id)
            except Todo.DoesNotExist:
                continue

            is_assigned = todo.assigned_users.filter(id=user.id).exists()
            is_owner = todo.owner == user

            # Check permissions
            if not (is_privileged or is_assigned or is_owner):
                continue

            # Assigned-only users can only change status, not priority/text unless it's just the same list reordered by a privileged user.
            status_only = is_assigned and not is_privileged and not is_owner
            
            # If status_only, they shouldn't be reordering the backlog for everyone, but they can move to a new status.
            # However, for UX, if they drag-and-drop to change status, order might be sent too.
            # We will allow order update if they are just moving to a different status column they belong to.
            
            # Always update priority if possible
            if not status_only:
                todo.priority = priority
            
            if new_status and new_status in dict(Todo.STATUS_CHOICES):
                todo.status = new_status

            todo.save()
            updated_count += 1

        return JsonResponse({'status': 'success', 'updated': updated_count})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
