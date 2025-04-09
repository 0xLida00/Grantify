document.addEventListener('DOMContentLoaded', function () {
    const apiBaseUrl = '/api/todos/';
    const todoList = document.getElementById('todo-list');
    const todoForm = document.getElementById('todo-form');
    const todoTitleInput = document.getElementById('todo-title');
    const paginationNav = document.createElement('nav'); // Create a pagination container
    paginationNav.className = 'mt-3';
    todoList.parentNode.appendChild(paginationNav); // Append it below the to-do list

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
                        <span>${todo.completed ? `<del>${todo.title}</del>` : todo.title}</span>
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

                // Update pagination controls
                updatePagination(data);
            })
            .catch(error => console.error('Error fetching to-dos:', error));
    }

    // Update pagination controls
    function updatePagination(data) {
        paginationNav.innerHTML = ''; // Clear existing pagination

        const pagination = document.createElement('ul');
        pagination.className = 'pagination justify-content-center';

        if (data.previous) {
            const prevLi = document.createElement('li');
            prevLi.className = 'page-item';
            prevLi.innerHTML = `<a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a>`;
            pagination.appendChild(prevLi);
        }

        for (let i = 1; i <= Math.ceil(data.count / data.page_size); i++) {
            const pageLi = document.createElement('li');
            pageLi.className = `page-item ${i === currentPage ? 'active' : ''}`;
            pageLi.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
            pagination.appendChild(pageLi);
        }

        if (data.next) {
            const nextLi = document.createElement('li');
            nextLi.className = 'page-item';
            nextLi.innerHTML = `<a class="page-link" href="#" data-page="${currentPage + 1}">Next</a>`;
            pagination.appendChild(nextLi);
        }

        paginationNav.appendChild(pagination);

        // Add event listeners to pagination links
        pagination.querySelectorAll('.page-link').forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                currentPage = parseInt(this.dataset.page);
                fetchTodos(currentPage);
            });
        });
    }

    // Add a new to-do item
    todoForm.addEventListener('submit', event => {
        event.preventDefault();
        const title = todoTitleInput.value;

        fetch(apiBaseUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ title }),
        })
            .then(response => {
                if (response.ok) {
                    todoTitleInput.value = '';
                    fetchTodos(currentPage); // Refresh the current page
                } else {
                    console.error('Error adding to-do:', response);
                }
            });
    });

    function toggleTodo(id, completed) {
        fetch(`${apiBaseUrl}${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ completed: !completed }),
        })
            .then(response => {
                if (response.ok) {
                    fetchTodos(currentPage); // Refresh the current page
                } else {
                    console.error('Error toggling to-do:', response);
                }
            });
    }

    // Delete a to-do item
    function deleteTodo(id) {
        fetch(`${apiBaseUrl}${id}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        })
            .then(response => {
                if (response.ok) {
                    fetchTodos(currentPage); // Refresh the current page
                } else {
                    console.error('Error deleting to-do:', response);
                }
            });
    }

    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    fetchTodos(); // Initial fetch
});