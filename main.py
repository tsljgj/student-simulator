#!/usr/bin/env python3
"""
Student-Tutor Simulator
A system that simulates a student with varying knowledge mastery levels
"""

import sys
from config import Config
from student_simulator import StudentSimulator

def print_welcome():
    """Print welcome message and instructions"""
    print("="*60)
    print("STUDENT-TUTOR SIMULATOR")
    print("="*60)
    print("This system simulates a student with varying knowledge mastery.")
    print("You are the teacher/tutor, and the AI will respond as a student.")
    print("\nCommands:")
    print("  /help     - Show this help message")
    print("  /status   - Show current knowledge mastery levels")
    print("  /update   - Update a knowledge component mastery")
    print("  /reset    - Reset conversation history")
    print("  /quit     - Exit the program")
    print("\nStart by asking the student a question!")
    print("="*60)

def print_status(simulator):
    """Print current mastery status"""
    print("\nCURRENT KNOWLEDGE MASTERY LEVELS:")
    print("-" * 40)
    mastery_status = simulator.get_current_mastery_status()
    for kc_id, mastery in mastery_status.items():
        kc_data = simulator.kc_manager.get_all_kcs()[kc_id]
        status_icon = "✓" if mastery == 100 else "~" if mastery == 50 else "✗"
        print(f"{status_icon} {kc_data['name']}: {mastery}%")
    print("-" * 40)

def update_mastery(simulator):
    """Interactive mastery update"""
    print("\nAVAILABLE KNOWLEDGE COMPONENTS:")
    all_kcs = simulator.kc_manager.get_all_kcs()
    kc_list = list(all_kcs.keys())
    
    for i, kc_id in enumerate(kc_list, 1):
        current_mastery = all_kcs[kc_id]['mastery']
        print(f"{i}. {all_kcs[kc_id]['name']} (currently {current_mastery}%)")
    
    try:
        choice = input("\nEnter the number of the KC to update (or 'cancel'): ").strip()
        if choice.lower() == 'cancel':
            return
        
        kc_index = int(choice) - 1
        if 0 <= kc_index < len(kc_list):
            kc_id = kc_list[kc_index]
            kc_name = all_kcs[kc_id]['name']
            
            new_mastery = input(f"Enter new mastery level for '{kc_name}' (0, 50, or 100): ").strip()
            
            if new_mastery in ['0', '50', '100']:
                simulator.update_mastery(kc_id, int(new_mastery))
                print(f"✓ Updated {kc_name} to {new_mastery}% mastery")
            else:
                print("Invalid mastery level. Use 0, 50, or 100.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    """Main application loop"""
    try:
        # Validate configuration
        Config.validate()
        
        # Initialize the student simulator
        print("Initializing student simulator...")
        simulator = StudentSimulator()
        
        # Print welcome message
        print_welcome()
        
        # Main conversation loop
        while True:
            try:
                # Get teacher input
                teacher_input = input("\nTeacher: ").strip()
                
                if not teacher_input:
                    continue
                
                # Handle commands
                if teacher_input.startswith('/'):
                    command = teacher_input.lower()
                    
                    if command == '/help':
                        print_welcome()
                    elif command == '/status':
                        print_status(simulator)
                    elif command == '/update':
                        update_mastery(simulator)
                    elif command == '/reset':
                        simulator.reset_conversation()
                        print("✓ Conversation history reset")
                    elif command == '/quit':
                        print("Goodbye!")
                        break
                    else:
                        print("Unknown command. Type /help for available commands.")
                    continue
                
                # Generate student response
                print("Student: ", end="", flush=True)
                student_response = simulator.generate_response(teacher_input)
                print(student_response)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue
                
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please make sure you have set the OPENAI_API_KEY environment variable.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()