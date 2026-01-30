#!/usr/bin/env python3
"""
Watch Insurance Advisor Agent
An AI-powered conversational agent that helps users decide whether 
insuring their watch makes financial sense.

Powered by OpenAI GPT-4
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load the system prompt from file
PROMPT_FILE = Path(__file__).parent / "watch_insurance_prompt.txt"


def load_system_prompt() -> str:
    """Load the system prompt from the prompt file."""
    try:
        with open(PROMPT_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Could not find prompt file at {PROMPT_FILE}")
        sys.exit(1)


def print_header():
    """Print the elegant header for the watch insurance advisor."""
    print("\n")
    print("  " + "═" * 56)
    print("  ║" + " " * 54 + "║")
    print("  ║" + "     ⌚  WATCH INSURANCE ADVISOR  ⌚".center(54) + "║")
    print("  ║" + " " * 54 + "║")
    print("  ║" + "     Your Personal Insurance Consultant".center(54) + "║")
    print("  ║" + " " * 54 + "║")
    print("  " + "═" * 56)
    print()


def print_divider(style: str = "light"):
    """Print a divider line."""
    if style == "heavy":
        print("\n  " + "━" * 54 + "\n")
    else:
        print("\n  " + "─" * 54 + "\n")


def print_message(role: str, content: str):
    """Print a message with appropriate formatting."""
    if role == "assistant":
        print(f"\n  Advisor: {content}")
    else:
        pass  # User input is already shown via input()


def chat(messages: list, system_prompt: str) -> str:
    """Send a message to the OpenAI API and return the response."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                *messages
            ],
            temperature=0.8,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an issue: {str(e)}"


def run_advisor():
    """Main conversation loop for the watch insurance advisor."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n  ⚠️  Error: OPENAI_API_KEY not found in .env file")
        print("  Please add your OpenAI API key to the .env file and try again.\n")
        sys.exit(1)
    
    # Load system prompt
    system_prompt = load_system_prompt()
    
    # Print welcome header
    print_header()
    
    # Initialize conversation
    messages = []
    
    # Get initial greeting from the AI
    initial_response = chat(messages, system_prompt)
    print_message("assistant", initial_response)
    messages.append({"role": "assistant", "content": initial_response})
    
    print("\n  " + "─" * 54)
    print("  Type 'quit' or 'exit' to end the conversation")
    print("  " + "─" * 54)
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            print()
            user_input = input("  You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ["quit", "exit", "bye", "goodbye", "q"]:
                print_divider("light")
                print("  Advisor: Thank you for chatting with me today. Take care,")
                print("           and best of luck with your decision!")
                print_divider("heavy")
                print("  " + "═" * 56)
                print("  ║" + "  Thank you for using Watch Insurance Advisor  ".center(54) + "║")
                print("  " + "═" * 56)
                print()
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Get AI response
            response = chat(messages, system_prompt)
            
            # Display response
            print_message("assistant", response)
            
            # Add assistant response to history
            messages.append({"role": "assistant", "content": response})
            
        except KeyboardInterrupt:
            print("\n")
            print_divider("light")
            print("  Advisor: No problem — feel free to come back anytime!")
            print_divider("heavy")
            break
        except EOFError:
            break


def main():
    """Entry point for the application."""
    run_advisor()


if __name__ == "__main__":
    main()
