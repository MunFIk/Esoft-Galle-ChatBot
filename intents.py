import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

intents = {
    "list_courses": [
        "list courses",
        "what courses are available",
        "show me courses",
        "what programs do you offer",
        "available programs",
        "courses details",
        "tell me about courses",
        "course list",
        "all your courses",
        "what courses do you have",
        "can you list courses",
        "which courses are there"
    ],
    "course_details": [
        "tell me about [course]",
        "what is [course]",
        "information about [course]",
        "details of [course]",
        "describe [course]",
        "explain [course]",
        "what does [course] cover",
        "what will i learn in [course]"
    ],
    "course_fees": [
        "how much is [course]",
        "what is the fee for [course]",
        "cost of [course]",
        "price of [course]",
        "payment for [course]",
        "fee structure of [course]",
        "installment plans for [course]",
        "payment options for [course]"
    ],
    "course_requirements": [
        "what do i need for [course]",
        "requirements for [course]",
        "qualifications for [course]",
        "eligibility for [course]",
        "prerequisites for [course]",
        "what qualifications do i need for [course]"
    ],
    "career_paths": [
        "what can i do after [course]",
        "job opportunities after [course]",
        "career options after [course]",
        "future prospects of [course]",
        "what jobs can i get after [course]",
        "employment opportunities after [course]"
    ],
    "contact_info": [
        "how to contact you",
        "what is your address",
        "where are you located",
        "phone number",
        "email address",
        "contact details",
        "how to reach you",
        "location of esoft galle"
    ],
    "registration": [
        "how to register",
        "registration process",
        "how to enroll",
        "admission process",
        "how to join",
        "how to apply",
        "what documents needed for registration",
        "registration requirements"
    ],
    "scholarships": [
        "do you offer scholarships",
        "scholarship information",
        "financial aid",
        "student discounts",
        "fee concessions",
        "how to get scholarship",
        "scholarship requirements",
        "financial assistance"
    ],
    "online_classes": [
        "do you have online classes",
        "online learning options",
        "distance learning",
        "virtual classes",
        "remote learning",
        "online course availability",
        "can i study online"
    ],
    "job_placement": [
        "do you help with jobs",
        "placement assistance",
        "career guidance",
        "job support",
        "employment help",
        "do you provide job placement",
        "career services"
    ],
    "certificates": [
        "do you provide certificates",
        "certification process",
        "course completion certificate",
        "accreditation",
        "qualification recognition",
        "certificate details",
        "how to get certificate"
    ],
    "branch_transfer": [
        "can i transfer to another branch",
        "branch transfer process",
        "change branch",
        "transfer between branches",
        "relocate to different branch",
        "switch branch"
    ],
    "opening_hours": [
        "what are your timings",
        "when are you open",
        "working hours",
        "branch hours",
        "operating hours",
        "when can i visit",
        "what time do you open"
    ]
}

def get_best_intent(user_input):
    doc = nlp(user_input.lower())
    best_intent = None
    best_score = 0
    
    for intent, patterns in intents.items():
        for pattern in patterns:
            pattern_doc = nlp(pattern)
            similarity = doc.similarity(pattern_doc)
            if similarity > best_score:
                best_score = similarity
                best_intent = intent
    
    # Threshold for intent matching
    if best_score < 0.5:
        return None
    
    return best_intent
