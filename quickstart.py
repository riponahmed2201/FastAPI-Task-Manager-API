#!/usr/bin/env python
"""
Quick start guide for the Task Manager API
Run this file to understand the basic workflow
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"
token: Optional[str] = None

def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def register_user(username: str, password: str):
    global token
    print_section("1. Register a new user")
    print(f"Registering user: {username}")
    
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"username": username, "password": password}
    )
    
    if response.status_code == 200:
        user = response.json()
        print(f"✓ User registered successfully!")
        print(f"  User ID: {user['id']}")
        print(f"  Username: {user['username']}")
        return user
    else:
        print(f"✗ Registration failed: {response.json()}")
        return None

def login_user(username: str, password: str):
    global token
    print_section("2. Login user")
    print(f"Logging in as: {username}")
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": username, "password": password}
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data['access_token']
        print(f"✓ Login successful!")
        print(f"  Token: {token[:20]}...")
        print(f"  Token Type: {data['token_type']}")
        return token
    else:
        print(f"✗ Login failed: {response.json()}")
        return None

def get_current_user():
    print_section("3. Get current user")
    
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        user = response.json()
        print(f"✓ Current user retrieved!")
        print(f"  ID: {user['id']}")
        print(f"  Username: {user['username']}")
        return user
    else:
        print(f"✗ Failed to get user: {response.json()}")
        return None

def create_task(title: str, description: str = ""):
    print_section("4. Create a task")
    print(f"Creating task: {title}")
    
    response = requests.post(
        f"{BASE_URL}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": title, "description": description}
    )
    
    if response.status_code == 200:
        task = response.json()
        print(f"✓ Task created successfully!")
        print(f"  Task ID: {task['id']}")
        print(f"  Title: {task['title']}")
        print(f"  Description: {task['description']}")
        print(f"  Completed: {task['completed']}")
        return task
    else:
        print(f"✗ Failed to create task: {response.json()}")
        return None

def get_tasks():
    print_section("5. Get all tasks")
    
    response = requests.get(
        f"{BASE_URL}/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✓ Retrieved {len(tasks)} task(s)!")
        for task in tasks:
            status = "✓ Complete" if task['completed'] else "○ Incomplete"
            print(f"  [{task['id']}] {task['title']} - {status}")
        return tasks
    else:
        print(f"✗ Failed to get tasks: {response.json()}")
        return None

def complete_task(task_id: int):
    print_section(f"6. Mark task {task_id} as complete")
    
    response = requests.patch(
        f"{BASE_URL}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        task = response.json()
        print(f"✓ Task marked as complete!")
        print(f"  Title: {task['title']}")
        print(f"  Completed: {task['completed']}")
        return task
    else:
        print(f"✗ Failed to mark task complete: {response.json()}")
        return None

def delete_task(task_id: int):
    print_section(f"7. Delete task {task_id}")
    
    response = requests.delete(
        f"{BASE_URL}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Task deleted successfully!")
        print(f"  Message: {result['message']}")
        return result
    else:
        print(f"✗ Failed to delete task: {response.json()}")
        return None

def main():
    print("\n" + "="*60)
    print("  TASK MANAGER API - QUICK START GUIDE")
    print("="*60)
    print("\nThis script demonstrates the basic workflow of the Task Manager API.")
    print("Make sure the server is running: uvicorn app.main:app --reload")
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print("\n✗ Server is not responding correctly")
            return
    except requests.exceptions.ConnectionError:
        print("\n✗ Cannot connect to server at http://localhost:8000")
        print("Please start the server with: uvicorn app.main:app --reload")
        return
    
    # Run the workflow
    user = register_user("demouser", "password123")
    if not user:
        return
    
    token_result = login_user("demouser", "password123")
    if not token_result:
        return
    
    get_current_user()
    
    task1 = create_task("Buy groceries", "Milk, eggs, bread")
    if task1:
        task_id = task1['id']
        
        task2 = create_task("Complete project", "Finish the API development")
        
        get_tasks()
        
        complete_task(task_id)
        
        get_tasks()
        
        delete_task(task_id)
        
        get_tasks()
    
    print_section("✓ Quick Start Complete!")
    print("You have successfully:")
    print("  1. Registered a new user")
    print("  2. Logged in and received an authentication token")
    print("  3. Retrieved the current user information")
    print("  4. Created tasks")
    print("  5. Retrieved all tasks")
    print("  6. Marked tasks as complete")
    print("  7. Deleted tasks")
    print("\nFor more information, visit:")
    print("  • Interactive API docs: http://localhost:8000/docs")
    print("  • ReDoc documentation: http://localhost:8000/redoc")
    print("  • Project README: See README.md in the project root")
    print()

if __name__ == "__main__":
    main()
