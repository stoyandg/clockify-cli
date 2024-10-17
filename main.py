import argparse
import time
import pickle
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch the Clockify API key from environment variables
API_KEY = os.getenv("CLOCKIFY_API_KEY")

if not API_KEY:
    raise ValueError("Clockify API Key not found. Make sure it's set in the .env file.")

# Clockify API base URL
CLOCKIFY_API_URL = "https://api.clockify.me/api/v1"

# Define the file to store the time data
TIME_FILE = 'time_data.pkl'

# Function to authenticate with Clockify
def authenticate():
    headers = {
        "X-Api-Key": API_KEY
    }
    
    response = requests.get(f"{CLOCKIFY_API_URL}/user", headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"Authentication successful! Logged in as: {user_data['name']}")
        return user_data
    else:
        print(f"Authentication failed! Status code: {response.status_code}")
        return None

# Function to get workspace ID
def get_workspace_id():
    headers = {
        "X-Api-Key": API_KEY
    }
    
    response = requests.get(f"{CLOCKIFY_API_URL}/workspaces", headers=headers)
    
    if response.status_code == 200:
        workspaces = response.json()
        if workspaces:
            return workspaces[0]['id']  # Return the first workspace ID
        else:
            print("No workspaces found.")
            return None
    else:
        print(f"Failed to retrieve workspaces. Status code: {response.status_code}")
        return None

# Function to get available projects in a workspace
def get_projects(workspace_id):
    headers = {
        "X-Api-Key": API_KEY
    }

    response = requests.get(f"{CLOCKIFY_API_URL}/workspaces/{workspace_id}/projects", headers=headers)

    if response.status_code == 200:
        projects = response.json()
        if projects:
            return {i+1: project for i, project in enumerate(projects)}
        else:
            print("No projects found.")
            return None
    else:
        print(f"Failed to retrieve projects. Status code: {response.status_code}")
        return None

# Function to submit time to Clockify
def submit_time(workspace_id, project_id, start_time, end_time, description):
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

    time_entry_data = {
        "start": datetime.utcfromtimestamp(start_time).isoformat() + 'Z',
        "end": datetime.utcfromtimestamp(end_time).isoformat() + 'Z',
        "description": description,
        "billable": True,
        "projectId": project_id  # Submit the project ID
    }

    response = requests.post(f"{CLOCKIFY_API_URL}/workspaces/{workspace_id}/time-entries", 
                             headers=headers, json=time_entry_data)

    if response.status_code == 201:
        print(f"Time entry successfully submitted to Clockify!")
    else:
        print(f"Failed to submit time entry. Status code: {response.status_code}")

# Function to load time data
def load_time_data():
    if os.path.exists(TIME_FILE):
        with open(TIME_FILE, 'rb') as f:
            return pickle.load(f)
    return None

# Function to save time data
def save_time_data(start_time):
    with open(TIME_FILE, 'wb') as f:
        pickle.dump(start_time, f)

# Function to start the timer
def start():
    start_time = time.time()
    save_time_data(start_time)
    print("Timer started!")

# Function to stop the timer and choose a project
def stop():
    start_time = load_time_data()
    if start_time:
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Authenticate and get projects
        user_data = authenticate()
        if user_data:
            workspace_id = get_workspace_id()
            if workspace_id:
                projects = get_projects(workspace_id)
                if projects:
                    project_id, project_name = choose_project(projects, elapsed_time)
                    
                    # Submit time to Clockify with the chosen project
                    submit_time(workspace_id, project_id, start_time, end_time, project_name)
        
        os.remove(TIME_FILE)  # Remove the file after stopping the timer
    else:
        print("Timer was not started. Use --start to start the timer.")

# Function to choose project and return the project ID
def choose_project(projects, elapsed_time):
    print("Choose a project:")
    for key, project in projects.items():
        print(f"{key} - {project['name']}")
    
    try:
        choice = int(input("Enter the number corresponding to the project: "))
        if choice in projects:
            project = projects[choice]
            print(f"You've been working on {project['name']} for {elapsed_time:.2f} seconds.")
            return project['id'], project['name']
        else:
            print("Invalid choice.")
            return None, "Unknown project"
    except ValueError:
        print("Please enter a valid number.")
        return None, "Unknown project"

# Main function to handle arguments and orchestrate the program
def main():
    # First, authenticate with Clockify
    if authenticate():
        parser = argparse.ArgumentParser(description='Time Tracker')
        parser.add_argument('--start', action='store_true', help='Start the timer')
        parser.add_argument('--stop', action='store_true', help='Stop the timer')

        args = parser.parse_args()

        if args.start:
            start()
        elif args.stop:
            stop()
        else:
            print("Please provide either --start or --stop as an argument.")

if __name__ == "__main__":
    main()
