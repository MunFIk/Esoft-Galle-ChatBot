import requests
import json
import time

# Base URL for the chatbot
BASE_URL = "http://localhost:5000"

def test_chatbot():
    print("Starting chatbot tests...\n")
    
    # Create a session to maintain context across requests
    session = requests.Session()
    
    def send_message(message):
        """Helper function to send a message to the chatbot"""
        response = session.post(
            f"{BASE_URL}/get_response",
            json={"message": message}
        )
        return response.json()["response"]

    # Test 1: Basic Greeting and Course Listing
    print("Test 1: Basic Greeting and Course Listing")
    print("User: Hi")
    print("Bot:", send_message("Hi"))
    time.sleep(1)
    
    print("\nUser: Tell me about courses")
    print("Bot:", send_message("Tell me about courses"))
    time.sleep(1)

    # Test 2: Course Details Flow
    print("\nTest 2: Course Details Flow")
    print("User: Tell me about Diploma in English Language")
    print("Bot:", send_message("Tell me about Diploma in English Language"))
    time.sleep(1)
    
    print("\nUser: What qualifications do I need?")
    print("Bot:", send_message("What qualifications do I need?"))
    time.sleep(1)
    
    print("\nUser: What about fees?")
    print("Bot:", send_message("What about fees?"))
    time.sleep(1)
    
    print("\nUser: When are the classes?")
    print("Bot:", send_message("When are the classes?"))
    time.sleep(1)

    # Test 3: Context Maintenance
    print("\nTest 3: Context Maintenance")
    print("User: Tell me about Bachelor of Business Management")
    print("Bot:", send_message("Tell me about Bachelor of Business Management"))
    time.sleep(1)
    
    print("\nUser: What qualifications do I need?")
    print("Bot:", send_message("What qualifications do I need?"))
    time.sleep(1)
    
    print("\nUser: What about fees?")
    print("Bot:", send_message("What about fees?"))
    time.sleep(1)

    # Test 4: Career and Accreditation
    print("\nTest 4: Career and Accreditation")
    print("User: What can I do after completing?")
    print("Bot:", send_message("What can I do after completing?"))
    time.sleep(1)
    
    print("\nUser: Is this course valid?")
    print("Bot:", send_message("Is this course valid?"))
    time.sleep(1)

    # Test 5: Module and Lecturer Information
    print("\nTest 5: Module and Lecturer Information")
    print("User: What will I learn?")
    print("Bot:", send_message("What will I learn?"))
    time.sleep(1)
    
    print("\nUser: Who teaches this course?")
    print("Bot:", send_message("Who teaches this course?"))
    time.sleep(1)

    # Test 6: Contact Information
    print("\nTest 6: Contact Information")
    print("User: How can I contact you?")
    print("Bot:", send_message("How can I contact you?"))
    time.sleep(1)

    # Test 7: FAQ
    print("\nTest 7: FAQ")
    print("User: Do you offer online classes?")
    print("Bot:", send_message("Do you offer online classes?"))
    time.sleep(1)
    
    print("\nUser: What are your opening hours?")
    print("Bot:", send_message("What are your opening hours?"))
    time.sleep(1)

    # Test 8: Small Talk
    print("\nTest 8: Small Talk")
    print("User: How are you?")
    print("Bot:", send_message("How are you?"))
    time.sleep(1)
    
    print("\nUser: What can you do?")
    print("Bot:", send_message("What can you do?"))
    time.sleep(1)

    print("\nAll tests completed!")

if __name__ == "__main__":
    test_chatbot() 