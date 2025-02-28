import os
import json
import datetime
import google.generativeai as genai
from dotenv import load_dotenv

class LumoraAssistant:
    def __init__(self, memory_file="patient_memory.json"):
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment variables
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        # Memory file path
        self.memory_file = memory_file
        
        # Load existing memory or create new
        self.patient_memory = self._load_memory()
        
        # Define Lumora's personality and context
        self.system_prompt = """
        You are Lumora, a nurturing and kind caretaker AI assistant. 
        You primarily interact with patients suffering from dementia.
        
        Guidelines for interaction:
        1. Include references to memories the patient has shared with you before
        2. Ask gentle questions to learn more about them
        3. Be patient and understanding, never frustrated
        4. Speak clearly and simply, but not condescendingly
        5. Don't overwhelm with too much information at once
        6. Respond with warmth and empathy
        7. If they repeat something, respond as if it's the first time they've shared it
        8. Help orient them to time and place when appropriate
        9. Avoid correcting them directly if they're confused
        10. Focus on emotional connection rather than factual accuracy
        
        Always adapt your responses based on their current emotional state and needs.
        """
        
        # initialize model and chat session
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.start_new_chat()

    
    def _load_memory(self):
        """Load patient memory from file or create new if not exists"""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # return empty memory structure if file doesn't exist or is invalid
            return {
                "personal_info": {},
                "important_memories": [],
                "preferences": {},
                "conversation_history": [],
                "topics_discussed": {}
            }
    
    def _save_memory(self):
        """Save patient memory to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.patient_memory, f, indent=4)
    
    def start_new_chat(self):
        """Start a new chat session with Lumora's personality"""
        self.chat = self.model.start_chat()

        system_message = f"{self.system_prompt}\n\nPlease follow these guidelines strictly."
        self.chat.send_message(system_message)

        history = []
        #system_instruction=self.system_prompt
        
        # Add memory context if available
        if self.patient_memory["personal_info"] or self.patient_memory["important_memories"]:
            memory_context = "Patient memory context:\n"
            
            if self.patient_memory["personal_info"]:
                memory_context += "Personal information:\n"
                for key, value in self.patient_memory["personal_info"].items():
                    memory_context += f"- {key}: {value}\n"
            
            if self.patient_memory["important_memories"]:
                memory_context += "\nImportant memories shared:\n"
                for memory in self.patient_memory["important_memories"]:
                    memory_context += f"- {memory}\n"
                    
            if self.patient_memory["preferences"]:
                memory_context += "\nPreferences:\n"
                for key, value in self.patient_memory["preferences"].items():
                    memory_context += f"- {key}: {value}\n"
            
            # Add memory context to system prompt
            history.append({
                "role": "system",
                "parts": [memory_context]
            })
        
    
    def update_memory(self, user_message, response):
        """Update patient memory based on conversation"""
        # Add to conversation history
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_memory["conversation_history"].append({
            "timestamp": timestamp,
            "patient": user_message,
            "lumora": response
        })
        
        # Ask Gemini to extract important information from this exchange
        try:
            extraction_prompt = f"""
            Based on this conversation exchange with a patient with dementia, extract any important information to remember:
            
            Patient: {user_message}
            Lumora: {response}
            
            Extract and categorize the following (respond in JSON format only):
            1. Personal information (name, family members, occupation, etc.)
            2. Important memories or stories shared
            3. Preferences mentioned (likes/dislikes)
            4. Topics discussed
            5. Emotional state
            
            JSON format:
            {{
                "personal_info": {{}},
                "memories": [],
                "preferences": {{}},
                "topics": [],
                "emotional_state": ""
            }}
            """
            
            extraction_model = genai.GenerativeModel("gemini-1.5-pro")
            extraction_chat = extraction_model.start_chat()
            extraction_response = extraction_chat.send_message(extraction_prompt)
            
            try:
                # Parse the extraction results
                extracted_data = json.loads(extraction_response.text)
                
                # Update personal info
                for key, value in extracted_data.get("personal_info", {}).items():
                    self.patient_memory["personal_info"][key] = value
                
                # Update important memories
                for memory in extracted_data.get("memories", []):
                    if memory not in self.patient_memory["important_memories"]:
                        self.patient_memory["important_memories"].append(memory)
                
                # Update preferences
                for key, value in extracted_data.get("preferences", {}).items():
                    self.patient_memory["preferences"][key] = value
                
                # Update topics discussed
                for topic in extracted_data.get("topics", []):
                    if topic in self.patient_memory["topics_discussed"]:
                        self.patient_memory["topics_discussed"][topic] += 1
                    else:
                        self.patient_memory["topics_discussed"][topic] = 1
            
            except json.JSONDecodeError:
                # If response isn't valid JSON, just continue without updating
                pass
                
        except Exception as e:
            # If extraction fails, just log and continue
            print(f"Memory extraction error: {str(e)}")
        
        # Save updated memory
        self._save_memory()
    
    def send_message(self, message):
        try:

            full_prompt = f"""
            System Instruction: {self.system_prompt}
            
            Patient: {message}
            Lumora:
            """
            response = self.chat.send_message(full_prompt)
            response_text = response.text

            while response_text.startswith(("\"", "'")) and response_text.endswith(("\"", "'")):
                response_text = response_text[1:-1].strip()

            # Ensure no residual quotation marks remain
            response_text = response_text.replace('\\"', '"').replace("\\'", "'")

            # Update memory
            self.update_memory(message, response_text)

            return response_text
        except Exception as e:
            return f"I'm having a little trouble understanding right now. Could you please repeat that? (Error: {str(e)})"

        """
        Send a message to Lumora and get the response
        try:
            response = self.chat.send_message(message)
            response_text = response.text
            
            # Update memory with this exchange
            self.update_memory(message, response_text)
            
            return response_text
        except Exception as e:
            return f"I'm having a little trouble understanding right now. Could you please repeat that? (Error: {str(e)})"
        """
        
    
    def get_patient_memory(self):
        """Get the current patient memory"""
        return self.patient_memory
    
    def reset_memory(self):
        """Reset patient memory (use with caution)"""
        self.patient_memory = {
            "personal_info": {},
            "important_memories": [],
            "preferences": {},
            "conversation_history": [],
            "topics_discussed": {}
        }
        self._save_memory()
        self.start_new_chat()
        return "Patient memory has been reset."