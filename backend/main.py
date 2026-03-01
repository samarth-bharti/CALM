"""
Baseline Calibration Prototype - Professional Edition with Employee Assessment
===============================================================================
Advanced behavioral analytics engine with sophisticated metrics,
statistical analysis, cognitive pattern recognition, and comprehensive
employee assessment features.

Author: Baseline Calibration System
Version: 3.0.0 Professional + Employee Assessment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass
import time
import uuid
import sqlite3
import json
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Employee Assessment API - Professional Edition",
    description="Advanced behavioral analytics with comprehensive employee assessment",
    version="3.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== ENUMS ==================

class CognitiveState(str, Enum):
    FLOW = "flow"
    FOCUSED = "focused"
    NORMAL = "normal"
    STRESSED = "stressed"
    OVERLOADED = "overloaded"

class StabilityClass(str, Enum):
    HIGHLY_STABLE = "Highly Stable"
    STABLE = "Stable"
    MODERATE = "Moderate"
    VARIABLE = "Variable"
    HIGHLY_VARIABLE = "Highly Variable"

class ExpertiseLevel(str, Enum):
    NOVICE = "Novice"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"
    MASTER = "Master"

class ProfessionalRole(str, Enum):
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    RESEARCH = "Research"
    MAINTENANCE = "Maintenance"

# ================== DATA MODELS ==================

# Existing models
class ProfileData(BaseModel):
    years_coding: int = Field(ge=0, le=50)
    daily_hours: int = Field(ge=1, le=16)
    primary_language: str
    focus_stability: int = Field(ge=1, le=5)
    multitask_level: str
    typing_frequency: Optional[str] = "medium"
    error_correction_style: Optional[str] = "immediate"
    preferred_complexity: Optional[int] = 3


class KeystrokeEvent(BaseModel):
    timestamp: float
    key: str
    is_backspace: bool = False
    is_enter: bool = False
    is_tab: bool = False
    is_space: bool = False
    is_punctuation: bool = False


class TypingMetricsInput(BaseModel):
    keystrokes: List[KeystrokeEvent]
    total_chars: int
    expected_text: str
    actual_text: Optional[str] = None
    test_duration_ms: Optional[float] = None


class CodingStageData(BaseModel):
    stage: int
    keystrokes: List[KeystrokeEvent]
    time_to_first_keystroke: float
    total_time: float
    backspace_count: int
    pause_events: int
    long_pause_events: int
    rewrite_count: int
    code_lines: Optional[int] = 1
    syntax_errors: Optional[int] = 0


class CodingMetricsInput(BaseModel):
    stages: List[CodingStageData]
    completed_stages: int
    language: Optional[str] = "Python"


class CognitiveTaskInput(BaseModel):
    keystrokes: List[KeystrokeEvent]
    total_time: float
    error_count: int
    hesitation_count: Optional[int] = 0
    revision_count: Optional[int] = 0


# ================== NEW DATA MODELS FOR EMPLOYEE ASSESSMENT ==================

class EmployeeInfo(BaseModel):
    """Employee demographic and professional information"""
    employee_id: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=2, max_length=100)
    # Accept both 'position' (backend) and 'job_role' (frontend)
    position: Optional[str] = Field(None, min_length=2, max_length=100)
    job_role: Optional[str] = Field(None, min_length=2, max_length=100)
    years_experience: int = Field(ge=0, le=50)
    # Accept both 'education_level' and 'education' (frontend might send different names)
    education_level: Optional[str] = Field(None, min_length=2, max_length=100)
    education: Optional[str] = Field(None, min_length=2, max_length=100)
    # Accept both 'age_range' and 'age' (frontend sends 'age')
    age_range: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=100)
    location: Optional[str] = Field(None, min_length=2, max_length=100)
    session_id: Optional[str] = None
    timestamp: Optional[float] = None
    consent_given: bool = True


class ClassificationQuestion(BaseModel):
    """Single classification question with answer"""
    question_id: str
    question_text: str
    answer: str
    answer_index: int


class ClassificationResult(BaseModel):
    """Professional role classification result"""
    session_id: str
    primary_role: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    secondary_role: Optional[str] = None
    secondary_confidence: Optional[float] = None
    frontend_score: float
    backend_score: float
    research_score: float
    maintenance_score: float
    timestamp: float
    classification_method: str = "weighted_scoring"


class ClassificationInput(BaseModel):
    """Input for classification endpoint"""
    session_id: str
    answers: List[ClassificationQuestion]


class HardwareDetails(BaseModel):
    """Hardware and environment information"""
    session_id: str
    screen_width: int
    screen_height: int
    screen_resolution: str
    pixel_ratio: float
    color_depth: Optional[int] = 24
    user_agent: str
    browser_name: str
    browser_version: str
    os_name: str
    os_version: Optional[str] = "Unknown"
    platform: str
    has_touch: bool
    has_mouse: bool
    has_keyboard: bool
    pointer_type: str
    network_latency_ms: Optional[float] = 0
    connection_type: Optional[str] = "unknown"
    cpu_cores: Optional[int] = None
    device_memory_gb: Optional[float] = None
    timestamp: float
    timezone: Optional[str] = "UTC"
    language: Optional[str] = "en"


class MouseClickEvent(BaseModel):
    """Single mouse click event"""
    timestamp: float
    x: int
    y: int
    target_x: int
    target_y: int
    distance_from_target: float
    reaction_time_ms: float
    click_type: str = "left"


class MouseMovement(BaseModel):
    """Mouse movement tracking"""
    timestamp: float
    x: int
    y: int
    velocity: Optional[float] = 0
    acceleration: Optional[float] = 0


class MouseMetricsInput(BaseModel):
    """Input for mouse metrics endpoint"""
    session_id: str
    test_type: str
    clicks: List[MouseClickEvent]
    movements: Optional[List[MouseMovement]] = []
    duration_ms: float
    timestamp: float


class MouseMetrics(BaseModel):
    """Comprehensive mouse behavior analysis"""
    session_id: str
    test_type: str
    mean_accuracy: float
    std_accuracy: float
    accuracy_score: float
    mean_reaction_time: float
    std_reaction_time: float
    fastest_reaction: float
    slowest_reaction: float
    mean_velocity: Optional[float] = 0
    path_efficiency: Optional[float] = 1.0
    tremor_score: Optional[float] = 0
    drag_precision: Optional[float] = None
    drop_accuracy: Optional[float] = None
    mouse_proficiency_score: float
    hand_eye_coordination: float
    timestamp: float
    duration_ms: float


class RoleTestResult(BaseModel):
    """Result from a single role-specific test"""
    session_id: str
    test_id: str
    test_category: str
    test_name: str
    start_time: float
    end_time: float
    duration_ms: float
    score: float = Field(ge=0, le=100)
    accuracy: float = Field(ge=0, le=1)
    completion_percentage: float = Field(ge=0, le=100)
    keystrokes: Optional[List[KeystrokeEvent]] = []
    mouse_events: Optional[List[MouseClickEvent]] = []
    custom_metrics: Optional[Dict[str, Any]] = {}
    suspicious_activity: bool = False
    tab_switches: int = 0
    window_blurs: int = 0
    paste_attempts: int = 0
    timestamp: float
    passed: bool = True


class AntiCheatEvent(BaseModel):
    """Anti-cheat event logging"""
    session_id: str
    event_type: str
    timestamp: float
    details: Optional[str] = None


# ================== DATABASE MANAGER ==================

class DatabaseManager:
    """Manage SQLite database operations"""
    
    def __init__(self, db_path: str = "data/assessment.db"):
        # Get the directory where main.py is located
        script_dir = Path(__file__).parent.resolve()
        
        # If db_path is relative, make it relative to the script directory
        if not Path(db_path).is_absolute():
            self.db_path = str(script_dir / db_path)
            data_dir = script_dir / "data"
        else:
            self.db_path = db_path
            data_dir = Path(db_path).parent
        
        # Create data directory if it doesn't exist
        try:
            data_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Data directory ready: {data_dir}")
        except PermissionError as e:
            logger.error(f"Permission denied creating data directory: {e}")
            raise
        except OSError as e:
            logger.error(f"OS error creating data directory: {e}")
            raise
        
        self.init_database()
    
    def get_connection(self):
        """Get a new database connection"""
        try:
            return sqlite3.connect(self.db_path, check_same_thread=False)
        except sqlite3.OperationalError as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def init_database(self):
        """Initialize database and create tables"""
        try:
            conn = self.get_connection()
            self.create_tables(conn)
            conn.close()
            logger.info(f"Database initialized successfully: {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def create_tables(self, conn):
        """Create all necessary tables"""
        cursor = conn.cursor()
        
        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                employee_id TEXT NOT NULL,
                start_time REAL NOT NULL,
                end_time REAL,
                status TEXT NOT NULL,
                completion_percentage REAL,
                total_duration_ms REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(employee_id)
            )
        """)
        
        # Employee information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                employee_id TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                department TEXT,
                position TEXT,
                years_experience INTEGER,
                education_level TEXT,
                age_range TEXT,
                location TEXT,
                timestamp REAL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Professional classification
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                primary_role TEXT NOT NULL,
                confidence_score REAL,
                secondary_role TEXT,
                frontend_score REAL,
                backend_score REAL,
                research_score REAL,
                maintenance_score REAL,
                timestamp REAL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Hardware details
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hardware (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                screen_resolution TEXT,
                browser_name TEXT,
                browser_version TEXT,
                os_name TEXT,
                os_version TEXT,
                network_latency_ms REAL,
                has_touch BOOLEAN,
                timestamp REAL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Mouse metrics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mouse_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                test_type TEXT,
                mean_accuracy REAL,
                mean_reaction_time REAL,
                accuracy_score REAL,
                mouse_proficiency_score REAL,
                hand_eye_coordination REAL,
                duration_ms REAL,
                timestamp REAL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Role-specific test results
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS role_test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                test_id TEXT NOT NULL,
                test_category TEXT,
                test_name TEXT,
                score REAL,
                accuracy REAL,
                duration_ms REAL,
                passed BOOLEAN,
                suspicious_activity BOOLEAN,
                tab_switches INTEGER,
                window_blurs INTEGER,
                paste_attempts INTEGER,
                timestamp REAL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Complete session data (JSON blob)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_data (
                session_id TEXT PRIMARY KEY,
                data_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Anti-cheat events
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anti_cheat_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                timestamp REAL,
                details TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_employee ON sessions(employee_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_employees_email ON employees(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_role_tests_session ON role_test_results(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_anti_cheat_session ON anti_cheat_events(session_id)")
        
        conn.commit()
    
    def check_existing_session(self, employee_id: str) -> Optional[str]:
        """Check if employee already has a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT session_id FROM employees WHERE employee_id = ?", (employee_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def create_session(self, session_id: str, employee_id: str):
        """Create new session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sessions (session_id, employee_id, start_time, status, completion_percentage)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, employee_id, time.time(), "in_progress", 0.0))
        conn.commit()
        conn.close()
    
    def save_employee(self, employee: EmployeeInfo):
        """Save employee information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employees (
                session_id, employee_id, full_name, email,
                department, position, years_experience,
                education_level, age_range, location, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            employee.session_id, employee.employee_id, employee.full_name,
            employee.email, employee.department, employee.position,
            employee.years_experience, employee.education_level,
            employee.age_range, employee.location, employee.timestamp
        ))
        conn.commit()
        conn.close()
    
    def save_classification(self, classification: ClassificationResult):
        """Save classification result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO classifications (
                session_id, primary_role, confidence_score, secondary_role,
                frontend_score, backend_score, research_score, maintenance_score, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            classification.session_id, classification.primary_role,
            classification.confidence_score, classification.secondary_role,
            classification.frontend_score, classification.backend_score,
            classification.research_score, classification.maintenance_score,
            classification.timestamp
        ))
        conn.commit()
        conn.close()
    
    def save_hardware(self, hardware: HardwareDetails):
        """Save hardware details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO hardware (
                session_id, screen_resolution, browser_name, browser_version,
                os_name, os_version, network_latency_ms, has_touch, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            hardware.session_id, hardware.screen_resolution, hardware.browser_name,
            hardware.browser_version, hardware.os_name, hardware.os_version,
            hardware.network_latency_ms, hardware.has_touch, hardware.timestamp
        ))
        conn.commit()
        conn.close()
    
    def save_mouse_metrics(self, metrics: MouseMetrics):
        """Save mouse metrics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mouse_metrics (
                session_id, test_type, mean_accuracy, mean_reaction_time,
                accuracy_score, mouse_proficiency_score, hand_eye_coordination,
                duration_ms, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            metrics.session_id, metrics.test_type, metrics.mean_accuracy,
            metrics.mean_reaction_time, metrics.accuracy_score,
            metrics.mouse_proficiency_score, metrics.hand_eye_coordination,
            metrics.duration_ms, metrics.timestamp
        ))
        conn.commit()
        conn.close()
    
    def save_role_test(self, result: RoleTestResult):
        """Save role test result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO role_test_results (
                session_id, test_id, test_category, test_name, score, accuracy,
                duration_ms, passed, suspicious_activity, tab_switches,
                window_blurs, paste_attempts, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.session_id, result.test_id, result.test_category, result.test_name,
            result.score, result.accuracy, result.duration_ms, result.passed,
            result.suspicious_activity, result.tab_switches, result.window_blurs,
            result.paste_attempts, result.timestamp
        ))
        conn.commit()
        conn.close()
    
    def save_anti_cheat_event(self, event: AntiCheatEvent):
        """Save anti-cheat event"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO anti_cheat_events (session_id, event_type, timestamp, details)
            VALUES (?, ?, ?, ?)
        """, (event.session_id, event.event_type, event.timestamp, event.details))
        conn.commit()
        conn.close()
    
    def get_anti_cheat_summary(self, session_id: str) -> Dict[str, Any]:
        """Get anti-cheat summary for session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT event_type, COUNT(*) as count
            FROM anti_cheat_events
            WHERE session_id = ?
            GROUP BY event_type
        """, (session_id,))
        events = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return events
    
    def get_session_data(self, session_id: str) -> Optional[Dict]:
        """Get complete session data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT data_json FROM session_data WHERE session_id = ?", (session_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return json.loads(result[0])
        return None
    
    def save_session_data(self, session_id: str, data: Dict):
        """Save complete session data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO session_data (session_id, data_json, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (session_id, json.dumps(data)))
        conn.commit()
        conn.close()


# Initialize database
db = DatabaseManager()


# ================== CLASSIFICATION QUESTIONS AND LOGIC ==================

CLASSIFICATION_QUESTIONS = [
    {
        "id": "q1",
        "text": "What percentage of your work involves visual design and user interfaces?",
        "options": ["0-25%", "25-50%", "50-75%", "75-100%"],
        "weights": {
            "Frontend": [0, 0.3, 0.7, 1.0],
            "Backend": [1.0, 0.7, 0.3, 0],
            "Research": [0.5, 0.5, 0.3, 0.1],
            "Maintenance": [0.3, 0.4, 0.3, 0.2]
        }
    },
    {
        "id": "q2",
        "text": "How often do you work with databases and server-side logic?",
        "options": ["Rarely", "Sometimes", "Often", "Always"],
        "weights": {
            "Backend": [0, 0.3, 0.7, 1.0],
            "Frontend": [1.0, 0.7, 0.3, 0],
            "Research": [0.3, 0.5, 0.6, 0.4],
            "Maintenance": [0.2, 0.4, 0.6, 0.7]
        }
    },
    {
        "id": "q3",
        "text": "Do you spend time analyzing data, running experiments, or building models?",
        "options": ["Never", "Occasionally", "Frequently", "Primarily"],
        "weights": {
            "Research": [0, 0.3, 0.7, 1.0],
            "Backend": [0.5, 0.4, 0.3, 0.2],
            "Frontend": [0.3, 0.2, 0.1, 0],
            "Maintenance": [0.2, 0.3, 0.2, 0.1]
        }
    },
    {
        "id": "q4",
        "text": "How much time do you spend fixing bugs vs building new features?",
        "options": ["Mostly new features", "Balanced", "Mostly bug fixes", "Almost all maintenance"],
        "weights": {
            "Maintenance": [0, 0.3, 0.7, 1.0],
            "Frontend": [1.0, 0.6, 0.3, 0.1],
            "Backend": [0.8, 0.6, 0.4, 0.2],
            "Research": [0.7, 0.5, 0.3, 0.1]
        }
    },
    {
        "id": "q5",
        "text": "Which tools do you use most frequently?",
        "options": ["React/Vue/Angular", "Node/Django/Flask", "Jupyter/R/MATLAB", "Git/Jenkins/Monitoring"],
        "weights": {
            "Frontend": [1.0, 0, 0, 0],
            "Backend": [0, 1.0, 0, 0],
            "Research": [0, 0, 1.0, 0],
            "Maintenance": [0, 0, 0, 1.0]
        }
    },
    {
        "id": "q6",
        "text": "What best describes your typical deliverables?",
        "options": ["UI components", "APIs/Services", "Analysis reports", "Bug fixes/Patches"],
        "weights": {
            "Frontend": [1.0, 0, 0, 0],
            "Backend": [0, 1.0, 0, 0],
            "Research": [0, 0, 1.0, 0],
            "Maintenance": [0, 0, 0, 1.0]
        }
    },
    {
        "id": "q7",
        "text": "How do you spend most of your coding time?",
        "options": ["Styling/Layout", "Business logic", "Data analysis", "Code review/Refactoring"],
        "weights": {
            "Frontend": [1.0, 0, 0, 0],
            "Backend": [0, 1.0, 0, 0],
            "Research": [0, 0, 1.0, 0],
            "Maintenance": [0, 0, 0, 1.0]
        }
    },
    {
        "id": "q8",
        "text": "Which statement best describes your work?",
        "options": [
            "I make things look good and work smoothly for users",
            "I build robust systems that process and store data",
            "I discover insights and optimize algorithms",
            "I keep systems running and improve existing code"
        ],
        "weights": {
            "Frontend": [1.0, 0, 0, 0],
            "Backend": [0, 1.0, 0, 0],
            "Research": [0, 0, 1.0, 0],
            "Maintenance": [0, 0, 0, 1.0]
        }
    }
]


def classify_professional_role(answers: List[ClassificationQuestion]) -> ClassificationResult:
    """
    Classify professional role using weighted scoring algorithm.
    Returns primary role, confidence score, and optional secondary role.
    """
    # Initialize scores
    scores = {
        "Frontend": 0.0,
        "Backend": 0.0,
        "Research": 0.0,
        "Maintenance": 0.0
    }
    
    # Calculate weighted scores
    for answer in answers:
        question = next((q for q in CLASSIFICATION_QUESTIONS if q["id"] == answer.question_id), None)
        if question:
            weights = question["weights"]
            answer_idx = answer.answer_index
            
            for role, role_weights in weights.items():
                if answer_idx < len(role_weights):
                    scores[role] += role_weights[answer_idx]
    
    # Normalize scores
    total_questions = len(answers)
    for role in scores:
        scores[role] = scores[role] / total_questions if total_questions > 0 else 0
    
    # Find primary and secondary roles
    sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary_role = sorted_roles[0][0]
    primary_score = sorted_roles[0][1]
    secondary_role = sorted_roles[1][0] if len(sorted_roles) > 1 else None
    secondary_score = sorted_roles[1][1] if len(sorted_roles) > 1 else 0
    
    # Calculate confidence (difference between primary and secondary)
    confidence = (primary_score - secondary_score) / primary_score if primary_score > 0 else 0
    
    # If confidence is low, include secondary role
    include_secondary = confidence < 0.3 and secondary_score > 0.3
    
    return ClassificationResult(
        session_id="",  # Will be set by caller
        primary_role=primary_role,
        confidence_score=confidence,
        secondary_role=secondary_role if include_secondary else None,
        secondary_confidence=secondary_score if include_secondary else None,
        frontend_score=scores["Frontend"],
        backend_score=scores["Backend"],
        research_score=scores["Research"],
        maintenance_score=scores["Maintenance"],
        timestamp=time.time()
    )


# ================== MOUSE METRICS ANALYTICS ==================

def calculate_mouse_metrics(mouse_data: MouseMetricsInput) -> MouseMetrics:
    """
    Calculate comprehensive mouse metrics from raw click and movement data.
    """
    clicks = mouse_data.clicks
    movements = mouse_data.movements or []
    
    # Calculate accuracy metrics
    distances = [click.distance_from_target for click in clicks]
    mean_accuracy = statistics.mean(distances) if distances else 0
    std_accuracy = statistics.stdev(distances) if len(distances) > 1 else 0
    
    # Accuracy score (0-100, lower distance = higher score)
    # Assume target radius is 30px, perfect click = 0px distance
    max_acceptable_distance = 50
    accuracy_score = max(0, min(100, 100 * (1 - mean_accuracy / max_acceptable_distance)))
    
    # Calculate reaction time metrics
    reaction_times = [click.reaction_time_ms for click in clicks]
    mean_reaction = statistics.mean(reaction_times) if reaction_times else 0
    std_reaction = statistics.stdev(reaction_times) if len(reaction_times) > 1 else 0
    fastest = min(reaction_times) if reaction_times else 0
    slowest = max(reaction_times) if reaction_times else 0
    
    # Calculate movement metrics if available
    mean_velocity = 0
    path_efficiency = 1.0
    tremor_score = 0
    
    if movements and len(movements) > 1:
        velocities = [m.velocity for m in movements if m.velocity is not None]
        mean_velocity = statistics.mean(velocities) if velocities else 0
        
        # Path efficiency: straight line distance / actual path length
        if len(movements) >= 2:
            start = movements[0]
            end = movements[-1]
            straight_distance = math.sqrt((end.x - start.x)**2 + (end.y - start.y)**2)
            
            actual_distance = 0
            for i in range(1, len(movements)):
                dx = movements[i].x - movements[i-1].x
                dy = movements[i].y - movements[i-1].y
                actual_distance += math.sqrt(dx**2 + dy**2)
            
            path_efficiency = straight_distance / actual_distance if actual_distance > 0 else 1.0
        
        # Tremor score: variability in velocity (smoothness)
        if velocities and len(velocities) > 1:
            velocity_cv = statistics.stdev(velocities) / statistics.mean(velocities) if statistics.mean(velocities) > 0 else 0
            tremor_score = min(100, velocity_cv * 100)
    
    # Calculate overall proficiency score
    # Weighted combination of accuracy, reaction time, and smoothness
    reaction_score = max(0, min(100, 100 * (1 - (mean_reaction - 200) / 800)))  # 200ms = excellent, 1000ms = poor
    smoothness_score = max(0, 100 - tremor_score)
    
    proficiency = (
        accuracy_score * 0.4 +
        reaction_score * 0.4 +
        smoothness_score * 0.2
    )
    
    # Hand-eye coordination score
    # Based on accuracy and reaction time consistency
    coordination = (
        accuracy_score * 0.5 +
        (100 - (std_reaction / mean_reaction * 100 if mean_reaction > 0 else 0)) * 0.5
    )
    coordination = max(0, min(100, coordination))
    
    return MouseMetrics(
        session_id=mouse_data.session_id,
        test_type=mouse_data.test_type,
        mean_accuracy=round(mean_accuracy, 2),
        std_accuracy=round(std_accuracy, 2),
        accuracy_score=round(accuracy_score, 2),
        mean_reaction_time=round(mean_reaction, 2),
        std_reaction_time=round(std_reaction, 2),
        fastest_reaction=round(fastest, 2),
        slowest_reaction=round(slowest, 2),
        mean_velocity=round(mean_velocity, 2),
        path_efficiency=round(path_efficiency, 4),
        tremor_score=round(tremor_score, 2),
        mouse_proficiency_score=round(proficiency, 2),
        hand_eye_coordination=round(coordination, 2),
        timestamp=mouse_data.timestamp,
        duration_ms=mouse_data.duration_ms
    )


# ================== ANTI-CHEAT VALIDATION ==================

class AntiCheatValidator:
    """Server-side anti-cheat validation"""
    
    SUSPICIOUS_ACTIVITY_THRESHOLD = {
        "tab_switches": 5,
        "window_blurs": 10,
        "paste_attempts": 3,
        "typing_anomalies": 3
    }
    
    def validate_typing_pattern(self, keystrokes: List[KeystrokeEvent]) -> Dict[str, Any]:
        """
        Detect paste vs typing by analyzing keystroke patterns.
        """
        if len(keystrokes) < 10:
            return {"suspicious": False, "reason": None}
        
        # Calculate inter-keystroke times
        ikt_values = []
        for i in range(1, len(keystrokes)):
            ikt = keystrokes[i].timestamp - keystrokes[i-1].timestamp
            ikt_values.append(ikt)
        
        # Check for suspiciously fast typing (paste detection)
        very_fast_count = sum(1 for ikt in ikt_values if ikt < 10)
        if very_fast_count > len(ikt_values) * 0.5:
            return {
                "suspicious": True,
                "reason": "Possible paste detected",
                "very_fast_percentage": very_fast_count / len(ikt_values)
            }
        
        # Check for unnatural consistency (bot detection)
        if len(ikt_values) > 20:
            std_ikt = statistics.stdev(ikt_values)
            mean_ikt = statistics.mean(ikt_values)
            cv = std_ikt / mean_ikt if mean_ikt > 0 else 0
            
            if cv < 0.1:  # Too consistent to be human
                return {
                    "suspicious": True,
                    "reason": "Unnatural typing consistency",
                    "coefficient_of_variation": cv
                }
        
        return {"suspicious": False, "reason": None}
    
    def validate_test_result(self, result: RoleTestResult) -> Dict[str, Any]:
        """Validate test result for suspicious activity"""
        flags = []
        
        # Check typing pattern
        if result.keystrokes:
            typing_check = self.validate_typing_pattern(result.keystrokes)
            if typing_check["suspicious"]:
                flags.append(typing_check["reason"])
        
        # Check tab switches
        if result.tab_switches > self.SUSPICIOUS_ACTIVITY_THRESHOLD["tab_switches"]:
            flags.append(f"Excessive tab switches: {result.tab_switches}")
        
        # Check window blurs
        if result.window_blurs > self.SUSPICIOUS_ACTIVITY_THRESHOLD["window_blurs"]:
            flags.append(f"Excessive window blurs: {result.window_blurs}")
        
        # Check paste attempts
        if result.paste_attempts > self.SUSPICIOUS_ACTIVITY_THRESHOLD["paste_attempts"]:
            flags.append(f"Multiple paste attempts: {result.paste_attempts}")
        
        # Check test duration (too fast = suspicious)
        expected_min_duration = 30000  # 30 seconds minimum
        if result.duration_ms < expected_min_duration:
            flags.append(f"Test completed too quickly: {result.duration_ms}ms")
        
        return {
            "suspicious": len(flags) > 0,
            "flags": flags,
            "confidence": min(1.0, len(flags) / 5.0)
        }


anti_cheat = AntiCheatValidator()


# ================== ROLE-SPECIFIC TEST LIBRARY ==================

# Simplified test library (subset for MVP)
ROLE_TESTS = {
    "Frontend": [
        {
            "test_id": "fe_01",
            "test_name": "HTML/CSS/JS Typing Test",
            "category": "Frontend",
            "difficulty": "Easy",
            "prompt": "Type the following HTML/CSS code exactly as shown:",
            "expected_code": """<div class="container">
  <h1 class="title">Welcome</h1>
  <button onclick="handleClick()">Click Me</button>
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
</style>""",
            "time_limit_seconds": 300
        },
        {
            "test_id": "fe_02",
            "test_name": "DOM Debugging Challenge",
            "category": "Frontend",
            "difficulty": "Medium",
            "prompt": "Fix the bug in this JavaScript code:",
            "initial_code": "document.querySeletor('#btn').addEventListener('click', fn);",
            "time_limit_seconds": 180
        }
    ],
    "Backend": [
        {
            "test_id": "be_01",
            "test_name": "API Debugging Challenge",
            "category": "Backend",
            "difficulty": "Medium",
            "prompt": "Fix the bug in this API endpoint:",
            "initial_code": "@app.get('/users/{id}')\ndef get_user(id: int):\n    user = db.query(User).filter(User.id == id).first()\n    return {'user': user.name}",
            "time_limit_seconds": 240
        },
        {
            "test_id": "be_02",
            "test_name": "SQL Query Optimization",
            "category": "Backend",
            "difficulty": "Hard",
            "prompt": "Optimize this slow SQL query:",
            "initial_code": "SELECT u.name, COUNT(o.id) FROM users u, orders o WHERE u.id = o.user_id GROUP BY u.name;",
            "time_limit_seconds": 360
        }
    ],
    "Research": [
        {
            "test_id": "re_01",
            "test_name": "Python Data Analysis",
            "category": "Research",
            "difficulty": "Medium",
            "prompt": "Analyze this dataset and find patterns:",
            "initial_code": "import pandas as pd\ndf = pd.read_csv('data.csv')\n# Your analysis here",
            "time_limit_seconds": 420
        },
        {
            "test_id": "re_02",
            "test_name": "Algorithm Complexity",
            "category": "Research",
            "difficulty": "Hard",
            "prompt": "Optimize this algorithm:",
            "initial_code": "def find_duplicates(arr):\n    result = []\n    for i in range(len(arr)):\n        for j in range(i+1, len(arr)):\n            if arr[i] == arr[j]:\n                result.append(arr[i])\n    return result",
            "time_limit_seconds": 360
        }
    ],
    "Maintenance": [
        {
            "test_id": "ma_01",
            "test_name": "Bug Identification",
            "category": "Maintenance",
            "difficulty": "Easy",
            "prompt": "Find and fix the bug in this code:",
            "initial_code": "def calculate_average(numbers):\n    total = sum(numbers)\n    return total / len(numbers)",
            "time_limit_seconds": 180
        },
        {
            "test_id": "ma_02",
            "test_name": "Code Refactoring",
            "category": "Maintenance",
            "difficulty": "Medium",
            "prompt": "Refactor this code to improve readability:",
            "initial_code": "def f(x,y,z):\n    if x>0:\n        if y>0:\n            if z>0:\n                return x+y+z\n    return 0",
            "time_limit_seconds": 240
        }
    ]
}


# ================== EXISTING PROFESSIONAL ANALYTICS (PRESERVED) ==================

@dataclass
class TypingMetricsResult:
    """Comprehensive typing analysis results"""
    mean_ikt: float
    std_ikt: float
    median_ikt: float
    mode_ikt: float
    coefficient_of_variation: float
    skewness: float
    kurtosis: float
    percentile_25: float
    percentile_75: float
    percentile_95: float
    interquartile_range: float
    typing_speed_cpm: float
    typing_speed_wpm: float
    burst_speed_cpm: float
    sustainable_speed_cpm: float
    rhythm_consistency_score: float
    flow_state_probability: float
    micro_pause_frequency: float
    correction_rate: float
    immediate_correction_rate: float
    delayed_correction_rate: float
    error_burst_count: int
    pause_ratio: float
    long_pause_ratio: float
    very_long_pause_ratio: float
    mean_pause_duration: float
    pause_pattern_regularity: float
    cognitive_load_index: float
    fatigue_indicator: float
    attention_stability: float
    typing_proficiency_score: float
    consistency_rating: float
    efficiency_score: float


@dataclass
class CognitiveProfileResult:
    """Advanced cognitive analysis results"""
    std_shift_between_stages: float
    correction_shift: float
    latency_shift: float
    speed_shift: float
    frustration_index: float
    stress_accumulation_rate: float
    cognitive_overload_probability: float
    load_sensitivity: float
    adaptive_capacity: float
    recovery_rate: float
    flow_state_duration_ratio: float
    flow_entry_count: int
    flow_exit_count: int
    average_flow_duration: float
    problem_solving_efficiency: float
    iteration_tendency: float
    exploration_vs_exploitation: float
    endurance_score: float
    degradation_rate: float
    optimal_session_length_estimate: float
    cognitive_flexibility_score: float
    focus_endurance_score: float
    problem_solving_score: float


# ================== SESSION STORAGE ==================

class SessionStorage:
    """Professional session management with analytics history"""
    
    def __init__(self):
        self.profile: Optional[Dict] = None
        self.typing_metrics: Optional[Dict] = None
        self.coding_metrics: Optional[Dict] = None
        self.cognitive_metrics: Optional[Dict] = None
        self.baseline: Dict = {
            "keyboard": None,
            "cognitive_profile": None,
            "experience_factor": None,
            "stability_modifier": None,
            "expertise_level": None,
            "baseline_confidence": None,
            "calibration_timestamp": None
        }
        self.analytics_history: List[Dict] = []
    
    def reset(self):
        self.__init__()

session_data = SessionStorage()


# ================== CALCULATION FUNCTIONS (PRESERVED FROM ORIGINAL) ==================

def calculate_percentile(data: List[float], percentile: int) -> float:
    """Calculate percentile using linear interpolation"""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    n = len(sorted_data)
    index = (percentile / 100) * (n - 1)
    lower = int(index)
    upper = lower + 1
    if upper >= n:
        return sorted_data[-1]
    weight = index - lower
    return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight


def calculate_skewness(data: List[float]) -> float:
    """Calculate skewness (asymmetry measure)"""
    if len(data) < 3:
        return 0.0
    n = len(data)
    mean = statistics.mean(data)
    std = statistics.stdev(data)
    if std == 0:
        return 0.0
    skew = sum((x - mean) ** 3 for x in data) / (n * std ** 3)
    return skew


def calculate_kurtosis(data: List[float]) -> float:
    """Calculate kurtosis (tailedness measure)"""
    if len(data) < 4:
        return 0.0
    n = len(data)
    mean = statistics.mean(data)
    std = statistics.stdev(data)
    if std == 0:
        return 0.0
    kurt = sum((x - mean) ** 4 for x in data) / (n * std ** 4) - 3
    return kurt


def detect_bursts(ikt_values: List[float], threshold_ms: float = 150) -> List[List[float]]:
    """Detect typing bursts - sequences of rapid keystrokes"""
    if not ikt_values:
        return []
    
    bursts = []
    current_burst = []
    
    for ikt in ikt_values:
        if ikt < threshold_ms:
            current_burst.append(ikt)
        else:
            if len(current_burst) >= 3:
                bursts.append(current_burst)
            current_burst = []
    
    if len(current_burst) >= 3:
        bursts.append(current_burst)
    
    return bursts


def calculate_rhythm_consistency(ikt_values: List[float]) -> float:
    """Calculate rhythm consistency score (0-100)"""
    if len(ikt_values) < 5:
        return 50.0
    
    cv = statistics.stdev(ikt_values) / statistics.mean(ikt_values) if statistics.mean(ikt_values) > 0 else 1
    
    window_size = min(10, len(ikt_values) // 3)
    local_cvs = []
    for i in range(len(ikt_values) - window_size):
        window = ikt_values[i:i+window_size]
        local_cv = statistics.stdev(window) / statistics.mean(window) if statistics.mean(window) > 0 else 1
        local_cvs.append(local_cv)
    
    avg_local_cv = statistics.mean(local_cvs) if local_cvs else cv
    consistency = 100 * (1 - min(1, (cv * 0.4 + avg_local_cv * 0.6)))
    
    return max(0, min(100, consistency))


def calculate_flow_state_probability(ikt_values: List[float], correction_rate: float) -> float:
    """Calculate probability of being in flow state"""
    if len(ikt_values) < 10:
        return 0.0
    
    rhythm_score = calculate_rhythm_consistency(ikt_values) / 100
    correction_score = max(0, 1 - correction_rate * 5)
    
    bursts = detect_bursts(ikt_values)
    if bursts:
        avg_burst_length = statistics.mean([len(b) for b in bursts])
        burst_score = min(1, avg_burst_length / 15)
    else:
        burst_score = 0
    
    flow_prob = (rhythm_score * 0.4 + correction_score * 0.35 + burst_score * 0.25)
    return min(1, max(0, flow_prob))


def calculate_cognitive_load_index(ikt_values: List[float], pause_ratio: float, 
                                    correction_rate: float, cv: float) -> float:
    """Calculate cognitive load index (0-100)"""
    if not ikt_values:
        return 50.0
    
    variability_load = min(1, cv) * 30
    pause_load = min(1, pause_ratio * 3) * 35
    correction_load = min(1, correction_rate * 5) * 35
    total_load = variability_load + pause_load + correction_load
    
    return min(100, max(0, total_load))


def calculate_fatigue_indicator(ikt_values: List[float], total_time_ms: float) -> float:
    """Calculate fatigue indicator based on typing pattern degradation"""
    if len(ikt_values) < 20:
        return 0.0
    
    segment_size = len(ikt_values) // 4
    segments = [ikt_values[i*segment_size:(i+1)*segment_size] for i in range(4)]
    
    segment_stds = [statistics.stdev(seg) if len(seg) > 1 else 0 for seg in segments]
    segment_means = [statistics.mean(seg) if seg else 0 for seg in segments]
    
    if len(segment_stds) >= 2:
        std_trend = (segment_stds[-1] - segment_stds[0]) / max(1, segment_stds[0])
        mean_trend = (segment_means[-1] - segment_means[0]) / max(1, segment_means[0])
        fatigue = (std_trend * 50 + mean_trend * 50)
        return min(100, max(0, fatigue))
    
    return 0.0


def calculate_attention_stability(ikt_values: List[float], long_pause_positions: List[int]) -> float:
    """Calculate attention stability score (0-100)"""
    if len(ikt_values) < 10:
        return 50.0
    
    rhythm_score = calculate_rhythm_consistency(ikt_values)
    total_keystrokes = len(ikt_values) + 1
    lapse_penalty = (len(long_pause_positions) / total_keystrokes) * 30 if total_keystrokes > 0 else 0
    stability = rhythm_score - lapse_penalty
    return max(0, min(100, stability))


def calculate_typing_proficiency(speed_wpm: float, accuracy: float, 
                                  consistency: float, efficiency: float) -> float:
    """Calculate overall typing proficiency score (0-100)"""
    speed_score = min(100, (speed_wpm / 70) * 100)
    accuracy_score = accuracy * 100
    proficiency = (
        speed_score * 0.25 +
        accuracy_score * 0.30 +
        consistency * 0.25 +
        efficiency * 0.20
    )
    return min(100, max(0, proficiency))


def calculate_efficiency_score(burst_speed: float, sustainable_speed: float,
                                correction_rate: float, pause_ratio: float) -> float:
    """Calculate typing efficiency score (0-100)"""
    speed_efficiency = (sustainable_speed / max(1, burst_speed)) * 100 if burst_speed > 0 else 50
    output_efficiency = (1 - correction_rate) * 100
    time_efficiency = (1 - pause_ratio) * 100
    efficiency = speed_efficiency * 0.3 + output_efficiency * 0.4 + time_efficiency * 0.3
    return min(100, max(0, efficiency))


def calculate_professional_typing_metrics(
    keystrokes: List[KeystrokeEvent], 
    total_chars: int,
    expected_text: str,
    actual_text: str = None
) -> Dict[str, Any]:
    """Calculate comprehensive professional typing metrics"""
    if len(keystrokes) < 2:
        return {
            "error": "Insufficient keystroke data",
            "minimum_required": 2,
            "provided": len(keystrokes)
        }
    
    # Calculate inter-keystroke times
    ikt_values = []
    pause_positions = []
    long_pause_positions = []
    very_long_pause_positions = []
    
    for i in range(1, len(keystrokes)):
        ikt = keystrokes[i].timestamp - keystrokes[i-1].timestamp
        ikt_values.append(ikt)
        
        if ikt > 800:
            pause_positions.append(i)
        if ikt > 1500:
            long_pause_positions.append(i)
        if ikt > 3000:
            very_long_pause_positions.append(i)
    
    # Basic statistics
    mean_ikt = statistics.mean(ikt_values)
    std_ikt = statistics.stdev(ikt_values) if len(ikt_values) > 1 else 0
    median_ikt = statistics.median(ikt_values)
    
    rounded_ikts = [round(ikt / 10) * 10 for ikt in ikt_values]
    try:
        mode_ikt = statistics.mode(rounded_ikts)
    except statistics.StatisticsError:
        mode_ikt = median_ikt
    
    # Advanced statistics
    cv = std_ikt / mean_ikt if mean_ikt > 0 else 0
    skewness = calculate_skewness(ikt_values)
    kurtosis = calculate_kurtosis(ikt_values)
    
    p25 = calculate_percentile(ikt_values, 25)
    p75 = calculate_percentile(ikt_values, 75)
    p95 = calculate_percentile(ikt_values, 95)
    iqr = p75 - p25
    
    # Speed calculations
    total_time_ms = keystrokes[-1].timestamp - keystrokes[0].timestamp
    total_time_min = total_time_ms / 60000
    
    typing_speed_cpm = total_chars / total_time_min if total_time_min > 0 else 0
    typing_speed_wpm = typing_speed_cpm / 5
    
    # Burst analysis
    bursts = detect_bursts(ikt_values)
    if bursts:
        burst_speeds = []
        for burst in bursts:
            burst_time = sum(burst) / 60000
            burst_chars = len(burst) + 1
            burst_speed = burst_chars / burst_time if burst_time > 0 else 0
            burst_speeds.append(burst_speed)
        burst_speed_cpm = statistics.mean(burst_speeds) if burst_speeds else typing_speed_cpm
    else:
        burst_speed_cpm = typing_speed_cpm
    
    active_time = sum(ikt_values) / 60000
    sustainable_speed_cpm = total_chars / active_time if active_time > 0 else typing_speed_cpm
    
    # Error analysis
    backspace_count = sum(1 for k in keystrokes if k.is_backspace)
    total_keystrokes = len(keystrokes)
    correction_rate = backspace_count / total_keystrokes if total_keystrokes > 0 else 0
    
    immediate_corrections = 0
    delayed_corrections = 0
    for i, k in enumerate(keystrokes):
        if k.is_backspace:
            if i > 0 and (keystrokes[i].timestamp - keystrokes[i-1].timestamp) < 500:
                immediate_corrections += 1
            else:
                delayed_corrections += 1
    
    immediate_correction_rate = immediate_corrections / total_keystrokes if total_keystrokes > 0 else 0
    delayed_correction_rate = delayed_corrections / total_keystrokes if total_keystrokes > 0 else 0
    
    error_burst_count = 0
    consecutive_corrections = 0
    for k in keystrokes:
        if k.is_backspace:
            consecutive_corrections += 1
            if consecutive_corrections >= 3:
                error_burst_count += 1
                consecutive_corrections = 0
        else:
            consecutive_corrections = 0
    
    # Pause analysis
    pause_count = len(pause_positions)
    long_pause_count = len(long_pause_positions)
    very_long_pause_count = len(very_long_pause_positions)
    
    pause_ratio = pause_count / total_keystrokes if total_keystrokes > 0 else 0
    long_pause_ratio = long_pause_count / total_keystrokes if total_keystrokes > 0 else 0
    very_long_pause_ratio = very_long_pause_count / total_keystrokes if total_keystrokes > 0 else 0
    
    pause_durations = [ikt for ikt in ikt_values if ikt > 800]
    mean_pause_duration = statistics.mean(pause_durations) if pause_durations else 0
    
    if len(pause_positions) > 1:
        pause_intervals = [pause_positions[i] - pause_positions[i-1] 
                          for i in range(1, len(pause_positions))]
        pause_pattern_regularity = 1 - (statistics.stdev(pause_intervals) / 
                                        statistics.mean(pause_intervals)) if pause_intervals and statistics.mean(pause_intervals) > 0 else 0
    else:
        pause_pattern_regularity = 1.0
    
    micro_pauses = sum(1 for ikt in ikt_values if 150 <= ikt <= 400)
    micro_pause_frequency = (micro_pauses / total_chars) * 100 if total_chars > 0 else 0
    
    rhythm_consistency = calculate_rhythm_consistency(ikt_values)
    flow_probability = calculate_flow_state_probability(ikt_values, correction_rate)
    cognitive_load = calculate_cognitive_load_index(ikt_values, pause_ratio, correction_rate, cv)
    fatigue = calculate_fatigue_indicator(ikt_values, total_time_ms)
    attention = calculate_attention_stability(ikt_values, long_pause_positions)
    
    if actual_text and expected_text:
        correct_chars = sum(1 for a, e in zip(actual_text, expected_text) if a == e)
        accuracy = correct_chars / len(expected_text) if expected_text else 0
    else:
        accuracy = max(0, 1 - correction_rate * 2)
    
    efficiency = calculate_efficiency_score(
        burst_speed_cpm, sustainable_speed_cpm, correction_rate, pause_ratio
    )
    
    proficiency = calculate_typing_proficiency(
        typing_speed_wpm, accuracy, rhythm_consistency, efficiency
    )
    
    return {
        "mean_ikt_ms": round(mean_ikt, 2),
        "std_ikt_ms": round(std_ikt, 2),
        "median_ikt_ms": round(median_ikt, 2),
        "mode_ikt_ms": round(mode_ikt, 2),
        "coefficient_of_variation": round(cv, 4),
        "skewness": round(skewness, 4),
        "kurtosis": round(kurtosis, 4),
        "percentile_25_ms": round(p25, 2),
        "percentile_75_ms": round(p75, 2),
        "percentile_95_ms": round(p95, 2),
        "interquartile_range_ms": round(iqr, 2),
        "typing_speed_cpm": round(typing_speed_cpm, 2),
        "typing_speed_wpm": round(typing_speed_wpm, 2),
        "burst_speed_cpm": round(burst_speed_cpm, 2),
        "sustainable_speed_cpm": round(sustainable_speed_cpm, 2),
        "rhythm_consistency_score": round(rhythm_consistency, 2),
        "flow_state_probability": round(flow_probability, 4),
        "micro_pause_frequency": round(micro_pause_frequency, 2),
        "correction_rate": round(correction_rate, 4),
        "immediate_correction_rate": round(immediate_correction_rate, 4),
        "delayed_correction_rate": round(delayed_correction_rate, 4),
        "error_burst_count": error_burst_count,
        "total_backspaces": backspace_count,
        "pause_ratio": round(pause_ratio, 4),
        "long_pause_ratio": round(long_pause_ratio, 4),
        "very_long_pause_ratio": round(very_long_pause_ratio, 4),
        "mean_pause_duration_ms": round(mean_pause_duration, 2),
        "pause_pattern_regularity": round(pause_pattern_regularity, 4),
        "total_pauses": pause_count,
        "long_pauses": long_pause_count,
        "very_long_pauses": very_long_pause_count,
        "cognitive_load_index": round(cognitive_load, 2),
        "fatigue_indicator": round(fatigue, 2),
        "attention_stability": round(attention, 2),
        "typing_proficiency_score": round(proficiency, 2),
        "consistency_rating": round(rhythm_consistency, 2),
        "efficiency_score": round(efficiency, 2),
        "accuracy_estimate": round(accuracy, 4),
        "total_keystrokes": total_keystrokes,
        "total_time_ms": round(total_time_ms, 2),
        "burst_count": len(bursts),
        "average_burst_length": round(statistics.mean([len(b) for b in bursts]), 2) if bursts else 0
    }


def calculate_professional_cognitive_profile(
    stages: List[CodingStageData],
    typing_baseline: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate comprehensive cognitive profile from coding test stages"""
    if not stages:
        return {"error": "No stage data provided"}
    
    baseline_std = typing_baseline.get("std_ikt_ms", 0) if typing_baseline else 0
    baseline_cv = typing_baseline.get("coefficient_of_variation", 0) if typing_baseline else 0
    baseline_correction = typing_baseline.get("correction_rate", 0) if typing_baseline else 0
    
    stage_analyses = []
    for stage in stages:
        keystrokes = stage.keystrokes
        
        ikt_values = []
        for i in range(1, len(keystrokes)):
            ikt = keystrokes[i].timestamp - keystrokes[i-1].timestamp
            ikt_values.append(ikt)
        
        stage_std = statistics.stdev(ikt_values) if len(ikt_values) > 1 else 0
        stage_mean = statistics.mean(ikt_values) if ikt_values else 0
        stage_cv = stage_std / stage_mean if stage_mean > 0 else 0
        
        total_keystrokes = len(keystrokes)
        correction_rate = stage.backspace_count / total_keystrokes if total_keystrokes > 0 else 0
        
        total_time_min = stage.total_time / 60000
        chars_typed = total_keystrokes - stage.backspace_count
        speed_cpm = chars_typed / total_time_min if total_time_min > 0 else 0
        
        pause_ratio = stage.pause_events / total_keystrokes if total_keystrokes > 0 else 0
        cognitive_load = calculate_cognitive_load_index(
            ikt_values, pause_ratio, correction_rate, stage_cv
        )
        
        flow_prob = calculate_flow_state_probability(ikt_values, correction_rate)
        
        stage_analyses.append({
            "stage": stage.stage,
            "std_ikt": stage_std,
            "mean_ikt": stage_mean,
            "cv": stage_cv,
            "correction_rate": correction_rate,
            "speed_cpm": speed_cpm,
            "cognitive_load": cognitive_load,
            "flow_probability": flow_prob,
            "latency": stage.time_to_first_keystroke,
            "total_time": stage.total_time,
            "pause_events": stage.pause_events,
            "long_pause_events": stage.long_pause_events,
            "rewrite_count": stage.rewrite_count
        })
    
    if len(stage_analyses) > 1:
        first = stage_analyses[0]
        last = stage_analyses[-1]
        
        std_shift = last["std_ikt"] - first["std_ikt"]
        correction_shift = last["correction_rate"] - first["correction_rate"]
        latency_shift = last["latency"] - first["latency"]
        speed_shift = last["speed_cpm"] - first["speed_cpm"]
    else:
        std_shift = correction_shift = latency_shift = speed_shift = 0
    
    total_long_pauses = sum(s["long_pause_events"] for s in stage_analyses)
    total_rewrites = sum(s["rewrite_count"] for s in stage_analyses)
    total_time_sec = sum(s["total_time"] for s in stage_analyses) / 1000
    
    frustration_index = (total_long_pauses * 2 + total_rewrites * 3) / total_time_sec if total_time_sec > 0 else 0
    
    if len(stage_analyses) > 1:
        load_values = [s["cognitive_load"] for s in stage_analyses]
        stress_accumulation = (load_values[-1] - load_values[0]) / max(1, load_values[0])
    else:
        stress_accumulation = 0
    
    avg_cognitive_load = statistics.mean([s["cognitive_load"] for s in stage_analyses])
    overload_probability = min(1, avg_cognitive_load / 80)
    
    current_std = stage_analyses[-1]["std_ikt"] if stage_analyses else 0
    load_sensitivity = (current_std - baseline_std) / baseline_std if baseline_std > 0 else 0
    
    if len(stage_analyses) > 1:
        speed_values = [s["speed_cpm"] for s in stage_analyses]
        speed_stability = 1 - (statistics.stdev(speed_values) / statistics.mean(speed_values)) if statistics.mean(speed_values) > 0 else 0
        adaptive_capacity = speed_stability * 100
    else:
        adaptive_capacity = 100
    
    if len(stage_analyses) >= 3:
        recovery_score = 0
        for i in range(2, len(stage_analyses)):
            if stage_analyses[i]["cognitive_load"] < stage_analyses[i-1]["cognitive_load"]:
                recovery_score += 1
        recovery_rate = recovery_score / (len(stage_analyses) - 2) if len(stage_analyses) > 2 else 1
    else:
        recovery_rate = 1
    
    flow_probabilities = [s["flow_probability"] for s in stage_analyses]
    avg_flow = statistics.mean(flow_probabilities) if flow_probabilities else 0
    
    flow_threshold = 0.6
    flow_entries = 0
    flow_exits = 0
    in_flow = False
    
    for fp in flow_probabilities:
        if fp >= flow_threshold and not in_flow:
            flow_entries += 1
            in_flow = True
        elif fp < flow_threshold and in_flow:
            flow_exits += 1
            in_flow = False
    
    flow_durations = []
    current_duration = 0
    for fp in flow_probabilities:
        if fp >= flow_threshold:
            current_duration += 1
        else:
            if current_duration > 0:
                flow_durations.append(current_duration)
            current_duration = 0
    if current_duration > 0:
        flow_durations.append(current_duration)
    
    avg_flow_duration = statistics.mean(flow_durations) if flow_durations else 0
    flow_duration_ratio = sum(flow_durations) / len(stage_analyses) if stage_analyses else 0
    
    total_time = sum(s["total_time"] for s in stage_analyses)
    total_chars = sum(len(stages[i].keystrokes) - stages[i].backspace_count 
                      for i in range(len(stages)))
    problem_solving_efficiency = (total_chars / (total_time / 1000)) if total_time > 0 else 0
    
    iteration_tendency = sum(s["rewrite_count"] for s in stage_analyses) / len(stage_analyses) if stage_analyses else 0
    
    exploration_score = statistics.mean([s["correction_rate"] * (1 - s["pause_ratio"]) 
                                         for s in stage_analyses])
    exploitation_score = statistics.mean([(1 - s["correction_rate"]) * (1 - s["cv"]) 
                                          for s in stage_analyses])
    exploration_vs_exploitation = exploration_score / (exploration_score + exploitation_score) if (exploration_score + exploitation_score) > 0 else 0.5
    
    endurance_score = adaptive_capacity * (1 - stress_accumulation) * (1 - overload_probability)
    endurance_score = max(0, min(100, endurance_score * 100))
    
    if len(stage_analyses) > 1:
        performance_trend = []
        for i in range(1, len(stage_analyses)):
            perf_change = (stage_analyses[i-1]["speed_cpm"] - stage_analyses[i]["speed_cpm"]) / max(1, stage_analyses[i-1]["speed_cpm"])
            performance_trend.append(perf_change)
        degradation_rate = statistics.mean(performance_trend) if performance_trend else 0
    else:
        degradation_rate = 0
    
    avg_stage_time = statistics.mean([s["total_time"] for s in stage_analyses]) / 60000
    optimal_session = avg_stage_time * (1 - degradation_rate) * (1 - overload_probability) * 3
    optimal_session = max(15, min(120, optimal_session))
    
    cognitive_flexibility = (adaptive_capacity * 0.4 + 
                            (1 - abs(exploration_vs_exploitation - 0.5) * 2) * 30 +
                            recovery_rate * 30)
    
    focus_endurance = endurance_score
    
    problem_solving_score = (problem_solving_efficiency * 0.3 + 
                            (1 - iteration_tendency / 5) * 35 +
                            (1 - frustration_index) * 35)
    
    return {
        "std_shift_between_stages": round(std_shift, 2),
        "correction_shift": round(correction_shift, 4),
        "latency_shift_ms": round(latency_shift, 2),
        "speed_shift_cpm": round(speed_shift, 2),
        "frustration_index": round(frustration_index, 4),
        "stress_accumulation_rate": round(stress_accumulation, 4),
        "cognitive_overload_probability": round(overload_probability, 4),
        "load_sensitivity": round(load_sensitivity, 4),
        "adaptive_capacity": round(adaptive_capacity, 2),
        "recovery_rate": round(recovery_rate, 4),
        "flow_state_duration_ratio": round(flow_duration_ratio, 4),
        "flow_entry_count": flow_entries,
        "flow_exit_count": flow_exits,
        "average_flow_duration_stages": round(avg_flow_duration, 2),
        "average_flow_probability": round(avg_flow, 4),
        "problem_solving_efficiency": round(problem_solving_efficiency, 4),
        "iteration_tendency": round(iteration_tendency, 4),
        "exploration_vs_exploitation_ratio": round(exploration_vs_exploitation, 4),
        "endurance_score": round(endurance_score, 2),
        "degradation_rate": round(degradation_rate, 4),
        "optimal_session_length_minutes": round(optimal_session, 1),
        "cognitive_flexibility_score": round(cognitive_flexibility, 2),
        "focus_endurance_score": round(focus_endurance, 2),
        "problem_solving_score": round(max(0, min(100, problem_solving_score)), 2),
        "completed_stages": len(stages),
        "stage_analyses": stage_analyses
    }


def calculate_experience_factor(years: int, daily_hours: int, 
                                 language: str, multitask: str) -> Dict[str, Any]:
    """Calculate comprehensive experience factor"""
    base_factor = math.log(years + 1) / math.log(15)
    intensity_factor = daily_hours / 8
    
    language_complexity = {
        "C": 1.2,
        "C++": 1.15,
        "Java": 1.0,
        "Python": 0.9,
        "JavaScript": 0.95
    }
    lang_factor = language_complexity.get(language, 1.0)
    
    multitask_factors = {"Low": 1.1, "Medium": 1.0, "High": 0.85}
    multitask_factor = multitask_factors.get(multitask, 1.0)
    
    combined = base_factor * (1 + intensity_factor * 0.2) * lang_factor * multitask_factor
    
    if combined >= 1.5:
        level = ExpertiseLevel.MASTER
    elif combined >= 1.2:
        level = ExpertiseLevel.EXPERT
    elif combined >= 0.8:
        level = ExpertiseLevel.ADVANCED
    elif combined >= 0.4:
        level = ExpertiseLevel.INTERMEDIATE
    else:
        level = ExpertiseLevel.NOVICE
    
    return {
        "experience_factor": round(combined, 4),
        "base_factor": round(base_factor, 4),
        "intensity_factor": round(intensity_factor, 4),
        "language_factor": round(lang_factor, 4),
        "multitask_factor": round(multitask_factor, 4),
        "expertise_level": level.value
    }


def calculate_stability_modifier(focus_stability: int, 
                                  typing_consistency: float = None) -> Dict[str, Any]:
    """Calculate stability modifier"""
    base_modifier = 0.7 + (focus_stability - 1) * 0.15
    
    if typing_consistency is not None:
        measured_factor = typing_consistency / 100
        blended = base_modifier * 0.6 + (0.7 + measured_factor * 0.6) * 0.4
    else:
        blended = base_modifier
    
    if blended >= 1.2:
        stability_class = StabilityClass.HIGHLY_STABLE
    elif blended >= 1.0:
        stability_class = StabilityClass.STABLE
    elif blended >= 0.9:
        stability_class = StabilityClass.MODERATE
    elif blended >= 0.8:
        stability_class = StabilityClass.VARIABLE
    else:
        stability_class = StabilityClass.HIGHLY_VARIABLE
    
    return {
        "stability_modifier": round(blended, 4),
        "base_modifier": round(base_modifier, 4),
        "stability_class": stability_class.value
    }


def classify_professional_metrics(typing: Dict, cognitive: Dict) -> Dict[str, Any]:
    """Generate professional classifications"""
    classifications = {}
    
    cv = typing.get("coefficient_of_variation", 0)
    rhythm = typing.get("rhythm_consistency_score", 0)
    
    if cv < 0.2 and rhythm > 80:
        typing_stability = "Highly Stable"
        confidence = 0.9
    elif cv < 0.35 and rhythm > 60:
        typing_stability = "Stable"
        confidence = 0.8
    elif cv < 0.5 and rhythm > 40:
        typing_stability = "Moderate"
        confidence = 0.7
    elif cv < 0.7:
        typing_stability = "Variable"
        confidence = 0.6
    else:
        typing_stability = "Highly Variable"
        confidence = 0.5
    
    classifications["typing_stability"] = {
        "classification": typing_stability,
        "confidence": round(confidence, 2),
        "cv_score": round(cv, 4),
        "rhythm_score": round(rhythm, 2)
    }
    
    correction = typing.get("correction_rate", 0)
    immediate = typing.get("immediate_correction_rate", 0)
    
    if correction < 0.03:
        intensity = "Minimal"
        confidence = 0.85
    elif correction < 0.08:
        intensity = "Low"
        confidence = 0.8
    elif correction < 0.15:
        intensity = "Moderate"
        confidence = 0.75
    elif correction < 0.25:
        intensity = "High"
        confidence = 0.7
    else:
        intensity = "Very High"
        confidence = 0.65
    
    classifications["correction_intensity"] = {
        "classification": intensity,
        "confidence": round(confidence, 2),
        "correction_rate": round(correction, 4),
        "immediate_ratio": round(immediate / correction, 4) if correction > 0 else 0
    }
    
    if cognitive:
        sensitivity = cognitive.get("load_sensitivity", 0)
        adaptive = cognitive.get("adaptive_capacity", 0)
        
        if sensitivity < 0.1 and adaptive > 80:
            load_class = "Low"
            confidence = 0.85
        elif sensitivity < 0.25 and adaptive > 60:
            load_class = "Low-Moderate"
            confidence = 0.75
        elif sensitivity < 0.4 and adaptive > 40:
            load_class = "Moderate"
            confidence = 0.7
        elif sensitivity < 0.6:
            load_class = "High"
            confidence = 0.65
        else:
            load_class = "Very High"
            confidence = 0.6
        
        classifications["load_sensitivity"] = {
            "classification": load_class,
            "confidence": round(confidence, 2),
            "sensitivity_score": round(sensitivity, 4),
            "adaptive_capacity": round(adaptive, 2)
        }
        
        frustration = cognitive.get("frustration_index", 0)
        overload = cognitive.get("cognitive_overload_probability", 0)
        
        if frustration < 0.05 and overload < 0.2:
            frustr_class = "Low"
            confidence = 0.85
        elif frustration < 0.15 and overload < 0.4:
            frustr_class = "Low-Moderate"
            confidence = 0.75
        elif frustration < 0.3 and overload < 0.6:
            frustr_class = "Moderate"
            confidence = 0.7
        elif frustration < 0.5:
            frustr_class = "High"
            confidence = 0.65
        else:
            frustr_class = "Very High"
            confidence = 0.6
        
        classifications["frustration_index"] = {
            "classification": frustr_class,
            "confidence": round(confidence, 2),
            "frustration_score": round(frustration, 4),
            "overload_probability": round(overload, 4)
        }
        
        flow_prob = cognitive.get("average_flow_probability", 0)
        endurance = cognitive.get("endurance_score", 0)
        
        if flow_prob > 0.6 and endurance > 70:
            state = CognitiveState.FLOW
        elif flow_prob > 0.4 and endurance > 50:
            state = CognitiveState.FOCUSED
        elif overload > 0.7:
            state = CognitiveState.OVERLOADED
        elif frustration > 0.4:
            state = CognitiveState.STRESSED
        else:
            state = CognitiveState.NORMAL
        
        classifications["cognitive_state"] = {
            "classification": state.value,
            "flow_probability": round(flow_prob, 4),
            "endurance_score": round(endurance, 2)
        }
    else:
        classifications["load_sensitivity"] = {"classification": "N/A", "confidence": 0}
        classifications["frustration_index"] = {"classification": "N/A", "confidence": 0}
        classifications["cognitive_state"] = {"classification": "N/A", "confidence": 0}
    
    return classifications


# ================== NEW API ENDPOINTS ==================

class StartSessionRequest(BaseModel):
    """Request body for starting a session"""
    employee_id: str = Field(..., min_length=3, max_length=50)


@app.post("/start-session")
async def start_session(request: StartSessionRequest):
    """
    Initialize new session and check for existing attempts.
    Enforces one-attempt-per-employee rule.
    """
    employee_id = request.employee_id
    # Check if employee already has a session
    existing = db.check_existing_session(employee_id)
    if existing:
        return {
            "status": "error",
            "message": "Employee has already completed an assessment",
            "existing_session_id": existing
        }
    
    # Generate new session ID
    session_id = str(uuid.uuid4())
    
    # Create session in database
    db.create_session(session_id, employee_id)
    
    return {
        "status": "success",
        "session_id": session_id,
        "message": "Session created successfully"
    }


@app.post("/employee-info")
async def save_employee_info(employee_info: EmployeeInfo):
    """Save employee demographic information"""
    # Set timestamp if not provided
    if not employee_info.timestamp:
        employee_info.timestamp = time.time()
    
    # Save to database
    db.save_employee(employee_info)
    
    return {
        "status": "success",
        "session_id": employee_info.session_id,
        "message": "Employee information saved"
    }


@app.post("/classification")
async def classify_employee(classification_input: ClassificationInput):
    """
    Classify employee into professional role based on questionnaire answers.
    """
    # Perform classification
    result = classify_professional_role(classification_input.answers)
    result.session_id = classification_input.session_id
    
    # Save to database
    db.save_classification(result)
    
    return {
        "status": "success",
        "classification": result.dict(),
        "message": "Professional role classified"
    }


@app.post("/hardware-info")
async def save_hardware_info(hardware: HardwareDetails):
    """Save hardware and environment details"""
    # Save to database
    db.save_hardware(hardware)
    
    return {
        "status": "success",
        "message": "Hardware information saved"
    }


@app.post("/mouse-metrics")
async def save_mouse_metrics(mouse_data: MouseMetricsInput):
    """
    Process and save mouse behavior metrics.
    Calculate accuracy, reaction time, and proficiency scores.
    """
    # Calculate metrics
    metrics = calculate_mouse_metrics(mouse_data)
    
    # Save to database
    db.save_mouse_metrics(metrics)
    
    return {
        "status": "success",
        "metrics": metrics.dict(),
        "message": "Mouse metrics saved"
    }


@app.post("/role-specific-test")
async def save_role_test_result(test_result: RoleTestResult):
    """
    Save role-specific test result.
    Validate anti-cheat flags and calculate scores.
    """
    # Validate for suspicious activity
    validation = anti_cheat.validate_test_result(test_result)
    
    if validation["suspicious"]:
        test_result.suspicious_activity = True
    
    # Save to database
    db.save_role_test(test_result)
    
    return {
        "status": "success",
        "result": test_result.dict(),
        "validation": validation,
        "message": "Role test result saved"
    }


@app.get("/test-content/{category}")
async def get_test_content(category: str, test_number: int = 0):
    """
    Return test content for specified role category.
    If test_number is provided, return that specific test.
    Otherwise, return all tests.
    """
    if category not in ROLE_TESTS:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
    
    tests = ROLE_TESTS[category]
    
    # If test_number is provided, return that specific test
    if test_number is not None and test_number >= 0:
        # Cycle through tests if test_number exceeds available tests
        test_index = test_number % len(tests)
        selected_test = tests[test_index]
        return {
            "status": "success",
            "category": category,
            "test": {
                "id": selected_test["test_id"],
                "name": selected_test["test_name"],
                "prompt": selected_test["prompt"],
                "code_snippet": selected_test.get("initial_code") or selected_test.get("expected_code") or ""
            }
        }
    
    return {
        "status": "success",
        "category": category,
        "tests": tests,
        "count": len(tests)
    }


@app.post("/anti-cheat-event")
async def log_anti_cheat_event(event: AntiCheatEvent):
    """Log anti-cheat event from client"""
    # Save event to database
    db.save_anti_cheat_event(event)
    
    # Get event count for this session
    events = db.get_anti_cheat_summary(event.session_id)
    total_events = sum(events.values())
    
    # Flag if threshold exceeded
    flagged = total_events > 20
    
    return {
        "status": "success",
        "message": "Anti-cheat event logged",
        "total_events": total_events,
        "flagged": flagged
    }


@app.get("/complete-session/{session_id}")
async def get_complete_session(session_id: str, admin_key: Optional[str] = None):
    """
    Retrieve complete session data including hidden analytics.
    Requires admin authentication in production.
    """
    # In production, validate admin_key here
    # For MVP, we'll allow access without key
    
    # Get session data
    session_data_dict = db.get_session_data(session_id)
    
    if not session_data_dict:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get anti-cheat summary
    anti_cheat_summary = db.get_anti_cheat_summary(session_id)
    
    return {
        "status": "success",
        "session_id": session_id,
        "session_data": session_data_dict,
        "anti_cheat_summary": anti_cheat_summary,
        "message": "Complete session data retrieved"
    }


@app.get("/session-status/{session_id}")
async def get_session_status(session_id: str):
    """Get current session status"""
    # This would query the sessions table for status
    # For now, return a simple response
    return {
        "status": "success",
        "session_id": session_id,
        "message": "Session status retrieved"
    }


# ================== EXISTING API ENDPOINTS (PRESERVED) ==================

@app.post("/profile")
async def save_profile(profile: ProfileData):
    """Save profile data and calculate comprehensive experience metrics"""
    exp_result = calculate_experience_factor(
        profile.years_coding,
        profile.daily_hours,
        profile.primary_language,
        profile.multitask_level
    )
    
    stab_result = calculate_stability_modifier(profile.focus_stability)
    
    session_data.profile = {
        "years_coding": profile.years_coding,
        "daily_hours": profile.daily_hours,
        "primary_language": profile.primary_language,
        "focus_stability": profile.focus_stability,
        "multitask_level": profile.multitask_level,
        "typing_frequency": profile.typing_frequency,
        "error_correction_style": profile.error_correction_style,
        "preferred_complexity": profile.preferred_complexity
    }
    
    session_data.baseline["experience_factor"] = exp_result["experience_factor"]
    session_data.baseline["stability_modifier"] = stab_result["stability_modifier"]
    session_data.baseline["expertise_level"] = exp_result["expertise_level"]
    
    return {
        "status": "success",
        "experience_analysis": exp_result,
        "stability_analysis": stab_result
    }


@app.post("/typing-metrics")
async def save_typing_metrics(data: TypingMetricsInput):
    """Process typing test data with professional-grade analysis"""
    metrics = calculate_professional_typing_metrics(
        data.keystrokes,
        data.total_chars,
        data.expected_text,
        data.actual_text
    )
    
    session_data.typing_metrics = [k.dict() for k in data.keystrokes]
    session_data.baseline["keyboard"] = metrics
    
    if session_data.profile:
        stab_result = calculate_stability_modifier(
            session_data.profile["focus_stability"],
            metrics.get("rhythm_consistency_score")
        )
        session_data.baseline["stability_modifier"] = stab_result["stability_modifier"]
    
    return {
        "status": "success",
        "metrics": metrics
    }


@app.post("/coding-metrics")
async def save_coding_metrics(data: CodingMetricsInput):
    """Process coding test data with professional cognitive analysis"""
    typing_baseline = session_data.baseline.get("keyboard", {})
    
    cognitive_profile = calculate_professional_cognitive_profile(
        data.stages,
        typing_baseline
    )
    
    session_data.coding_metrics = [s.dict() for s in data.stages]
    session_data.baseline["cognitive_profile"] = cognitive_profile
    
    return {
        "status": "success",
        "cognitive_profile": cognitive_profile,
        "completed_stages": data.completed_stages
    }


@app.get("/summary")
async def get_summary():
    """Get comprehensive calibration summary with professional classifications"""
    profile = session_data.profile
    baseline = session_data.baseline
    
    keyboard = baseline.get("keyboard") or {}
    cognitive = baseline.get("cognitive_profile") or {}
    
    classifications = classify_professional_metrics(keyboard, cognitive)
    
    confidence_factors = []
    if keyboard:
        confidence_factors.append(keyboard.get("total_keystrokes", 0) / 500)
    if cognitive:
        confidence_factors.append(cognitive.get("completed_stages", 0) / 3)
    if profile:
        confidence_factors.append(0.5)
    
    baseline_confidence = statistics.mean(confidence_factors) if confidence_factors else 0
    baseline_confidence = min(1, baseline_confidence)
    
    summary = {
        "profile": profile,
        "classifications": classifications,
        "baseline_vector": {
            "keyboard": keyboard,
            "cognitive_profile": cognitive,
            "experience_factor": baseline.get("experience_factor"),
            "stability_modifier": baseline.get("stability_modifier"),
            "expertise_level": baseline.get("expertise_level")
        },
        "calibration_metadata": {
            "baseline_confidence": round(baseline_confidence, 4),
            "calibration_timestamp": time.time(),
            "data_completeness": {
                "has_profile": profile is not None,
                "has_typing_metrics": keyboard is not None and len(keyboard) > 0,
                "has_cognitive_metrics": cognitive is not None and len(cognitive) > 0
            }
        }
    }
    
    return summary


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Employee Assessment API - Professional Edition v3.0",
        "features": [
            "Advanced statistical analysis",
            "Cognitive load measurement",
            "Flow state detection",
            "Professional classifications",
            "Employee assessment",
            "Role classification",
            "Mouse behavior analysis",
            "Anti-cheat validation",
            "Role-specific testing"
        ]
    }


