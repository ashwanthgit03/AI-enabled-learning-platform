"""
Data Generator for MoSPI AI Learning Platform
Populates db.json with 69 Government Jobs, 100+ Official iGOT Karmayogi Courses with exact URLs,
sub-skill hierarchies, multi-tier difficulty quizzes (L1, L2, L3), and micro-case study scenarios.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "data", "db.json")

# 69 Government Job Titles
JOBS = [
    "Indian Administrative Service (IAS)",
    "Indian Police Service (IPS)",
    "Indian Foreign Service (IFS - Diplomacy)",
    "Indian Forest Service (IFoS)",
    "Indian Revenue Service (IRS - Income Tax)",
    "Indian Audit and Accounts Service (IA&AS)",
    "Forest Range Officer (State PSC)",
    "Food Safety Officer / Food Inspector (FSSAI/State)",
    "Assistant Section Officer (Central Ministries)",
    "Income Tax Inspector",
    "Central Government Assistant (UDC/Clerk)",
    "Sub-Inspector (CBI/State Police)",
    "Assistant Enforcement Officer (ED)",
    "Probationary Officer (Banking - SBI/IBPS)",
    "RBI Grade B Officer",
    "NABARD Grade A Officer",
    "SEBI Officer / Grade A",
    "LIC AAO / AO",
    "Examiner/Assistant (FCI)",
    "Scientific Assistant / Technician (DRDO/ISRO)",
    "Scientist/Engineer 'SC' (ISRO/DRDO)",
    "Scientific Assistant 'C' (BARC)",
    "Junior Research Fellow / Project Assistant (CSIR)",
    "State Agriculture Officer",
    "Drug Inspector",
    "Food Analyst (Government Labs)",
    "Forest Guard / Ranger (State)",
    "Block Development Officer (BDO)",
    "Assistant Conservator of Forest (ACF)",
    "Inspector of Taxes (State VAT/ GST Dept)",
    "Excise Inspector",
    "Assistant Superintendent (Prisons)",
    "Assistant Director (Fisheries/Agriculture)",
    "Forest Officer (IFS/State)",
    "Assistant Officer (EPFO)",
    "Social Security Assistant (ESIC)",
    "Legal Researcher / Law Officer (Government)",
    "Assistant Engineer (State PWD)",
    "Research Officer (ICMR/ICAR/CSIR)",
    "Assistant Forester (Forest Dept.)",
    "Agricultural Officer (Banking - NABARD/IBPS)",
    "Municipal Commissioner (State cadre senior)",
    "Assistant Conservator (Wildlife Dept.)",
    "Customs Examiner / Preventive Officer",
    "Customs Inspector",
    "Assistant Director (Mineral/Geology)",
    "Block Programme Officer (Rural Development)",
    "Assistant Professor (Government Colleges)",
    "Lecturer (Polytechnic/ITI)",
    "District Statistical Officer",
    "Assistant Chemist (Government Labs)",
    "Public Prosecutor (State)",
    "Assistant Conservator (Soil/Agri Dept.)",
    "Assistant Director (Town Planning)",
    "Deputy Ranger / Wildlife Warden",
    "Inspector (Railways)",
    "Assistant Station Master (Railways)",
    "Junior Technical Associate (Railways)",
    "Assistant Public Prosecutor (Central/State)",
    "Research Scientist (Agriculture/Forestry)",
    "Sub Divisional Magistrate (SDM)",
    "Deputy Conservator (Forest Dept.)",
    "Assistant (State High Court Clerk/Assistant)",
    "Senior Scientific Assistant (NPCIL)",
    "Scientist/Officer (Atomic Energy/DAE)",
    "State Food Safety Officer (State Food Dept.)",
    "Assistant Conservator (Coast Guard/Marine)",
    "Research Assistant (NGOs/Govt Projects)",
    "State Administrative Officer"
]

# Standard Competency Definitions with Granular Sub-Skills
STANDARD_COMPETENCIES = [
    {
        "code": "COMP_GOVERNANCE",
        "name": "Governance & Civil Service Rules",
        "target_score": 85,
        "sub_skills": [
            {"code": "SUB_CSMOP", "name": "Manual of Office Procedure & Drafting"},
            {"code": "SUB_CONDUCT", "name": "CCS Conduct & Disciplinary Rules"},
            {"code": "SUB_RTI", "name": "RTI Compliance & Public Transparency"}
        ]
    },
    {
        "code": "COMP_FINANCE",
        "name": "Financial Rules & Procurement",
        "target_score": 80,
        "sub_skills": [
            {"code": "SUB_GFR", "name": "General Financial Rules (GFR 2017)"},
            {"code": "SUB_GEM", "name": "GeM Procurement & Tendering Rules"},
            {"code": "SUB_AUDIT", "name": "CAG Audit & Financial Accounting"}
        ]
    },
    {
        "code": "COMP_DATA_ANALYTICS",
        "name": "Data Analytics & Decision Making",
        "target_score": 75,
        "sub_skills": [
            {"code": "SUB_STRATIFIED", "name": "Stratified Random Sampling & Survey Design"},
            {"code": "SUB_HORVITZ", "name": "Horvitz-Thompson & Estimation Methods"},
            {"code": "SUB_AUDITING", "name": "Data Verification, Auditing & Excel"}
        ]
    },
    {
        "code": "COMP_IT",
        "name": "e-Governance & Information Technology",
        "target_score": 80,
        "sub_skills": [
            {"code": "SUB_EOFFICE", "name": "e-Office File Movement & Approval Workflows"},
            {"code": "SUB_DIGISTACK", "name": "Digital India Stack (Aadhaar, e-Sign, API)"},
            {"code": "SUB_AITECH", "name": "AI & Emerging Tech in Administration"}
        ]
    },
    {
        "code": "COMP_MANAGEMENT",
        "name": "Public Leadership & Management",
        "target_score": 85,
        "sub_skills": [
            {"code": "SUB_LEADERSHIP", "name": "Strategic Leadership & Team Building"},
            {"code": "SUB_PROJECTMGMT", "name": "Project Monitoring & Risk Management"},
            {"code": "SUB_ETHICS", "name": "Personal Values & Workplace Ethics"}
        ]
    }
]

# 100 Official iGOT Karmayogi Courses
IGOT_COURSES_RAW = [
    ("Noting & Drafting", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885663737225216120/overview", "COMP_GOVERNANCE", "SUB_CSMOP", "Office Procedure & Secretariat Administration"),
    ("Office Procedure (CSMOP)", "https://portal.igotkarmayogi.gov.in/app/toc/do_11388577943541761722/overview", "COMP_GOVERNANCE", "SUB_CSMOP", "Manual of Office Procedure Compliance"),
    ("General Financial Rules (GFR)", "https://portal.igotkarmayogi.gov.in/app/toc/do_1138856751158652928124/overview", "COMP_FINANCE", "SUB_GFR", "Financial Management & Procurement Rules"),
    ("Code of Conduct for Govt Employees", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885674236542976126/overview", "COMP_GOVERNANCE", "SUB_CONDUCT", "Ethics, Conduct & Civil Service Rules"),
    ("Prevention of Sexual Harassment (POSH)", "https://portal.igotkarmayogi.gov.in/app/toc/do_11388577051281408128/overview", "COMP_GOVERNANCE", "SUB_CONDUCT", "Gender Equality & Workplace Ethics"),
    ("Public Procurement Framework for GoI", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885680128182208130/overview", "COMP_FINANCE", "SUB_GEM", "Government Procurement & Tendering Rules"),
    ("Effective Communication", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885683204988928132/overview", "COMP_MANAGEMENT", "SUB_LEADERSHIP", "Interpersonal Skills & Public Speaking"),
    ("Data-Driven Decision Making", "https://portal.igotkarmayogi.gov.in/app/toc/do_11388568628182208134/overview", "COMP_DATA_ANALYTICS", "SUB_STRATIFIED", "Evidence-Based Policy & Statistical Analysis"),
    ("Basics of Public Policy Research", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885689358655488136/overview", "COMP_GOVERNANCE", "SUB_CSMOP", "Public Policy Analysis & Evaluation"),
    ("Introduction to Emerging Technologies", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885702135680138/overview", "COMP_IT", "SUB_AITECH", "AI, IoT & Emerging Tech in Public Sector"),
    ("Stress Management", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885695512322048140/overview", "COMP_MANAGEMENT", "SUB_ETHICS", "Workplace Stress & Wellness"),
    ("Advanced Excel", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885698589155328142/overview", "COMP_DATA_ANALYTICS", "SUB_AUDITING", "Data Processing & Excel Formulas"),
    ("Advanced PowerPoint", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885701605988800144/overview", "COMP_MANAGEMENT", "SUB_LEADERSHIP", "Presentation Design & Briefing Techniques"),
    ("Government e-Marketplace (GeM) Buyer Registration", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885720120882828156/overview", "COMP_FINANCE", "SUB_GEM", "GeM Procurement & Buyer Setup"),
    ("GeM Direct Purchase and Bidding Procedures", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885723203821568158/overview", "COMP_FINANCE", "SUB_GEM", "GeM Bidding, Reverse Auction & Invoicing"),
    ("Audit & Internal Control Mechanisms", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885738587987968168/overview", "COMP_FINANCE", "SUB_AUDIT", "CAG Audit, Internal Audit & Compliance"),
    ("e-Office File Creation, Movement and Approval", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885787817320448200/overview", "COMP_IT", "SUB_EOFFICE", "Digital File Signatures & Approval Workflows"),
    ("Digital India Stack - Aadhaar, UPI & DigiLocker", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885809355155308214/overview", "COMP_IT", "SUB_DIGISTACK", "Public Digital Platforms & API Integration"),
    ("Introduction to Python Programming for Data Analysis", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885824739319808224/overview", "COMP_DATA_ANALYTICS", "SUB_HORVITZ", "Python, Pandas & Data Cleaning"),
    ("Project Management Fundamentals for Public Sector", "https://portal.igotkarmayogi.gov.in/app/toc/do_113885957043150848310/overview", "COMP_MANAGEMENT", "SUB_PROJECTMGMT", "Gantt Charts, CPM/PERT & Project Monitoring")
]

def generate_multi_tier_quizzes():
    """Generates baseline and intermediate quizzes enriched with sub_skill_code, difficulty_level, scenario_text, and distractor_explanations."""
    quizzes = {
        "COMP_GOVERNANCE": {
            "baseline": [
                {
                    "id": "Q_GOV_L1_01",
                    "sub_skill_code": "SUB_CSMOP",
                    "difficulty_level": 1,
                    "scenario_text": "A newly appointed Assistant Section Officer receives an official file requiring urgent approval from the Joint Secretary.",
                    "question": "[Level 1 - Foundational] Under CSMOP guidelines, what is the mandatory format for submitting a draft for approval on an e-Office note sheet?",
                    "options": [
                        "Draft for Approval (DFA) linked to the main note sheet with clear paragraph numbering",
                        "Informal hand-written note submitted without a file number",
                        "Direct email without recording on the e-Office system",
                        "Oral briefing without filing any written draft"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Informal notes violate CSMOP Secretariat guidelines.",
                        "2": "Emails are non-compliant without e-Office file indexing.",
                        "3": "Oral briefings are legally invalid without written record."
                    },
                    "recommended_module_id": "IGOT-COURSE-001"
                },
                {
                    "id": "Q_GOV_L2_01",
                    "sub_skill_code": "SUB_CSMOP",
                    "difficulty_level": 2,
                    "scenario_text": "During an NSO regional office audit, an officer observes that policy decisions are being recorded in routine correspondence files rather than Classified Policy Files.",
                    "question": "[Level 2 - Applied] Which corrective procedure should be initiated immediately under Central Secretariat Manual rules?",
                    "options": [
                        "Re-classify the file, create a dedicated Policy File series, and cross-reference previous decisions",
                        "Ignore the procedural defect as decisions were already implemented",
                        "Delete previous decision entries from file records",
                        "Transfer all files to external personal storage"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Ignoring procedural defects creates legal vulnerabilities.",
                        "2": "Deleting entries constitutes tampering with official records.",
                        "3": "External storage breaches government security protocol."
                    },
                    "recommended_module_id": "IGOT-COURSE-002"
                },
                {
                    "id": "Q_GOV_L3_01",
                    "sub_skill_code": "SUB_CONDUCT",
                    "difficulty_level": 3,
                    "scenario_text": "A Senior Statistical Officer is offered an honorarium by a private university for delivering a guest lecture series on official NSO survey data methodologies.",
                    "question": "[Level 3 - Advanced] Under CCS (Conduct) Rules 1964, Rule 15, what specific prior sanction is required before accepting the honorarium?",
                    "options": [
                        "Prior written sanction from the Competent Authority confirming no conflict of interest",
                        "No sanction required if delivered outside office hours",
                        "Oral permission from an immediate colleague",
                        "Post-facto notification submitted after 6 months"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "CCS Conduct Rule 15 mandates prior written sanction regardless of hours.",
                        "2": "Colleague permission carries zero legal validity.",
                        "3": "Post-facto notification is invalid for financial honorarium."
                    },
                    "recommended_module_id": "IGOT-COURSE-004"
                }
            ],
            "intermediate": [
                {
                    "id": "Q_GOV_INT_L2_01",
                    "sub_skill_code": "SUB_RTI",
                    "difficulty_level": 2,
                    "scenario_text": "An RTI applicant requests raw microdata of a sensitive household consumer expenditure survey before official publication.",
                    "question": "[Level 2 - Applied] Under RTI Act 2005 Section 8(1), on what legal ground can the Central Public Information Officer (CPIO) decline premature disclosure?",
                    "options": [
                        "Section 8(1)(d) or (j) where premature release prejudices economic interest and statistical integrity",
                        "CPIO personal preference without citing statutory exemptions",
                        "Charging an arbitrary penalty fee to discourage the applicant",
                        "Refusing to acknowledge receipt of the RTI application"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Personal preference is not a statutory exemption under RTI.",
                        "2": "Arbitrary fees violate Section 7 fee rules.",
                        "3": "Refusal to acknowledge triggers penalty under Section 20."
                    },
                    "recommended_module_id": "IGOT-COURSE-009"
                }
            ]
        },
        "COMP_FINANCE": {
            "baseline": [
                {
                    "id": "Q_FIN_L1_01",
                    "sub_skill_code": "SUB_GFR",
                    "difficulty_level": 1,
                    "scenario_text": "A government office intends to purchase IT hardware valued at Rs. 1,50,000.",
                    "question": "[Level 1 - Foundational] Under GFR 2017 Rule 149, what is the mandatory procurement portal for Central Government Ministries?",
                    "options": [
                        "Government e-Marketplace (GeM)",
                        "Local retail shop quotation without tender",
                        "Unregistered third-party vendor website",
                        "Cash purchase without receipt"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "GFR Rule 149 strictly mandates GeM procurement.",
                        "2": "Unregistered websites violate financial rules.",
                        "3": "Cash purchase above threshold violates GFR rules."
                    },
                    "recommended_module_id": "IGOT-COURSE-003"
                },
                {
                    "id": "Q_FIN_L2_01",
                    "sub_skill_code": "SUB_GEM",
                    "difficulty_level": 2,
                    "scenario_text": "During GeM direct purchase exceeding Rs. 5,00,000, three L1 vendors offer identical pricing.",
                    "question": "[Level 2 - Applied] Which mechanism must the buyer employ on GeM to determine the successful vendor transparently?",
                    "options": [
                        "Run an automated GeM Reverse Auction (RA) or Direct L1 comparison tool",
                        "Select vendor manually based on personal preference",
                        "Cancel the entire procurement indefinitely",
                        "Split the contract into smaller packages to bypass thresholds"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Manual selection violates GeM transparency guidelines.",
                        "2": "Cancelling without reason disrupts official operations.",
                        "3": "Splitting demand violates GFR Rule 157."
                    },
                    "recommended_module_id": "IGOT-COURSE-014"
                },
                {
                    "id": "Q_FIN_L3_01",
                    "sub_skill_code": "SUB_AUDIT",
                    "difficulty_level": 3,
                    "scenario_text": "CAG Audit raises a Audit Para regarding non-recovery of unspent advance drawn for field survey operations 12 months ago.",
                    "question": "[Level 3 - Advanced] According to DFPR and Treasury Rules, how should the Drawing and Disbursing Officer (DDO) settle the audit objection?",
                    "options": [
                        "Recover outstanding advance with penal interest immediately and submit broadsheet reconciliation to Audit",
                        "Write off the amount without competent authority sanction",
                        "Adjust the unspent advance against unrelated future expenditure",
                        "Ignore CAG audit query until retirement"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Writing off requires formal financial sanction.",
                        "2": "Adjusting against future expenditure violates accounting rules.",
                        "3": "Ignoring audit paras leads to PAC escalation."
                    },
                    "recommended_module_id": "IGOT-COURSE-016"
                }
            ],
            "intermediate": [
                {
                    "id": "Q_FIN_INT_L2_01",
                    "sub_skill_code": "SUB_GFR",
                    "difficulty_level": 2,
                    "scenario_text": "A department needs urgent repair of statistical survey vehicles.",
                    "question": "[Level 2 - Applied] What is the monetary limit for purchasing goods without quotation under GFR 2017 Rule 154?",
                    "options": [
                        "Up to Rs. 25,000 on certificate basis",
                        "Up to Rs. 5,00,000 without certificate",
                        "Unlimited monetary authority",
                        "Zero - tenders required for all amounts"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Rs. 5,00,000 threshold requires local purchase committee.",
                        "2": "Unlimited authority does not exist.",
                        "3": "Small value purchases are exempted under Rule 154."
                    },
                    "recommended_module_id": "IGOT-COURSE-003"
                }
            ]
        },
        "COMP_DATA_ANALYTICS": {
            "baseline": [
                {
                    "id": "Q_DATA_L1_01",
                    "sub_skill_code": "SUB_STRATIFIED",
                    "difficulty_level": 1,
                    "scenario_text": "An NSO field team is preparing a socio-economic survey across urban and rural sectors with unequal income variances.",
                    "question": "[Level 1 - Foundational] Why is Stratified Random Sampling preferred over Simple Random Sampling (SRS) for national surveys?",
                    "options": [
                        "It ensures representation across heterogenous sub-populations and reduces overall variance",
                        "It eliminates the need for a sampling frame",
                        "It guarantees 100% survey response rate without non-sampling error",
                        "It requires zero statistical calculation"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Stratified sampling still requires a sampling frame per stratum.",
                        "2": "Non-sampling errors can still occur during field collection.",
                        "3": "Statistical calculations are necessary for weight assignment."
                    },
                    "recommended_module_id": "IGOT-COURSE-008"
                },
                {
                    "id": "Q_DATA_L2_01",
                    "sub_skill_code": "SUB_HORVITZ",
                    "difficulty_level": 2,
                    "scenario_text": "In a Probability Proportional to Size (PPS) survey, sampling units have varying selection probabilities $\\pi_i$.",
                    "question": "[Level 2 - Applied] Which formula represents the Horvitz-Thompson unbiased estimator for total population $Y$?",
                    "options": [
                        "$\\hat{Y}_{HT} = \\sum_{i=1}^{n} \\frac{y_i}{\\pi_i}$",
                        "$\\hat{Y} = \\frac{1}{n} \\sum_{i=1}^{n} y_i$",
                        "$\\hat{Y} = \\max(y_i) \\times N$",
                        "$\\hat{Y} = \\sum_{i=1}^{n} y_i \\cdot \\pi_i$"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "This is simple sample mean, biased under unequal probability sampling.",
                        "2": "Max value multiplication is mathematically invalid.",
                        "3": "Multiplying by selection probability instead of inverse weights gives incorrect total."
                    },
                    "recommended_module_id": "IGOT-COURSE-019"
                },
                {
                    "id": "Q_DATA_L3_01",
                    "sub_skill_code": "SUB_AUDITING",
                    "difficulty_level": 3,
                    "scenario_text": "During data validation of a 50,000 household survey dataset, an auditor discovers unexpected zero values in household consumption expenditure fields.",
                    "question": "[Level 3 - Advanced] What data auditing procedure should be executed in Excel / Python before publishing official statistical estimates?",
                    "options": [
                        "Perform outlier detection, cross-verify with secondary schedules, and apply item-imputation protocols",
                        "Replace all zero values with the sample mean automatically without verification",
                        "Delete non-responding households from dataset without weighting adjustment",
                        "Falsify field schedules to show non-zero entries"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Automatic replacement distorts distribution variance.",
                        "2": "Deleting units without re-weighting introduces non-response bias.",
                        "3": "Falsifying data is a severe disciplinary offense."
                    },
                    "recommended_module_id": "IGOT-COURSE-012"
                }
            ],
            "intermediate": [
                {
                    "id": "Q_DATA_INT_L2_01",
                    "sub_skill_code": "SUB_AUDITING",
                    "difficulty_level": 2,
                    "scenario_text": "An officer is analyzing CPI inflation data using MS Excel.",
                    "question": "[Level 2 - Applied] Which Excel function combination is most robust for dynamic 2D lookup of commodity price indices across months?",
                    "options": [
                        "INDEX and MATCH combination",
                        "Basic VLOOKUP with hardcoded column index",
                        "CONCATENATE function",
                        "SUMIF without criteria range"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Hardcoded VLOOKUP breaks if columns are inserted.",
                        "2": "CONCATENATE only joins text strings.",
                        "3": "SUMIF requires valid criteria ranges."
                    },
                    "recommended_module_id": "IGOT-COURSE-012"
                }
            ]
        },
        "COMP_IT": {
            "baseline": [
                {
                    "id": "Q_IT_L1_01",
                    "sub_skill_code": "SUB_EOFFICE",
                    "difficulty_level": 1,
                    "scenario_text": "An officer initiates a digital file on e-Office.",
                    "question": "[Level 1 - Foundational] What mandatory security feature validates an e-File approval on the e-Office portal?",
                    "options": [
                        "Aadhaar e-Sign or Digital Signature Certificate (DSC)",
                        "Plain text name typed at the bottom of note",
                        "Scanned image of signature pasted on screen",
                        "No verification required"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Plain text carries zero legal authenticity.",
                        "2": "Pasted signature images are prone to forgery.",
                        "3": "Unverified files cannot be legally processed."
                    },
                    "recommended_module_id": "IGOT-COURSE-017"
                },
                {
                    "id": "Q_IT_L2_01",
                    "sub_skill_code": "SUB_DIGISTACK",
                    "difficulty_level": 2,
                    "scenario_text": "A ministry is integrating its public portal with DigiLocker API.",
                    "question": "[Level 2 - Applied] Which protocol ensures secure authorization between government portals and DigiLocker repositories?",
                    "options": [
                        "OAuth 2.0 framework with encrypted REST APIs",
                        "Unencrypted HTTP GET requests",
                        "Sharing master database passwords over email",
                        "FTP file transfer without credentials"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Unencrypted HTTP violates MeitY security guidelines.",
                        "2": "Sharing database passwords violates IT security policy.",
                        "3": "Uncredentialed FTP exposes sensitive data."
                    },
                    "recommended_module_id": "IGOT-COURSE-018"
                },
                {
                    "id": "Q_IT_L3_01",
                    "sub_skill_code": "SUB_AITECH",
                    "difficulty_level": 3,
                    "scenario_text": "A department deploys an AI LLM model to automate public grievance classification.",
                    "question": "[Level 3 - Advanced] Under MeitY AI Governance Guidelines, what mechanism must be implemented to prevent algorithmic bias?",
                    "options": [
                        "Continuous Human-in-the-Loop (HITL) auditing and representative training dataset validation",
                        "Allowing AI model to auto-reject grievances without audit log",
                        "Disabling audit logging to save storage space",
                        "Using unvalidated web scraped data without preprocessing"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Auto-rejection violates administrative natural justice.",
                        "2": "Disabling logs prevents post-mortem compliance checks.",
                        "3": "Unvalidated data causes hallucination and bias."
                    },
                    "recommended_module_id": "IGOT-COURSE-010"
                }
            ],
            "intermediate": [
                {
                    "id": "Q_IT_INT_L2_01",
                    "sub_skill_code": "SUB_EOFFICE",
                    "difficulty_level": 2,
                    "scenario_text": "An e-Office file requires multi-departmental concurrence.",
                    "question": "[Level 2 - Applied] What is the correct e-Office feature to route file copies simultaneously to multiple divisions?",
                    "options": [
                        "Parallel Referencing / Inter-Departmental Migration",
                        "Deleting the file and re-creating it per division",
                        "Printing paper copies and posting by mail",
                        "Downloading file to local USB drive"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Deleting files breaks audit trail.",
                        "2": "Paper mail defeats paperless e-Office objective.",
                        "3": "USB downloads violate endpoint security."
                    },
                    "recommended_module_id": "IGOT-COURSE-017"
                }
            ]
        },
        "COMP_MANAGEMENT": {
            "baseline": [
                {
                    "id": "Q_MGMT_L1_01",
                    "sub_skill_code": "SUB_LEADERSHIP",
                    "difficulty_level": 1,
                    "scenario_text": "A team leader is managing a complex multi-district survey project.",
                    "question": "[Level 1 - Foundational] Which key leadership practice ensures timely project delivery across dispersed teams?",
                    "options": [
                        "Clear goal setting, milestone tracking, and regular feedback loops",
                        "Micro-managing every minor task without delegation",
                        "Avoiding communication until deadline expires",
                        "Assigning conflicting targets to team members"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Micro-management lowers productivity and morale.",
                        "2": "Avoiding communication causes project failure.",
                        "3": "Conflicting targets create internal friction."
                    },
                    "recommended_module_id": "IGOT-COURSE-007"
                },
                {
                    "id": "Q_MGMT_L2_01",
                    "sub_skill_code": "SUB_PROJECTMGMT",
                    "difficulty_level": 2,
                    "scenario_text": "A major government infrastructure project faces critical path delays.",
                    "question": "[Level 2 - Applied] In CPM / PERT project monitoring, what does a zero float activity represent?",
                    "options": [
                        "A critical activity where any delay directly delays the overall project completion date",
                        "An activity that can be delayed indefinitely without impact",
                        "An optional task that can be omitted",
                        "A completed task requiring no monitoring"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Activities with zero float cannot be delayed without delaying the project.",
                        "2": "Zero float tasks are mandatory, not optional.",
                        "3": "Completed tasks have no float status."
                    },
                    "recommended_module_id": "IGOT-COURSE-020"
                },
                {
                    "id": "Q_MGMT_L3_01",
                    "sub_skill_code": "SUB_ETHICS",
                    "difficulty_level": 3,
                    "scenario_text": "An administrator faces public pressure to fast-track an environmental clearance for a commercial project.",
                    "question": "[Level 3 - Advanced] How should the officer balance administrative speed with public interest ethics?",
                    "options": [
                        "Adhere strictly to statutory EIA evaluation parameters while ensuring transparent, time-bound processing",
                        "Bypass environmental impact study to appease stakeholders",
                        "Delay file indefinitely without providing official reasons",
                        "Outsource decision making to an unauthorized private consultant"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "Bypassing EIA rules causes environmental harm and legal invalidity.",
                        "2": "Indefinite delay violates administrative timelines.",
                        "3": "Delegating statutory authority to private consultants is illegal."
                    },
                    "recommended_module_id": "IGOT-COURSE-011"
                }
            ],
            "intermediate": [
                {
                    "id": "Q_MGMT_INT_L2_01",
                    "sub_skill_code": "SUB_PROJECTMGMT",
                    "difficulty_level": 2,
                    "scenario_text": "A project manager is monitoring budget expenditure variance.",
                    "question": "[Level 2 - Applied] What metric in Earned Value Management (EVM) indicates a project is under budget?",
                    "options": [
                        "Cost Variance (CV = EV - AC) > 0",
                        "Schedule Variance (SV) < 0",
                        "Cost Performance Index (CPI) < 0.5",
                        "Actual Cost exceeding Budgeted Cost"
                    ],
                    "answer": 0,
                    "distractor_explanations": {
                        "1": "SV indicates schedule status, not cost.",
                        "2": "CPI < 1 indicates over budget expenditure.",
                        "3": "Actual exceeding Budget means over budget."
                    },
                    "recommended_module_id": "IGOT-COURSE-020"
                }
            ]
        }
    }
    return quizzes

def generate_full_database():
    roles = []

    for idx, job_title in enumerate(JOBS):
        role_id = f"ROLE_JOB_{idx+1:03d}"
        dept = "Central/State Civil Services"
        exp_years = 1 + (idx % 10)
        
        if "Forest" in job_title:
            dept = "Forest & Environment Department"
        elif "Income Tax" in job_title or "Revenue" in job_title or "Taxes" in job_title or "Excise" in job_title:
            dept = "Revenue & Taxation Department"
        elif "Police" in job_title or "CBI" in job_title or "Prisons" in job_title:
            dept = "Police & Home Affairs Department"
        elif "Banking" in job_title or "RBI" in job_title or "SEBI" in job_title or "NABARD" in job_title or "LIC" in job_title:
            dept = "Financial & Banking Services"
        elif "Statistical" in job_title:
            dept = "Ministry of Statistics and Programme Implementation (MoSPI)"
        elif "ISRO" in job_title or "DRDO" in job_title or "BARC" in job_title or "CSIR" in job_title or "NPCIL" in job_title:
            dept = "Scientific & Research Laboratories"

        roles.append({
            "id": role_id,
            "title": job_title,
            "department": dept,
            "eligibility": "Bachelor's/Master's Degree in relevant discipline with Union/State Public Service Commission qualification.",
            "experience_years": exp_years,
            "description": f"Official position responsibilities for {job_title} within the {dept}.",
            "required_competencies": STANDARD_COMPETENCIES
        })

    igot_courses = []
    for idx, (title, url, comp_code, sub_code, desc) in enumerate(IGOT_COURSES_RAW):
        igot_courses.append({
            "course_id": f"IGOT-COURSE-{idx+1:03d}",
            "title": title,
            "provider": "iGOT Karmayogi / DoPT / Capacity Building Commission (CBC)",
            "competency_code": comp_code,
            "sub_skill_code": sub_code,
            "competency_name": desc,
            "duration": f"{3 + (idx % 8)} Hours",
            "rating": round(4.5 + ((idx % 5) * 0.1), 1),
            "igot_url": url,
            "description": f"{desc}. Official training module indexed from iGOT Karmayogi national portal.",
            "embed_video_url": "https://www.youtube.com/embed/3E16_f6V4mI"
        })

    quizzes = generate_multi_tier_quizzes()

    db_data = {
        "roles": roles,
        "quizzes": quizzes,
        "igot_courses": igot_courses,
        "creator_uploaded_materials": [],
        "users": {}
    }

    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_data, f, indent=2)

    print(f"Successfully generated db.json with sub-skills, multi-tier quizzes, and scenarios across {len(roles)} Roles & {len(igot_courses)} iGOT Courses!")

if __name__ == "__main__":
    generate_full_database()
