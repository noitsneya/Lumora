from chat import LumoraAssistant
import sys
import os
import datetime
import google.generativeai as genai

genai.configure(api_key="GEMINI_API_KEY")
models = genai.list_models()
for model in models:
    print(model.name, "-", model.supported_generation_methods)

def print_header():
    """Print a welcome header for Lumora"""
    print("\n" + "="*60)
    print("                       LUMORA ASSISTANT")
    print("           A nurturing companion for dementia care")
    print("="*60)
    print("\nType your message to chat with Lumora.")
    print("Special commands:")
    print("  'exit' or 'quit' - End the session")
    print("  'new session' - Start a new chat session (keeps memory)")
    print("  'memory' - View current patient memory")
    print("  'reset memory' - Clear all patient memory (use with caution)")
    print("-"*60 + "\n")

def format_response(text):
    """Format Lumora's response for better readability"""
    # Add some light formatting to make responses more readable
    paragraphs = text.split('\n')
    formatted = []
    for p in paragraphs:
        if p.strip():
            # Wrap long lines
            formatted.append(p)
        else:
            formatted.append("")
    return "\n".join(formatted)

def main():
    print_header()
    
    try:
        # Initialize Lumora
        print("Initializing Lumora...")
        lumora = LumoraAssistant()
        
        # Get current time for greeting
        current_hour = datetime.datetime.now().hour
        time_greeting = "Good morning" if 5 <= current_hour < 12 else "Good afternoon" if 12 <= current_hour < 18 else "Good evening"
        
        # Welcome message
        welcome_message = f"{time_greeting}! I'm Lumora, your companion. How are you feeling today?"
        print(f"\nLumora: {welcome_message}")
        
        while True:
            # Get user input
            user_input = input("\nYou: ")
            
            # Process special commands
            if user_input.lower() in ['exit', 'quit']:
                print("\nLumora: It was lovely spending time with you. I'll be here when you need me again. Take care!")
                break
                
            elif user_input.lower() == 'new session':
                lumora.start_new_chat()
                print("\nLumora: I'm starting a fresh conversation, but I'll remember everything we've discussed before.")
                continue
                
            elif user_input.lower() == 'memory':
                memory = lumora.get_patient_memory()
                
                print("\n----- PATIENT MEMORY -----")
                
                if memory["personal_info"]:
                    print("\nPersonal Information:")
                    for key, value in memory["personal_info"].items():
                        print(f"  - {key}: {value}")
                        
                if memory["important_memories"]:
                    print("\nImportant Memories:")
                    for memory_item in memory["important_memories"]:
                        print(f"  - {memory_item}")
                        
                if memory["preferences"]:
                    print("\nPreferences:")
                    for key, value in memory["preferences"].items():
                        print(f"  - {key}: {value}")
                        
                if memory["topics_discussed"]:
                    print("\nFrequently Discussed Topics:")
                    for topic, count in sorted(memory["topics_discussed"].items(), key=lambda x: x[1], reverse=True):
                        print(f"  - {topic}: {count} times")
                
                print("\n--------------------------")
                continue
                
            elif user_input.lower() == 'reset memory':
                confirm = input("\nWARNING: This will erase all stored patient memory. Type 'CONFIRM' to proceed: ")
                if confirm == "CONFIRM":
                    lumora.reset_memory()
                    print("\nLumora: I've reset my memory. Let's start fresh. How are you today?")
                else:
                    print("\nLumora: Memory reset cancelled.")
                continue
            
            # Regular conversation - send message to Lumora
            print("\nLumora: ", end="")
            response = lumora.send_message(user_input)
            print(format_response(response))
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check your .env file and make sure GEMINI_API_KEY is set correctly.")
        sys.exit(1)

if __name__ == "__main__":
    main()