@app.post("/reset")
async def reset_session():
    """Reset session data for a new calibration"""
    session_data.reset()
    return {
        "status": "success",
        "message": "Session reset successfully"
    }


@app.get("/metrics/definitions")
async def get_metric_definitions():
    """Get definitions of all metrics for documentation"""
    return {
        "typing_metrics": {
            "mean_ikt_ms": "Mean inter-keystroke time in milliseconds",
            "std_ikt_ms": "Standard deviation of inter-keystroke time",
            "coefficient_of_variation": "Ratio of std to mean - consistency measure",
            "skewness": "Asymmetry measure of IKT distribution",
            "kurtosis": "Tailedness measure of IKT distribution",
            "typing_speed_wpm": "Words per minute (5 chars = 1 word)",
            "burst_speed_cpm": "Speed during rapid typing bursts",
            "rhythm_consistency_score": "0-100 score of typing rhythm regularity",
            "flow_state_probability": "Probability of being in flow state",
            "cognitive_load_index": "0-100 index of cognitive load during typing",
            "fatigue_indicator": "0-100 indicator of fatigue development",
            "typing_proficiency_score": "Overall typing proficiency 0-100"
        },
        "cognitive_metrics": {
            "load_sensitivity": "Sensitivity to increased cognitive load",
            "adaptive_capacity": "Ability to maintain performance under load",
            "frustration_index": "Index of frustration indicators",
            "flow_state_duration_ratio": "Ratio of time spent in flow state",
            "cognitive_flexibility_score": "Ability to adapt thinking 0-100",
            "focus_endurance_score": "Ability to maintain focus 0-100",
            "problem_solving_score": "Problem solving efficiency 0-100",
            "optimal_session_length_minutes": "Estimated optimal work session length"
        },
        "mouse_metrics": {
            "mean_accuracy": "Average distance from target in pixels",
            "accuracy_score": "0-100 score based on click accuracy",
            "mean_reaction_time": "Average reaction time in milliseconds",
            "mouse_proficiency_score": "Overall mouse proficiency 0-100",
            "hand_eye_coordination": "Hand-eye coordination score 0-100"
        },
        "classification": {
            "primary_role": "Main professional role (Frontend/Backend/Research/Maintenance)",
            "confidence_score": "Confidence in classification 0-1",
            "role_scores": "Individual scores for each role category"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
