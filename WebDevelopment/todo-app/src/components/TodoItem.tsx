import { Todo } from '../types';

interface TodoItemProps {
  todo: Todo;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
}

export default function TodoItem({ todo, toggleTodo, deleteTodo }: TodoItemProps) {
  return (
    <li className="flex items-center justify-between p-4 mb-2 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center gap-3">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => toggleTodo(todo.id)}
          className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
        />
        <span className={`text-lg ${todo.completed ? 'text-gray-400 line-through' : 'text-gray-800'}`}>
          {todo.text}
        </span>
      </div>
      <button
        onClick={() => deleteTodo(todo.id)}
        className="px-3 py-1 text-sm text-red-500 hover:text-red-700 hover:bg-red-50 rounded transition-colors"
      >
        Delete
      </button>
    </li>
  );
}
