from openai import OpenAI
from typing import List, Dict
from kc_manager import KCManager
from config import Config

class StudentSimulator:
    """Simulates a student using OpenAI GPT-4 based on knowledge mastery"""
    
    def __init__(self):
        self.kc_manager = KCManager()
        self.conversation_history = []
        # Initialize OpenAI client with current API format
        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY
        )
        self.load_prompts()
    
    def load_prompts(self):
        """Load prompt templates from files"""
        self.prompts = {}
        prompt_files = {
            'base': 'student_base_prompt.txt',
            'mastery_0': 'mastery_0_prompt.txt',
            'mastery_50': 'mastery_50_prompt.txt',
            'mastery_100': 'mastery_100_prompt.txt'
        }
        
        for key, filename in prompt_files.items():
            try:
                with open(f"{Config.PROMPTS_DIR}{filename}", 'r') as f:
                    self.prompts[key] = f.read().strip()
            except FileNotFoundError:
                print(f"Warning: Could not load {filename}")
                self.prompts[key] = ""
    
    def generate_response(self, teacher_message: str) -> str:
        """Generate student response based on mastery levels"""
        # Identify relevant KCs for this question
        relevant_kcs = self.kc_manager.identify_relevant_kcs(teacher_message)
        
        # Build mastery info string
        mastery_info = self.build_mastery_info(relevant_kcs)
        
        # Get conversation history string
        history_str = self.get_conversation_history_string()
        
        # Build the full prompt
        full_prompt = self.build_full_prompt(teacher_message, mastery_info, history_str)
        
        try:
            # Call OpenAI API with current format
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": full_prompt},
                    {"role": "user", "content": teacher_message}
                ],
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )
            
            student_response = response.choices[0].message.content.strip()
            
            # Add to conversation history
            self.add_to_history("Teacher", teacher_message)
            self.add_to_history("Student", student_response)
            
            return student_response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm having trouble thinking right now. Could you repeat that?"
    
    def build_mastery_info(self, relevant_kcs: List) -> str:
        """Build mastery information string for the prompt"""
        if not relevant_kcs:
            return "No specific knowledge components identified for this question."
        
        mastery_lines = []
        for kc_id, mastery in relevant_kcs:
            kc_data = self.kc_manager.kc_data[kc_id]
            mastery_lines.append(f"- {kc_data['name']}: {mastery}% mastery")
        
        return "\n".join(mastery_lines)
    
    def build_full_prompt(self, teacher_message: str, mastery_info: str, history_str: str) -> str:
        """Build the complete prompt for the AI"""
        base_prompt = self.prompts['base'].format(
            conversation_history=history_str,
            mastery_info=mastery_info,
            teacher_message=teacher_message
        )
        
        # Add mastery-specific guidance
        relevant_kcs = self.kc_manager.identify_relevant_kcs(teacher_message)
        mastery_guidance = self.get_mastery_guidance(relevant_kcs)
        
        return f"{base_prompt}\n\n{mastery_guidance}"
    
    def get_mastery_guidance(self, relevant_kcs: List) -> str:
        """Get mastery-specific guidance for the response"""
        if not relevant_kcs:
            return ""
        
        # Determine the primary mastery level to use
        mastery_levels = [mastery for _, mastery in relevant_kcs]
        primary_mastery = min(mastery_levels) if mastery_levels else 50
        
        if primary_mastery == 0:
            return self.prompts['mastery_0']
        elif primary_mastery <= 50:
            return self.prompts['mastery_50']
        else:
            return self.prompts['mastery_100']
    
    def add_to_history(self, speaker: str, message: str):
        """Add message to conversation history"""
        self.conversation_history.append(f"{speaker}: {message}")
        # Keep only last 10 exchanges to avoid token limits
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def get_conversation_history_string(self) -> str:
        """Get conversation history as string"""
        if not self.conversation_history:
            return "This is the start of the conversation."
        return "\n".join(self.conversation_history[-10:])  # Last 5 exchanges
    
    def update_mastery(self, kc_id: str, new_mastery: int):
        """Update mastery level for a knowledge component"""
        self.kc_manager.update_kc_mastery(kc_id, new_mastery)
    
    def get_current_mastery_status(self) -> Dict:
        """Get current mastery status for all KCs"""
        return {kc_id: data['mastery'] for kc_id, data in self.kc_manager.get_all_kcs().items()}
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []