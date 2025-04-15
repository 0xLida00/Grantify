document.addEventListener('DOMContentLoaded', function () {
    const apiBaseUrl = '/api/todos/';
    const todoList = document.getElementById('todo-list');
    const todoForm = document.getElementById('todo-form');
    const todoTitleInput = document.getElementById('todo-title');
    const todoDescriptionInput = document.getElementById('todo-description');
    const paginationNav = document.createElement('nav');
    paginationNav.className = 'mt-3';
    todoList.parentNode.appendChild(paginationNav);

    let currentPage = 1;

    // Fetch and display to-do items
    function fetchTodos(page = 1) {
        fetch(`${apiBaseUrl}?page=${page}`, {
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                const sortedTodos = data.results.sort((a, b) => a.completed - b.completed);

                todoList.innerHTML = '';
                sortedTodos.forEach(todo => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item d-flex justify-content-between align-items-center';
                    li.innerHTML = `
                        <a href="/todos/${todo.id}/" class="text-decoration-none">
                            ${todo.completed ? `<del>${todo.title}</del>` : todo.title}
                        </a>
                        <div>
                            <button class="btn btn-sm ${todo.completed ? 'btn-secondary' : 'btn-success'} toggle-btn" data-id="${todo.id}" data-completed="${todo.completed}">
                                ${todo.completed ? 'Undo' : 'Complete'}
                            </button>
                            <button class="btn btn-sm btn-danger delete-btn" data-id="${todo.id}">Delete</button>
                        </div>
                    `;
                    todoList.appendChild(li);
                });

                document.querySelectorAll('.toggle-btn').forEach(button => {
                    button.addEventListener('click', function () {
                        toggleTodo(this.dataset.id, this.dataset.completed === 'true');
                    });
                });

                document.querySelectorAll('.delete-btn').forEach(button => {
                    button.addEventListener('click', function () {
                        deleteTodo(this.dataset.id);
                    });
                });

                updatePagination(data);
            })
            .catch(error => console.error('Error fetching to-dos:', error));
    }

    // Add a new to-do item
    todoForm.addEventListener('submit', event => {
        event.preventDefault();
        const title = todoTitleInput.value;
        const description = todoDescriptionInput.value;

        fetch(apiBaseUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ title, description }),
        })
            .then(response => {
                if (response.ok) {
                    todoTitleInput.value = '';
                    todoDescriptionInput.value = '';
                    fetchTodos(currentPage);
                } else {
                    console.error('Error adding to-do:', response);
                }
            });
    });

    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    fetchTodos();
});