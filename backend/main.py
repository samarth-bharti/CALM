"""
Baseline Calibration Prototype - Professional Edition
======================================================
Advanced behavioral analytics engine with sophisticated metrics,
statistical analysis, and cognitive pattern recognition.

Author: Baseline Calibration System
Version: 2.0.0 Professional
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass
import time

app = FastAPI(
    title="Baseline Calibration API - Professional Edition",
    description="Advanced behavioral analytics with professional-grade metrics",
    version="2.0.0"
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

# ================== DATA MODELS ==================

class ProfileData(BaseModel):
    years_coding: int = Field(ge=0, le=50)
    daily_hours: int = Field(ge=1, le=16)
    primary_language: str
    focus_stability: int = Field(ge=1, le=5)
    multitask_level: str
    # Enhanced profile fields
    typing_frequency: Optional[str] = "medium"  # low, medium, high
    error_correction_style: Optional[str] = "immediate"  # immediate, batch, minimal
    preferred_complexity: Optional[int] = 3  # 1-5 scale


class KeystrokeEvent(BaseModel):
    timestamp: float  # milliseconds
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
    time_to_first_keystroke: float  # ms
    total_time: float  # ms
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


# ================== PROFESSIONAL ANALYTICS CLASSES ==================

@dataclass
class TypingMetricsResult:
    """Comprehensive typing analysis results"""
    # Basic metrics
    mean_ikt: float
    std_ikt: float
    median_ikt: float
    mode_ikt: float
    
    # Advanced statistical measures
    coefficient_of_variation: float
    skewness: float
    kurtosis: float
    percentile_25: float
    percentile_75: float
    percentile_95: float
    interquartile_range: float
    
    # Speed metrics
    typing_speed_cpm: float  # chars per minute
    typing_speed_wpm: float  # words per minute
    burst_speed_cpm: float   # speed during active typing bursts
    sustainable_speed_cpm: float  # adjusted for pauses
    
    # Rhythm analysis
    rhythm_consistency_score: float  # 0-100
    flow_state_probability: float   # 0-1
    micro_pause_frequency: float    # pauses per 100 chars
    
    # Error analysis
    correction_rate: float
    immediate_correction_rate: float
    delayed_correction_rate: float
    error_burst_count: int
    
    # Pause analysis
    pause_ratio: float
    long_pause_ratio: float
    very_long_pause_ratio: float  # >3000ms
    mean_pause_duration: float
    pause_pattern_regularity: float
    
    # Cognitive indicators
    cognitive_load_index: float
    fatigue_indicator: float
    attention_stability: float
    
    # Derived scores
    typing_proficiency_score: float  # 0-100
    consistency_rating: float       # 0-100
    efficiency_score: float         # 0-100


@dataclass
class CognitiveProfileResult:
    """Advanced cognitive analysis results"""
    # Stage progression metrics
    std_shift_between_stages: float
    correction_shift: float
    latency_shift: float
    speed_shift: float
    
    # Frustration and stress indicators
    frustration_index: float
    stress_accumulation_rate: float
    cognitive_overload_probability: float
    
    # Load sensitivity
    load_sensitivity: float
    adaptive_capacity: float
    recovery_rate: float
    
    # Flow analysis
    flow_state_duration_ratio: float
    flow_entry_count: int
    flow_exit_count: int
    average_flow_duration: float
    
    # Problem solving metrics
    problem_solving_efficiency: float
    iteration_tendency: float
    exploration_vs_exploitation: float
    
    # Cognitive endurance
    endurance_score: float
    degradation_rate: float
    optimal_session_length_estimate: float  # minutes
    
    # Overall cognitive score
    cognitive_flexibility_score: float  # 0-100
    focus_endurance_score: float        # 0-100
    problem_solving_score: float        # 0-100


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


# ================== PROFESSIONAL CALCULATION FUNCTIONS ==================

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
    """
    Calculate skewness (asymmetry measure).
    Negative = left-skewed, Positive = right-skewed, 0 = symmetric
    """
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
    """
    Calculate kurtosis (tailedness measure).
    >3 = heavy tails (leptokurtic), <3 = light tails (platykurtic), 3 = normal
    Using excess kurtosis (subtract 3 from Pearson's definition)
    """
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
    """
    Detect typing bursts - sequences of rapid keystrokes.
    Returns list of burst sequences.
    """
    if not ikt_values:
        return []
    
    bursts = []
    current_burst = []
    
    for ikt in ikt_values:
        if ikt < threshold_ms:
            current_burst.append(ikt)
        else:
            if len(current_burst) >= 3:  # Minimum 3 keystrokes for a burst
                bursts.append(current_burst)
            current_burst = []
    
    if len(current_burst) >= 3:
        bursts.append(current_burst)
    
    return bursts


def calculate_rhythm_consistency(ikt_values: List[float]) -> float:
    """
    Calculate rhythm consistency score (0-100).
    Uses coefficient of variation and local variability analysis.
    """
    if len(ikt_values) < 5:
        return 50.0
    
    # Global consistency
    cv = statistics.stdev(ikt_values) / statistics.mean(ikt_values) if statistics.mean(ikt_values) > 0 else 1
    
    # Local consistency (rolling window)
    window_size = min(10, len(ikt_values) // 3)
    local_cvs = []
    for i in range(len(ikt_values) - window_size):
        window = ikt_values[i:i+window_size]
        local_cv = statistics.stdev(window) / statistics.mean(window) if statistics.mean(window) > 0 else 1
        local_cvs.append(local_cv)
    
    avg_local_cv = statistics.mean(local_cvs) if local_cvs else cv
    
    # Combine global and local consistency
    consistency = 100 * (1 - min(1, (cv * 0.4 + avg_local_cv * 0.6)))
    
    return max(0, min(100, consistency))


def calculate_flow_state_probability(ikt_values: List[float], correction_rate: float) -> float:
    """
    Calculate probability of being in flow state.
    Based on rhythm consistency, low correction rate, and sustained activity.
    """
    if len(ikt_values) < 10:
        return 0.0
    
    # Rhythm factor
    rhythm_score = calculate_rhythm_consistency(ikt_values) / 100
    
    # Correction factor (low correction = higher flow probability)
    correction_score = max(0, 1 - correction_rate * 5)
    
    # Sustained activity factor
    bursts = detect_bursts(ikt_values)
    if bursts:
        avg_burst_length = statistics.mean([len(b) for b in bursts])
        burst_score = min(1, avg_burst_length / 15)  # 15+ keystrokes = optimal burst
    else:
        burst_score = 0
    
    # Combined probability
    flow_prob = (rhythm_score * 0.4 + correction_score * 0.35 + burst_score * 0.25)
    
    return min(1, max(0, flow_prob))


def calculate_cognitive_load_index(ikt_values: List[float], pause_ratio: float, 
                                    correction_rate: float, cv: float) -> float:
    """
    Calculate cognitive load index (0-100).
    Higher values indicate higher cognitive load.
    """
    if not ikt_values:
        return 50.0
    
    # Variability factor
    variability_load = min(1, cv) * 30
    
    # Pause factor
    pause_load = min(1, pause_ratio * 3) * 35
    
    # Correction factor
    correction_load = min(1, correction_rate * 5) * 35
    
    total_load = variability_load + pause_load + correction_load
    
    return min(100, max(0, total_load))


def calculate_fatigue_indicator(ikt_values: List[float], total_time_ms: float) -> float:
    """
    Calculate fatigue indicator based on typing pattern degradation over time.
    Returns 0-100 where higher = more fatigue.
    """
    if len(ikt_values) < 20:
        return 0.0
    
    # Split into segments
    segment_size = len(ikt_values) // 4
    segments = [
        ikt_values[i*segment_size:(i+1)*segment_size] 
        for i in range(4)
    ]
    
    # Calculate variability for each segment
    segment_stds = [statistics.stdev(seg) if len(seg) > 1 else 0 for seg in segments]
    segment_means = [statistics.mean(seg) if seg else 0 for seg in segments]
    
    # Check for increasing variability (fatigue sign)
    if len(segment_stds) >= 2:
        std_trend = (segment_stds[-1] - segment_stds[0]) / max(1, segment_stds[0])
        mean_trend = (segment_means[-1] - segment_means[0]) / max(1, segment_means[0])
        
        # Increasing std and mean IKT indicates fatigue
        fatigue = (std_trend * 50 + mean_trend * 50)
        return min(100, max(0, fatigue))
    
    return 0.0


def calculate_attention_stability(ikt_values: List[float], long_pause_positions: List[int]) -> float:
    """
    Calculate attention stability score (0-100).
    Based on consistency and absence of attention lapses.
    """
    if len(ikt_values) < 10:
        return 50.0
    
    # Base stability from rhythm
    rhythm_score = calculate_rhythm_consistency(ikt_values)
    
    # Penalty for long pauses (attention lapses)
    total_keystrokes = len(ikt_values) + 1
    lapse_penalty = (len(long_pause_positions) / total_keystrokes) * 30 if total_keystrokes > 0 else 0
    
    stability = rhythm_score - lapse_penalty
    return max(0, min(100, stability))


def calculate_typing_proficiency(speed_wpm: float, accuracy: float, 
                                  consistency: float, efficiency: float) -> float:
    """
    Calculate overall typing proficiency score (0-100).
    Weighted combination of speed, accuracy, consistency, and efficiency.
    """
    # Speed score (normalized to professional standards)
    # Professional typist: 60-80 WPM, Expert: 80-100+ WPM
    speed_score = min(100, (speed_wpm / 70) * 100)
    
    # Accuracy score
    accuracy_score = accuracy * 100
    
    # Combined proficiency
    proficiency = (
        speed_score * 0.25 +
        accuracy_score * 0.30 +
        consistency * 0.25 +
        efficiency * 0.20
    )
    
    return min(100, max(0, proficiency))


def calculate_efficiency_score(burst_speed: float, sustainable_speed: float,
                                correction_rate: float, pause_ratio: float) -> float:
    """
    Calculate typing efficiency score (0-100).
    Measures how effectively keystrokes translate to output.
    """
    # Speed efficiency
    speed_efficiency = (sustainable_speed / max(1, burst_speed)) * 100 if burst_speed > 0 else 50
    
    # Output efficiency (keystrokes that contribute to output)
    output_efficiency = (1 - correction_rate) * 100
    
    # Time efficiency (time spent typing vs pausing)
    time_efficiency = (1 - pause_ratio) * 100
    
    efficiency = speed_efficiency * 0.3 + output_efficiency * 0.4 + time_efficiency * 0.3
    
    return min(100, max(0, efficiency))


# ================== MAIN CALCULATION FUNCTIONS ==================

def calculate_professional_typing_metrics(
    keystrokes: List[KeystrokeEvent], 
    total_chars: int,
    expected_text: str,
    actual_text: str = None
) -> Dict[str, Any]:
    """
    Calculate comprehensive professional typing metrics.
    
    This is the main typing analysis function that computes all metrics
    including advanced statistical measures, cognitive indicators, and
    derived scores.
    """
    if len(keystrokes) < 2:
        return {
            "error": "Insufficient keystroke data",
            "minimum_required": 2,
            "provided": len(keystrokes)
        }
    
    # Calculate inter-keystroke times
    ikt_values = []
    pause_positions = []  # Positions of pauses > 800ms
    long_pause_positions = []  # Positions of pauses > 1500ms
    very_long_pause_positions = []  # Positions of pauses > 3000ms
    
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
    
    # Mode calculation (using rounded values for binning)
    rounded_ikts = [round(ikt / 10) * 10 for ikt in ikt_values]
    try:
        mode_ikt = statistics.mode(rounded_ikts)
    except statistics.StatisticsError:
        mode_ikt = median_ikt
    
    # Advanced statistics
    cv = std_ikt / mean_ikt if mean_ikt > 0 else 0
    skewness = calculate_skewness(ikt_values)
    kurtosis = calculate_kurtosis(ikt_values)
    
    # Percentiles
    p25 = calculate_percentile(ikt_values, 25)
    p75 = calculate_percentile(ikt_values, 75)
    p95 = calculate_percentile(ikt_values, 95)
    iqr = p75 - p25
    
    # Speed calculations
    total_time_ms = keystrokes[-1].timestamp - keystrokes[0].timestamp
    total_time_min = total_time_ms / 60000
    
    typing_speed_cpm = total_chars / total_time_min if total_time_min > 0 else 0
    typing_speed_wpm = typing_speed_cpm / 5  # Standard: 5 chars = 1 word
    
    # Burst analysis
    bursts = detect_bursts(ikt_values)
    if bursts:
        burst_speeds = []
        for burst in bursts:
            burst_time = sum(burst) / 60000  # Convert to minutes
            burst_chars = len(burst) + 1  # Keystrokes in burst
            burst_speed = burst_chars / burst_time if burst_time > 0 else 0
            burst_speeds.append(burst_speed)
        burst_speed_cpm = statistics.mean(burst_speeds) if burst_speeds else typing_speed_cpm
    else:
        burst_speed_cpm = typing_speed_cpm
    
    # Sustainable speed (adjusted for pauses)
    active_time = sum(ikt_values) / 60000
    sustainable_speed_cpm = total_chars / active_time if active_time > 0 else typing_speed_cpm
    
    # Error analysis
    backspace_count = sum(1 for k in keystrokes if k.is_backspace)
    total_keystrokes = len(keystrokes)
    correction_rate = backspace_count / total_keystrokes if total_keystrokes > 0 else 0
    
    # Immediate vs delayed corrections
    immediate_corrections = 0
    delayed_corrections = 0
    for i, k in enumerate(keystrokes):
        if k.is_backspace:
            # Check if correction happened within 500ms of error
            if i > 0 and (keystrokes[i].timestamp - keystrokes[i-1].timestamp) < 500:
                immediate_corrections += 1
            else:
                delayed_corrections += 1
    
    immediate_correction_rate = immediate_corrections / total_keystrokes if total_keystrokes > 0 else 0
    delayed_correction_rate = delayed_corrections / total_keystrokes if total_keystrokes > 0 else 0
    
    # Error burst detection (multiple corrections in sequence)
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
    
    # Mean pause duration
    pause_durations = [ikt for ikt in ikt_values if ikt > 800]
    mean_pause_duration = statistics.mean(pause_durations) if pause_durations else 0
    
    # Pause pattern regularity
    if len(pause_positions) > 1:
        pause_intervals = [pause_positions[i] - pause_positions[i-1] 
                          for i in range(1, len(pause_positions))]
        pause_pattern_regularity = 1 - (statistics.stdev(pause_intervals) / 
                                        statistics.mean(pause_intervals)) if pause_intervals and statistics.mean(pause_intervals) > 0 else 0
    else:
        pause_pattern_regularity = 1.0
    
    # Micro pause frequency (pauses 150-400ms, natural typing rhythm)
    micro_pauses = sum(1 for ikt in ikt_values if 150 <= ikt <= 400)
    micro_pause_frequency = (micro_pauses / total_chars) * 100 if total_chars > 0 else 0
    
    # Rhythm consistency
    rhythm_consistency = calculate_rhythm_consistency(ikt_values)
    
    # Flow state probability
    flow_probability = calculate_flow_state_probability(ikt_values, correction_rate)
    
    # Cognitive indicators
    cognitive_load = calculate_cognitive_load_index(ikt_values, pause_ratio, correction_rate, cv)
    fatigue = calculate_fatigue_indicator(ikt_values, total_time_ms)
    attention = calculate_attention_stability(ikt_values, long_pause_positions)
    
    # Accuracy calculation (if actual text provided)
    if actual_text and expected_text:
        correct_chars = sum(1 for a, e in zip(actual_text, expected_text) if a == e)
        accuracy = correct_chars / len(expected_text) if expected_text else 0
    else:
        # Estimate accuracy from correction rate
        accuracy = max(0, 1 - correction_rate * 2)
    
    # Efficiency score
    efficiency = calculate_efficiency_score(
        burst_speed_cpm, sustainable_speed_cpm, correction_rate, pause_ratio
    )
    
    # Proficiency score
    proficiency = calculate_typing_proficiency(
        typing_speed_wpm, accuracy, rhythm_consistency, efficiency
    )
    
    return {
        # Basic metrics
        "mean_ikt_ms": round(mean_ikt, 2),
        "std_ikt_ms": round(std_ikt, 2),
        "median_ikt_ms": round(median_ikt, 2),
        "mode_ikt_ms": round(mode_ikt, 2),
        
        # Advanced statistics
        "coefficient_of_variation": round(cv, 4),
        "skewness": round(skewness, 4),
        "kurtosis": round(kurtosis, 4),
        "percentile_25_ms": round(p25, 2),
        "percentile_75_ms": round(p75, 2),
        "percentile_95_ms": round(p95, 2),
        "interquartile_range_ms": round(iqr, 2),
        
        # Speed metrics
        "typing_speed_cpm": round(typing_speed_cpm, 2),
        "typing_speed_wpm": round(typing_speed_wpm, 2),
        "burst_speed_cpm": round(burst_speed_cpm, 2),
        "sustainable_speed_cpm": round(sustainable_speed_cpm, 2),
        
        # Rhythm analysis
        "rhythm_consistency_score": round(rhythm_consistency, 2),
        "flow_state_probability": round(flow_probability, 4),
        "micro_pause_frequency": round(micro_pause_frequency, 2),
        
        # Error analysis
        "correction_rate": round(correction_rate, 4),
        "immediate_correction_rate": round(immediate_correction_rate, 4),
        "delayed_correction_rate": round(delayed_correction_rate, 4),
        "error_burst_count": error_burst_count,
        "total_backspaces": backspace_count,
        
        # Pause analysis
        "pause_ratio": round(pause_ratio, 4),
        "long_pause_ratio": round(long_pause_ratio, 4),
        "very_long_pause_ratio": round(very_long_pause_ratio, 4),
        "mean_pause_duration_ms": round(mean_pause_duration, 2),
        "pause_pattern_regularity": round(pause_pattern_regularity, 4),
        "total_pauses": pause_count,
        "long_pauses": long_pause_count,
        "very_long_pauses": very_long_pause_count,
        
        # Cognitive indicators
        "cognitive_load_index": round(cognitive_load, 2),
        "fatigue_indicator": round(fatigue, 2),
        "attention_stability": round(attention, 2),
        
        # Derived scores
        "typing_proficiency_score": round(proficiency, 2),
        "consistency_rating": round(rhythm_consistency, 2),
        "efficiency_score": round(efficiency, 2),
        "accuracy_estimate": round(accuracy, 4),
        
        # Raw data summary
        "total_keystrokes": total_keystrokes,
        "total_time_ms": round(total_time_ms, 2),
        "burst_count": len(bursts),
        "average_burst_length": round(statistics.mean([len(b) for b in bursts]), 2) if bursts else 0
    }


def calculate_professional_cognitive_profile(
    stages: List[CodingStageData],
    typing_baseline: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate comprehensive cognitive profile from coding test stages.
    
    Analyzes problem-solving patterns, cognitive load progression,
    flow states, and adaptive capacity.
    """
    if not stages:
        return {"error": "No stage data provided"}
    
    # Extract baseline values
    baseline_std = typing_baseline.get("std_ikt_ms", 0) if typing_baseline else 0
    baseline_cv = typing_baseline.get("coefficient_of_variation", 0) if typing_baseline else 0
    baseline_correction = typing_baseline.get("correction_rate", 0) if typing_baseline else 0
    
    # Analyze each stage
    stage_analyses = []
    for stage in stages:
        keystrokes = stage.keystrokes
        
        # Calculate IKT values for this stage
        ikt_values = []
        for i in range(1, len(keystrokes)):
            ikt = keystrokes[i].timestamp - keystrokes[i-1].timestamp
            ikt_values.append(ikt)
        
        # Stage metrics
        stage_std = statistics.stdev(ikt_values) if len(ikt_values) > 1 else 0
        stage_mean = statistics.mean(ikt_values) if ikt_values else 0
        stage_cv = stage_std / stage_mean if stage_mean > 0 else 0
        
        # Correction analysis
        total_keystrokes = len(keystrokes)
        correction_rate = stage.backspace_count / total_keystrokes if total_keystrokes > 0 else 0
        
        # Speed metrics
        total_time_min = stage.total_time / 60000
        chars_typed = total_keystrokes - stage.backspace_count
        speed_cpm = chars_typed / total_time_min if total_time_min > 0 else 0
        
        # Cognitive load for this stage
        pause_ratio = stage.pause_events / total_keystrokes if total_keystrokes > 0 else 0
        cognitive_load = calculate_cognitive_load_index(
            ikt_values, pause_ratio, correction_rate, stage_cv
        )
        
        # Flow probability
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
    
    # Calculate progression metrics
    if len(stage_analyses) > 1:
        first = stage_analyses[0]
        last = stage_analyses[-1]
        
        std_shift = last["std_ikt"] - first["std_ikt"]
        correction_shift = last["correction_rate"] - first["correction_rate"]
        latency_shift = last["latency"] - first["latency"]
        speed_shift = last["speed_cpm"] - first["speed_cpm"]
    else:
        std_shift = correction_shift = latency_shift = speed_shift = 0
    
    # Frustration index calculation
    total_long_pauses = sum(s["long_pause_events"] for s in stage_analyses)
    total_rewrites = sum(s["rewrite_count"] for s in stage_analyses)
    total_time_sec = sum(s["total_time"] for s in stage_analyses) / 1000
    
    frustration_index = (total_long_pauses * 2 + total_rewrites * 3) / total_time_sec if total_time_sec > 0 else 0
    
    # Stress accumulation (increasing cognitive load across stages)
    if len(stage_analyses) > 1:
        load_values = [s["cognitive_load"] for s in stage_analyses]
        stress_accumulation = (load_values[-1] - load_values[0]) / max(1, load_values[0])
    else:
        stress_accumulation = 0
    
    # Cognitive overload probability
    avg_cognitive_load = statistics.mean([s["cognitive_load"] for s in stage_analyses])
    overload_probability = min(1, avg_cognitive_load / 80)  # 80+ load = likely overloaded
    
    # Load sensitivity
    current_std = stage_analyses[-1]["std_ikt"] if stage_analyses else 0
    load_sensitivity = (current_std - baseline_std) / baseline_std if baseline_std > 0 else 0
    
    # Adaptive capacity (ability to maintain performance under increasing load)
    if len(stage_analyses) > 1:
        speed_values = [s["speed_cpm"] for s in stage_analyses]
        speed_stability = 1 - (statistics.stdev(speed_values) / statistics.mean(speed_values)) if statistics.mean(speed_values) > 0 else 0
        adaptive_capacity = speed_stability * 100
    else:
        adaptive_capacity = 100
    
    # Recovery rate (improvement after difficult sections)
    if len(stage_analyses) >= 3:
        # Check if performance recovered after potential dip
        recovery_score = 0
        for i in range(2, len(stage_analyses)):
            if stage_analyses[i]["cognitive_load"] < stage_analyses[i-1]["cognitive_load"]:
                recovery_score += 1
        recovery_rate = recovery_score / (len(stage_analyses) - 2) if len(stage_analyses) > 2 else 1
    else:
        recovery_rate = 1
    
    # Flow state analysis
    flow_probabilities = [s["flow_probability"] for s in stage_analyses]
    avg_flow = statistics.mean(flow_probabilities) if flow_probabilities else 0
    
    # Detect flow entries and exits
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
    
    # Average flow duration (stages in flow)
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
    
    # Problem solving efficiency
    total_time = sum(s["total_time"] for s in stage_analyses)
    total_chars = sum(len(stages[i].keystrokes) - stages[i].backspace_count 
                      for i in range(len(stages)))
    problem_solving_efficiency = (total_chars / (total_time / 1000)) if total_time > 0 else 0
    
    # Iteration tendency (preference for revision)
    iteration_tendency = sum(s["rewrite_count"] for s in stage_analyses) / len(stage_analyses) if stage_analyses else 0
    
    # Exploration vs exploitation ratio
    # High correction + low pause = exploration (trying different approaches)
    # Low correction + steady pace = exploitation (confident execution)
    exploration_score = statistics.mean([s["correction_rate"] * (1 - s["pause_ratio"]) 
                                         for s in stage_analyses])
    exploitation_score = statistics.mean([(1 - s["correction_rate"]) * (1 - s["cv"]) 
                                          for s in stage_analyses])
    exploration_vs_exploitation = exploration_score / (exploration_score + exploitation_score) if (exploration_score + exploitation_score) > 0 else 0.5
    
    # Cognitive endurance
    endurance_score = adaptive_capacity * (1 - stress_accumulation) * (1 - overload_probability)
    endurance_score = max(0, min(100, endurance_score * 100))
    
    # Degradation rate
    if len(stage_analyses) > 1:
        performance_trend = []
        for i in range(1, len(stage_analyses)):
            perf_change = (stage_analyses[i-1]["speed_cpm"] - stage_analyses[i]["speed_cpm"]) / max(1, stage_analyses[i-1]["speed_cpm"])
            performance_trend.append(perf_change)
        degradation_rate = statistics.mean(performance_trend) if performance_trend else 0
    else:
        degradation_rate = 0
    
    # Optimal session length estimate (based on fatigue and degradation)
    avg_stage_time = statistics.mean([s["total_time"] for s in stage_analyses]) / 60000  # minutes
    optimal_session = avg_stage_time * (1 - degradation_rate) * (1 - overload_probability) * 3
    optimal_session = max(15, min(120, optimal_session))  # Clamp between 15-120 minutes
    
    # Overall cognitive scores
    cognitive_flexibility = (adaptive_capacity * 0.4 + 
                            (1 - abs(exploration_vs_exploitation - 0.5) * 2) * 30 +
                            recovery_rate * 30)
    
    focus_endurance = endurance_score
    
    problem_solving_score = (problem_solving_efficiency * 0.3 + 
                            (1 - iteration_tendency / 5) * 35 +
                            (1 - frustration_index) * 35)
    
    return {
        # Stage progression
        "std_shift_between_stages": round(std_shift, 2),
        "correction_shift": round(correction_shift, 4),
        "latency_shift_ms": round(latency_shift, 2),
        "speed_shift_cpm": round(speed_shift, 2),
        
        # Frustration and stress
        "frustration_index": round(frustration_index, 4),
        "stress_accumulation_rate": round(stress_accumulation, 4),
        "cognitive_overload_probability": round(overload_probability, 4),
        
        # Load sensitivity
        "load_sensitivity": round(load_sensitivity, 4),
        "adaptive_capacity": round(adaptive_capacity, 2),
        "recovery_rate": round(recovery_rate, 4),
        
        # Flow analysis
        "flow_state_duration_ratio": round(flow_duration_ratio, 4),
        "flow_entry_count": flow_entries,
        "flow_exit_count": flow_exits,
        "average_flow_duration_stages": round(avg_flow_duration, 2),
        "average_flow_probability": round(avg_flow, 4),
        
        # Problem solving
        "problem_solving_efficiency": round(problem_solving_efficiency, 4),
        "iteration_tendency": round(iteration_tendency, 4),
        "exploration_vs_exploitation_ratio": round(exploration_vs_exploitation, 4),
        
        # Endurance
        "endurance_score": round(endurance_score, 2),
        "degradation_rate": round(degradation_rate, 4),
        "optimal_session_length_minutes": round(optimal_session, 1),
        
        # Overall scores
        "cognitive_flexibility_score": round(cognitive_flexibility, 2),
        "focus_endurance_score": round(focus_endurance, 2),
        "problem_solving_score": round(max(0, min(100, problem_solving_score)), 2),
        
        # Stage details
        "completed_stages": len(stages),
        "stage_analyses": stage_analyses
    }


def calculate_experience_factor(years: int, daily_hours: int, 
                                 language: str, multitask: str) -> Dict[str, Any]:
    """
    Calculate comprehensive experience factor with multiple dimensions.
    """
    # Base experience (logarithmic scaling)
    base_factor = math.log(years + 1) / math.log(15)  # Normalized to ~1 at 15 years
    
    # Practice intensity factor
    intensity_factor = daily_hours / 8  # Normalized to 8 hours/day
    
    # Language complexity bonus
    language_complexity = {
        "C": 1.2,
        "C++": 1.15,
        "Java": 1.0,
        "Python": 0.9,
        "JavaScript": 0.95
    }
    lang_factor = language_complexity.get(language, 1.0)
    
    # Multitasking adjustment
    multitask_factors = {"Low": 1.1, "Medium": 1.0, "High": 0.85}
    multitask_factor = multitask_factors.get(multitask, 1.0)
    
    # Combined experience factor
    combined = base_factor * (1 + intensity_factor * 0.2) * lang_factor * multitask_factor
    
    # Determine expertise level
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
    """
    Calculate stability modifier with multiple factors.
    """
    # Base modifier from self-reported focus
    # Map 1-5 to 0.7-1.3
    base_modifier = 0.7 + (focus_stability - 1) * 0.15
    
    # If typing consistency available, incorporate it
    if typing_consistency is not None:
        # Blend self-reported with measured consistency
        measured_factor = typing_consistency / 100  # Normalize to 0-1
        blended = base_modifier * 0.6 + (0.7 + measured_factor * 0.6) * 0.4
    else:
        blended = base_modifier
    
    # Determine stability class
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
    """
    Generate professional classifications with confidence scores.
    """
    classifications = {}
    
    # Typing Stability Classification
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
    
    # Correction Intensity
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
    
    # Load Sensitivity
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
        
        # Frustration Index
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
        
        # Cognitive State Assessment
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


# ================== API ENDPOINTS ==================

@app.post("/profile")
async def save_profile(profile: ProfileData):
    """
    Save profile data and calculate comprehensive experience metrics.
    """
    # Calculate experience factor
    exp_result = calculate_experience_factor(
        profile.years_coding,
        profile.daily_hours,
        profile.primary_language,
        profile.multitask_level
    )
    
    # Calculate stability modifier
    stab_result = calculate_stability_modifier(profile.focus_stability)
    
    # Store profile
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
    """
    Process typing test data with professional-grade analysis.
    """
    # Calculate comprehensive metrics
    metrics = calculate_professional_typing_metrics(
        data.keystrokes,
        data.total_chars,
        data.expected_text,
        data.actual_text
    )
    
    # Store results
    session_data.typing_metrics = [k.dict() for k in data.keystrokes]
    session_data.baseline["keyboard"] = metrics
    
    # Update stability modifier with measured consistency
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
    """
    Process coding test data with professional cognitive analysis.
    """
    typing_baseline = session_data.baseline.get("keyboard", {})
    
    # Calculate cognitive profile
    cognitive_profile = calculate_professional_cognitive_profile(
        data.stages,
        typing_baseline
    )
    
    # Store results
    session_data.coding_metrics = [s.dict() for s in data.stages]
    session_data.baseline["cognitive_profile"] = cognitive_profile
    
    return {
        "status": "success",
        "cognitive_profile": cognitive_profile,
        "completed_stages": data.completed_stages
    }


@app.get("/summary")
async def get_summary():
    """
    Get comprehensive calibration summary with professional classifications.
    """
    profile = session_data.profile
    baseline = session_data.baseline
    
    keyboard = baseline.get("keyboard") or {}
    cognitive = baseline.get("cognitive_profile") or {}
    
    # Generate professional classifications
    classifications = classify_professional_metrics(keyboard, cognitive)
    
    # Calculate baseline confidence
    confidence_factors = []
    if keyboard:
        confidence_factors.append(keyboard.get("total_keystrokes", 0) / 500)  # More keystrokes = higher confidence
    if cognitive:
        confidence_factors.append(cognitive.get("completed_stages", 0) / 3)  # More stages = higher confidence
    if profile:
        confidence_factors.append(0.5)  # Profile completeness
    
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
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Baseline Calibration API - Professional Edition v2.0",
        "features": [
            "Advanced statistical analysis",
            "Cognitive load measurement",
            "Flow state detection",
            "Professional classifications"
        ]
    }


@app.post("/reset")
async def reset_session():
    """Reset session data for a new calibration."""
    session_data.reset()
    return {
        "status": "success",
        "message": "Session reset successfully"
    }


@app.get("/metrics/definitions")
async def get_metric_definitions():
    """
    Get definitions of all metrics for documentation.
    """
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
        }
    }
