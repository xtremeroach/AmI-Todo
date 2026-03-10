# ImA TODO - User Manual

Welcome to the ImA TODO User Manual! This guide covers the essential features of the task board, prioritizing tasks, and accessing the application securely.

## 1. Local and Admin Login

For standard users inside the organization, Single Sign-On (SSO) via Microsoft Entra ID is seamlessly integrated. For system administrators or external local users, a dedicated `Local Sign-in` page is provided.

**How to access it:**
Navigate directly to `/login/` in your browser. Enter your local credentials.

> [!NOTE]
> Only local users with a usable password configured in the database can use this form. Standard Entra ID users will be cleanly redirected. Additionally, only the `admin` superuser or members of the `admin` group can access the Django `/admin/` panel. Normal local users will be redirected to the dashboard.

![Local Sign-in Page](./screenshots/login.png)

---

## 2. Managing Priorities with Drag and Drop

The primary way to manage your work on the Task Board is through the interactive interface. You can prioritize tasks and update their status using smooth drag-and-drop mechanics.

### Prioritizing within a Status Column
1. Hover your cursor over a task card. The cursor will change to a "grab" icon.
2. Click and hold the task card, then drag it up or down within its current column.
3. Drop the card at the desired position. The topmost items inherently have the highest priority in ascending sort view.

### Moving Tasks to a New Status
1. Click and hold a task card.
2. Drag it to a different column (e.g., from **OPEN** to **ONGOING**).
3. Drop the card into its new priority slot. The system automatically updates the task's status and its new priority.

![Drag and Drop in Action](./screenshots/drag_drop.png)

> [!IMPORTANT]
> The drag-and-drop feature strictly enforces permissions. You can only move items around if you are the owner of the task, assigned to the task, or have administrative/writer privileges.

---

## 3. Stacked View

If you prefer viewing tasks strictly as a horizontal list instead of Kanban columns, you can switch to the **Stacked View**.

1. Click the **Stacked View** icon (the three horizontal bars) on the top-right toolbar.
2. Your tasks will be grouped vertically by their status.
3. The *exact same* drag-and-drop logic applies here: you can pull a task up or down the list, or drag it entirely outside of its group to place it into another status group.

![Stacked View List](./screenshots/stacked.png)

---

## 4. Sorting Priority

By default, the board displays tasks in **Ascending** priority order (highest priority at the top).

If you wish to reverse the list to see lower priority tasks first, simply click the **Sort** button next to the view toggles. The button icon will flip, representing the new Descending sort direction.

![Sort Toggle UI](./screenshots/sort.png)
