from flask import Blueprint, render_template, request, jsonify, session
import json
import os
from intents import get_best_intent
import random

chatbot_bp = Blueprint('chatbot', __name__)

# Load knowledge base (includes courses + contact + FAQ + small_talk)
basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, 'data', 'knowledge_base.json'), 'r') as f:
    knowledge_base = json.load(f)

courses = knowledge_base.get('courses', [])
small_talk = knowledge_base.get('small_talk', {})
faq = knowledge_base.get('faq', [])
contact_info = knowledge_base.get('contact_info', {})

@chatbot_bp.route('/')
def home():
    return render_template('chat.html')

@chatbot_bp.route('/get_response', methods=['POST'])
def get_response():
    # Check if the request has JSON data
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 415
    
    try:
        data = request.get_json()
        user_input = data.get('message', '').lower().strip()
        
        if not user_input:
            return jsonify({'response': "Please provide a message."})

        # Get conversation state from session
        last_course = session.get('last_course', None)
        conversation_state = session.get('conversation_state', 'initial')

        # First check if it's a small talk query
        for category, responses in small_talk.items():
            for response in responses:
                for pattern in response['patterns']:
                    if pattern.lower() in user_input.lower():
                        if isinstance(response['response'], list):
                            session['conversation_state'] = 'initial'
                            return jsonify({'response': random.choice(response['response'])})
                        session['conversation_state'] = 'initial'
                        return jsonify({'response': response['response']})

        # Check FAQ before other intents
        for faq_item in faq:
            if any(pattern.lower() in user_input.lower() for pattern in faq_item.get('patterns', [])):
                session['conversation_state'] = 'initial'
                return jsonify({'response': faq_item['answer'].replace('•', '*')})

        # Check contact info
        if any(keyword in user_input.lower() for keyword in ['contact', 'address', 'phone', 'email', 'location', 'where are you', 'opening hours', 'timings', 'when are you open', 'working hours', 'how can i contact you']):
            session['conversation_state'] = 'initial'
            response = "Here are our contact details:\n\n"
            response += f"🏢 Branch: {contact_info['branch_name']}\n"
            response += f"📍 Address: {contact_info['address']}\n"
            response += f"📞 Phone: {contact_info['phone']}\n"
            response += f"💬 WhatsApp: {contact_info['whatsapp']}\n"
            response += f"📧 Email: {contact_info['email']}\n"
            response += f"🚨 Emergency Contact: {contact_info['emergency_contact']}\n\n"
            response += "🌐 Social Media:\n"
            for platform, link in contact_info['social_media'].items():
                response += f"{platform.capitalize()}: {link}\n"
            response += "\n⏰ Opening Hours:\n"
            response += "* Monday to Friday: 8:30 AM - 5:30 PM\n"
            response += "* Saturday: 9:00 AM - 1:00 PM\n"
            response += "* Sunday: Closed\n"
            return jsonify({'response': response})

        # Check if it's a course listing request (with typo tolerance)
        course_listing_keywords = ['list courses', 'available courses', 'what courses', 'show courses', 'programs', 'offer', 'tell me about courses', 'show me courses', 'what courses do you have', 'all courses', 'couese', 'cours', 'cource']
        if any(keyword in user_input.lower() for keyword in course_listing_keywords):
            course_list = "\n".join([f"* {course['name']}" for course in courses])
            session['conversation_state'] = 'course_listed'
            suggestions = [course['name'] for course in courses]
            return jsonify({
                'response': f"Here are our available courses:\n\n{course_list}\n\nWhich course would you like to know more about? I can tell you about:\n* Course details\n* Entry requirements\n* Fees and payment plans\n* Career opportunities\n* Class schedules\n* Course accreditation",
                'suggestions': suggestions
            })

        # Handle follow-up questions if we have a last course
        if last_course and any(keyword in user_input.lower() for keyword in ['this', 'that', 'it', 'the course', 'course', 'qualification', 'fee', 'schedule', 'module', 'career', 'accreditation', 'what', 'how', 'when', 'who', 'where', 'tell me about', 'details', 'information', 'wanna know about', 'valid', 'teaches', 'lecturer']):
            for course in courses:
                if course['name'].lower() == last_course.lower():
                    # Handle specific course queries
                    if any(keyword in user_input.lower() for keyword in ['how much', 'fee', 'cost', 'price', 'payment', 'installment', 'plans', 'course fees']):
                        session['conversation_state'] = 'discussing_fees'
                        response = f"Here are the fee details for {course['name']}:\n\n"
                        response += f"💰 Total Fee: {course['fee']}\n\n"
                        response += "💳 Payment Plans:\n"
                        for plan in course['payment_plans']:
                            response += f"* {plan}\n"
                        response += "\nWould you like to know about:\n* Entry requirements\n* Class schedules\n* Course modules\n* Career opportunities"
                        return jsonify({'response': response})
                    
                    elif any(keyword in user_input.lower() for keyword in ['need', 'require', 'qualification', 'eligibility', 'prerequisites', 'what do i need', 'qualifications', 'entry']):
                        session['conversation_state'] = 'discussing_requirements'
                        response = f"Here are the entry requirements for {course['name']}:\n\n"
                        response += f"📝 {course['requirements']}\n\n"
                        response += "Would you like to know about:\n* Course fees and payment plans\n* Class schedules\n* Course modules\n* Career opportunities"
                        return jsonify({'response': response})
                    
                    elif any(keyword in user_input.lower() for keyword in ['after', 'career', 'job', 'future', 'what can i do', 'opportunities', 'complete', 'finish']):
                        session['conversation_state'] = 'discussing_careers'
                        response = f"After completing {course['name']}, you can pursue these career paths:\n\n"
                        careers = course['career_paths'].split(', ')
                        for career in careers:
                            response += f"* {career}\n"
                        response += "\nWould you like to know about:\n* Entry requirements\n* Course fees\n* Class schedules\n* Course modules"
                        return jsonify({'response': response})
                    
                    elif any(keyword in user_input.lower() for keyword in ['module', 'lecturer', 'teacher', 'instructor', 'what will i learn', 'what do i learn', 'subjects', 'topics', 'syllabus', 'who teaches', 'who is the lecturer']):
                        session['conversation_state'] = 'discussing_modules'
                        response = f"Here are the course modules and lecturer details for {course['name']}:\n\n"
                        response += "📚 Modules:\n"
                        modules = course['modules'].split(', ')
                        for module in modules:
                            response += f"* {module}\n"
                        response += f"\n👨‍🏫 Lecturer: {course['lecturer']}\n\n"
                        response += "Would you like to know about:\n* Entry requirements\n* Course fees\n* Class schedules\n* Career opportunities"
                        return jsonify({'response': response})
                    
                    elif any(keyword in user_input.lower() for keyword in ['schedule', 'time', 'when', 'class', 'lecture', 'day', 'week']):
                        session['conversation_state'] = 'discussing_schedule'
                        response = f"Here's the schedule information for {course['name']}:\n\n"
                        response += "📅 Class Schedule:\n"
                        response += "* Weekday Classes: Monday to Friday, 9:00 AM - 4:00 PM\n"
                        response += "* Weekend Classes: Saturday, 9:00 AM - 1:00 PM\n"
                        response += "* Online Classes: Flexible timing with recorded sessions\n\n"
                        response += "Would you like to know about:\n* Entry requirements\n* Course fees\n* Course modules\n* Career opportunities"
                        return jsonify({'response': response})
                    
                    elif any(keyword in user_input.lower() for keyword in ['valid', 'approved', 'accredited', 'recognition', 'certification', 'is this course valid', 'is it valid']):
                        session['conversation_state'] = 'discussing_accreditation'
                        response = f"About {course['name']} accreditation:\n\n"
                        response += "✅ This course is:\n"
                        response += "* Accredited by the Tertiary and Vocational Education Commission (TVEC)\n"
                        response += "* Recognized by the University Grants Commission (UGC)\n"
                        response += "* Accepted by local and international employers\n\n"
                        response += "Would you like to know about:\n* Entry requirements\n* Course fees\n* Class schedules\n* Career opportunities"
                        return jsonify({'response': response})
                    
                    # Handle general course details request
                    elif any(keyword in user_input.lower() for keyword in ['details', 'description', 'about', 'tell me about', 'what is', 'explain', 'wanna know about']):
                        response = f"Here's a brief overview of {course['name']}:\n\n"
                        response += f"📖 Description: {course['description']}\n"
                        response += f"⏱️ Duration: {course['duration']}\n\n"
                        response += "Would you like to know more about:\n"
                        response += "* Entry requirements\n"
                        response += "* Course fees and payment plans\n"
                        response += "* Class schedules\n"
                        response += "* Course modules and lecturer\n"
                        response += "* Career opportunities\n"
                        response += "* Course accreditation\n\n"
                        response += "Just ask me what you'd like to know!"
                        return jsonify({'response': response})

        # Check for new course mentions
        for course in courses:
            if course['name'].lower() in user_input.lower():
                # Store the current course in session for context
                session['last_course'] = course['name']
                session['conversation_state'] = 'discussing_course'
                
                # Handle specific course queries
                if any(keyword in user_input.lower() for keyword in ['how much', 'fee', 'cost', 'price', 'payment', 'installment', 'plans', 'course fees']):
                    session['conversation_state'] = 'discussing_fees'
                    response = f"Here are the fee details for {course['name']}:\n\n"
                    response += f"💰 Total Fee: {course['fee']}\n\n"
                    response += "💳 Payment Plans:\n"
                    for plan in course['payment_plans']:
                        response += f"* {plan}\n"
                    response += "\nWould you like to know about:\n* Entry requirements\n* Class schedules\n* Course modules\n* Career opportunities"
                    return jsonify({'response': response})
                
                # If just the course name is mentioned, show overview
                response = f"Here's a brief overview of {course['name']}:\n\n"
                response += f"📖 Description: {course['description']}\n"
                response += f"⏱️ Duration: {course['duration']}\n\n"
                response += "Would you like to know more about:\n"
                response += "* Entry requirements\n"
                response += "* Course fees and payment plans\n"
                response += "* Class schedules\n"
                response += "* Course modules and lecturer\n"
                response += "* Career opportunities\n"
                response += "* Course accreditation\n\n"
                response += "Just ask me what you'd like to know!"
                return jsonify({'response': response})

        # Check for casual responses
        casual_responses = knowledge_base.get('casual_responses', {})
        for category, responses in casual_responses.items():
            for keyword, response in responses.items():
                if keyword.lower() in user_input.lower():
                    return jsonify({'response': response})

        # If no intent is matched and no other conditions are met, use a random fallback response
        fallback_responses = [
            "I'm not sure I understand. Could you please rephrase your question?",
            "I'm here to help with course information, contact details, and general inquiries about ESOFT Galle.",
            "Would you like to know about our courses, contact information, or something else?",
            "I can help you with information about our courses, contact details, and general inquiries."
        ]
        suggestions = [
            "Tell me about courses",
            "Contact information",
            "Opening hours",
            "Online classes"
        ]
        return jsonify({
            'response': random.choice(fallback_responses),
            'suggestions': suggestions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
