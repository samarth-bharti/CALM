import { useState, useEffect, useRef } from 'react'

// API base URL
const API_BASE = 'http://localhost:8000'

// ================== WELCOME SCREEN ==================
function WelcomeScreen({ onNext }) {
  return (
    <div className="card">
      <div className="logo-container">
        <div className="logo-pulse"></div>
        <div className="logo-ring"></div>
      </div>
      <h1>Understand Your Natural Work Rhythm</h1>
      <p className="subtitle">
        Professional behavioral analytics to identify your unique typing patterns, 
        coding behavior, and cognitive responses.
      </p>
      <div className="features-grid">
        <div className="feature-item">
          <span className="feature-icon">⌨️</span>
          <span>Typing Analysis</span>
        </div>
        <div className="feature-item">
          <span className="feature-icon">🧠</span>
          <span>Cognitive Load</span>
        </div>
        <div className="feature-item">
          <span className="feature-icon">📊</span>
          <span>Flow Detection</span>
        </div>
        <div className="feature-item">
          <span className="feature-icon">🎯</span>
          <span>Baseline Vector</span>
        </div>
      </div>
      <div className="btn-container">
        <button className="btn btn-primary" onClick={onNext}>
          Start Calibration
        </button>
      </div>
    </div>
  )
}

// ================== PRIVACY SCREEN ==================
function PrivacyScreen({ onNext }) {
  const [agreed, setAgreed] = useState(false)

  return (
    <div className="card">
      <h2>Privacy & Data Notice</h2>
      <p className="subtitle">Your privacy is our priority</p>
      
      <div className="privacy-cards">
        <div className="privacy-card">
          <div className="privacy-icon">🔒</div>
          <h4>No Text Recording</h4>
          <p>We do NOT record what you type</p>
        </div>
        <div className="privacy-card">
          <div className="privacy-icon">⏱️</div>
          <h4>Timing Only</h4>
          <p>We only measure timing patterns</p>
        </div>
        <div className="privacy-card">
          <div className="privacy-icon">💻</div>
          <h4>Local Processing</h4>
          <p>No data leaves your device</p>
        </div>
        <div className="privacy-card">
          <div className="privacy-icon">🧪</div>
          <h4>Prototype</h4>
          <p>This is a calibration phase only</p>
        </div>
      </div>

      <label className="checkbox-container">
        <input 
          type="checkbox" 
          checked={agreed} 
          onChange={(e) => setAgreed(e.target.checked)}
        />
        <span>I understand and agree to proceed</span>
      </label>
      <div className="btn-container">
        <button className="btn" disabled={!agreed} onClick={onNext}>
          Continue to Profile
        </button>
      </div>
    </div>
  )
}

// ================== PROFILE SCREEN ==================
function ProfileScreen({ onNext, profile, setProfile }) {
  const [formData, setFormData] = useState({
    yearsCoding: profile.yearsCoding || 3,
    dailyHours: profile.dailyHours || 6,
    primaryLanguage: profile.primaryLanguage || 'Python',
    focusStability: profile.focusStability || 3,
    multitaskLevel: profile.multitaskLevel || 'Medium',
    typingFrequency: profile.typingFrequency || 'medium',
    errorCorrectionStyle: profile.errorCorrectionStyle || 'immediate',
    preferredComplexity: profile.preferredComplexity || 3
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/profile`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          years_coding: formData.yearsCoding,
          daily_hours: formData.dailyHours,
          primary_language: formData.primaryLanguage,
          focus_stability: formData.focusStability,
          multitask_level: formData.multitaskLevel,
          typing_frequency: formData.typingFrequency,
          error_correction_style: formData.errorCorrectionStyle,
          preferred_complexity: formData.preferredComplexity
        })
      })
      const data = await response.json()
      if (data.status === 'success') {
        setProfile(formData)
        onNext()
      }
    } catch (error) {
      console.error('Error saving profile:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Professional Profile</h2>
      <p className="subtitle">Help us calibrate to your experience level</p>

      <div className="form-section">
        <h3 className="form-section-title">Experience</h3>
        
        <div className="form-group">
          <label>Years of Coding Experience</label>
          <select 
            value={formData.yearsCoding}
            onChange={(e) => setFormData({...formData, yearsCoding: parseInt(e.target.value)})}
          >
            <option value={0}>Less than 1 year</option>
            <option value={1}>1-2 years</option>
            <option value={3}>3-4 years</option>
            <option value={5}>5-7 years</option>
            <option value={8}>8-10 years</option>
            <option value={12}>12-15 years</option>
            <option value={16}>15+ years</option>
          </select>
        </div>

        <div className="form-group">
          <label>Daily Coding Hours</label>
          <select 
            value={formData.dailyHours}
            onChange={(e) => setFormData({...formData, dailyHours: parseInt(e.target.value)})}
          >
            <option value={1}>1-2 hours</option>
            <option value={3}>3-4 hours</option>
            <option value={5}>5-6 hours</option>
            <option value={7}>7-8 hours</option>
            <option value={9}>9-10 hours</option>
            <option value={11}>10+ hours</option>
          </select>
        </div>

        <div className="form-group">
          <label>Primary Programming Language</label>
          <select 
            value={formData.primaryLanguage}
            onChange={(e) => setFormData({...formData, primaryLanguage: e.target.value})}
          >
            <option value="C">C</option>
            <option value="C++">C++</option>
            <option value="Python">Python</option>
            <option value="Java">Java</option>
            <option value="JavaScript">JavaScript</option>
          </select>
        </div>
      </div>

      <div className="form-section">
        <h3 className="form-section-title">Work Style</h3>
        
        <div className="form-group">
          <label>Focus Stability: <span className="slider-value">{formData.focusStability}</span></label>
          <div className="slider-container">
            <span>Distractible</span>
            <input 
              type="range" 
              min="1" 
              max="5" 
              value={formData.focusStability}
              onChange={(e) => setFormData({...formData, focusStability: parseInt(e.target.value)})}
            />
            <span>Highly Focused</span>
          </div>
        </div>

        <div className="form-group">
          <label>Multitasking Tendency</label>
          <div className="radio-group">
            {['Low', 'Medium', 'High'].map((level) => (
              <div 
                key={level}
                className={`radio-option ${formData.multitaskLevel === level ? 'selected' : ''}`}
                onClick={() => setFormData({...formData, multitaskLevel: level})}
              >
                {level}
              </div>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Typing Frequency</label>
          <div className="radio-group">
            {['low', 'medium', 'high'].map((level) => (
              <div 
                key={level}
                className={`radio-option ${formData.typingFrequency === level ? 'selected' : ''}`}
                onClick={() => setFormData({...formData, typingFrequency: level})}
              >
                {level.charAt(0).toUpperCase() + level.slice(1)}
              </div>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Error Correction Style</label>
          <div className="radio-group">
            {[
              { value: 'immediate', label: 'Immediate' },
              { value: 'batch', label: 'Batch' },
              { value: 'minimal', label: 'Minimal' }
            ].map((option) => (
              <div 
                key={option.value}
                className={`radio-option ${formData.errorCorrectionStyle === option.value ? 'selected' : ''}`}
                onClick={() => setFormData({...formData, errorCorrectionStyle: option.value})}
              >
                {option.label}
              </div>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Preferred Task Complexity: <span className="slider-value">{formData.preferredComplexity}</span></label>
          <div className="slider-container">
            <span>Simple</span>
            <input 
              type="range" 
              min="1" 
              max="5" 
              value={formData.preferredComplexity}
              onChange={(e) => setFormData({...formData, preferredComplexity: parseInt(e.target.value)})}
            />
            <span>Complex</span>
          </div>
        </div>
      </div>

      <div className="btn-container">
        <button className="btn" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Analyzing...' : 'Continue to Typing Test'}
        </button>
      </div>
    </div>
  )
}

// ================== TYPING TEST SCREEN ==================
const TYPING_TEXT = `The quick brown fox jumps over the lazy dog. Programming is both an art and a science, requiring creativity and logical thinking. Every developer has a unique coding style that reflects their thought process. By understanding your natural rhythm, you can optimize your workflow and improve productivity. This calibration measures your typing patterns, including speed, consistency, and correction behavior. Remember, there is no right or wrong way to type - we are simply capturing your natural behavior. Take your time and type naturally as you would in your daily work. The analysis will provide insights into your cognitive patterns.`

function TypingTestScreen({ onNext, setTypingBaseline }) {
  const [userInput, setUserInput] = useState('')
  const [started, setStarted] = useState(false)
  const [completed, setCompleted] = useState(false)
  const [keystrokes, setKeystrokes] = useState([])
  const [startTime, setStartTime] = useState(null)
  const [metrics, setMetrics] = useState(null)
  const textareaRef = useRef(null)

  const handleKeyDown = (e) => {
    if (!started) {
      setStarted(true)
      setStartTime(Date.now())
    }

    const keystroke = {
      timestamp: Date.now() - (startTime || Date.now()),
      key: e.key,
      is_backspace: e.key === 'Backspace' || e.key === 'Delete',
      is_enter: e.key === 'Enter',
      is_tab: e.key === 'Tab',
      is_space: e.key === ' ',
      is_punctuation: /[.,!?;:'"()-]/.test(e.key)
    }
    setKeystrokes(prev => [...prev, keystroke])
  }

  const handleChange = (e) => {
    const value = e.target.value
    setUserInput(value)

    if (value.length >= TYPING_TEXT.length && !completed) {
      setCompleted(true)
      handleSubmit(value)
    }
  }

  const handleSubmit = async (finalInput = userInput) => {
    try {
      const response = await fetch(`${API_BASE}/typing-metrics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          keystrokes: keystrokes,
          total_chars: finalInput.length,
          expected_text: TYPING_TEXT,
          actual_text: finalInput,
          test_duration_ms: keystrokes[keystrokes.length - 1]?.timestamp || 0
        })
      })
      const data = await response.json()
      if (data.status === 'success') {
        setMetrics(data.metrics)
        setTypingBaseline(data.metrics)
      }
    } catch (error) {
      console.error('Error saving typing metrics:', error)
    }
  }

  const progress = (userInput.length / TYPING_TEXT.length) * 100

  return (
    <div className="card">
      <h2>Controlled Typing Assessment</h2>
      <p className="subtitle">Type the text below naturally. Your patterns are being analyzed.</p>
      
      <div className="progress-container">
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${Math.min(progress, 100)}%` }}></div>
        </div>
        <span className="progress-text">{Math.round(progress)}% Complete</span>
      </div>

      <div className="text-display">
        {TYPING_TEXT.split('').map((char, index) => {
          let className = 'char'
          if (index < userInput.length) {
            className += userInput[index] === char ? ' correct' : ' incorrect'
          } else if (index === userInput.length) {
            className += ' current'
          }
          return <span key={index} className={className}>{char}</span>
        })}
      </div>

      <textarea
        ref={textareaRef}
        className="typing-area"
        value={userInput}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder="Start typing here..."
        disabled={completed}
        rows={4}
        autoFocus
      />

      {completed && metrics && (
        <div className="metrics-preview">
          <h3>Quick Analysis</h3>
          <div className="quick-stats">
            <div className="quick-stat">
              <span className="stat-value">{metrics.typing_speed_wpm}</span>
              <span className="stat-label">WPM</span>
            </div>
            <div className="quick-stat">
              <span className="stat-value">{metrics.rhythm_consistency_score}%</span>
              <span className="stat-label">Consistency</span>
            </div>
            <div className="quick-stat">
              <span className="stat-value">{(metrics.accuracy_estimate * 100).toFixed(1)}%</span>
              <span className="stat-label">Accuracy</span>
            </div>
            <div className="quick-stat">
              <span className="stat-value">{metrics.typing_proficiency_score}</span>
              <span className="stat-label">Proficiency</span>
            </div>
          </div>
          <div className="btn-container">
            <button className="btn" onClick={onNext}>
              Continue to Coding Test
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

// ================== CODING TEST SCREEN ==================
const CODING_TASKS = [
  {
    stage: 1,
    title: "Stage 1: Hello World",
    description: "Write a program that prints 'Hello World' in your selected language.",
    difficulty: 1
  },
  {
    stage: 2,
    title: "Stage 2: String Reverse",
    description: "Write a function to reverse a string.",
    difficulty: 2
  },
  {
    stage: 3,
    title: "Stage 3: Palindrome Check",
    description: "Write a function to check if a string is a palindrome.",
    difficulty: 3
  }
]

function CodingTestScreen({ onNext, profile, setCodingBaseline }) {
  const [currentStage, setCurrentStage] = useState(0)
  const [stagesData, setStagesData] = useState([])
  const [userInput, setUserInput] = useState('')
  const [started, setStarted] = useState(false)
  const [keystrokes, setKeystrokes] = useState([])
  const [startTime, setStartTime] = useState(null)
  const [firstKeystrokeTime, setFirstKeystrokeTime] = useState(null)
  const [backspaceCount, setBackspaceCount] = useState(0)
  const [pauseCount, setPauseCount] = useState(0)
  const [longPauseCount, setLongPauseCount] = useState(0)
  const [rewriteCount, setRewriteCount] = useState(0)
  const lastKeystrokeTime = useRef(null)
  const consecutiveBackspaces = useRef(0)

  const task = CODING_TASKS[currentStage]

  const handleKeyDown = (e) => {
    const now = Date.now()
    
    if (!started) {
      setStarted(true)
      setStartTime(now)
      setFirstKeystrokeTime(now)
      lastKeystrokeTime.current = now
    }

    if (lastKeystrokeTime.current) {
      const timeSinceLast = now - lastKeystrokeTime.current
      if (timeSinceLast > 800) {
        setPauseCount(prev => prev + 1)
      }
      if (timeSinceLast > 1500) {
        setLongPauseCount(prev => prev + 1)
      }
    }

    const isBackspace = e.key === 'Backspace' || e.key === 'Delete'
    
    if (isBackspace) {
      setBackspaceCount(prev => prev + 1)
      consecutiveBackspaces.current += 1
      
      if (consecutiveBackspaces.current >= 5) {
        setRewriteCount(prev => prev + 1)
        consecutiveBackspaces.current = 0
      }
    } else {
      consecutiveBackspaces.current = 0
    }

    const keystroke = {
      timestamp: now - startTime,
      key: e.key,
      is_backspace: isBackspace,
      is_enter: e.key === 'Enter',
      is_tab: e.key === 'Tab',
      is_space: e.key === ' ',
      is_punctuation: /[.,!?;:'"()-{}[\]]/.test(e.key)
    }
    setKeystrokes(prev => [...prev, keystroke])
    lastKeystrokeTime.current = now
  }

  const handleStageComplete = async () => {
    const stageData = {
      stage: currentStage + 1,
      keystrokes: keystrokes,
      time_to_first_keystroke: firstKeystrokeTime ? firstKeystrokeTime - startTime : 0,
      total_time: Date.now() - startTime,
      backspace_count: backspaceCount,
      pause_events: pauseCount,
      long_pause_events: longPauseCount,
      rewrite_count: rewriteCount,
      code_lines: userInput.split('\n').length,
      syntax_errors: 0
    }

    const newStagesData = [...stagesData, stageData]
    setStagesData(newStagesData)

    const correctionRate = backspaceCount / keystrokes.length
    const pauseRate = pauseCount / keystrokes.length
    
    if (correctionRate < 0.15 && pauseRate < 0.1 && currentStage < CODING_TASKS.length - 1) {
      setCurrentStage(prev => prev + 1)
      setUserInput('')
      setStarted(false)
      setKeystrokes([])
      setStartTime(null)
      setFirstKeystrokeTime(null)
      setBackspaceCount(0)
      setPauseCount(0)
      setLongPauseCount(0)
      setRewriteCount(0)
      consecutiveBackspaces.current = 0
    } else {
      try {
        const response = await fetch(`${API_BASE}/coding-metrics`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            stages: newStagesData,
            completed_stages: newStagesData.length,
            language: profile?.primaryLanguage || 'Python'
          })
        })
        const data = await response.json()
        if (data.status === 'success') {
          setCodingBaseline(data.cognitive_profile)
        }
      } catch (error) {
        console.error('Error saving coding metrics:', error)
      }
      onNext()
    }
  }

  return (
    <div className="card">
      <h2>Adaptive Coding Assessment</h2>
      <p className="subtitle">Multi-stage cognitive pattern analysis</p>
      
      <div className="stage-indicator">
        {CODING_TASKS.map((t, index) => (
          <div 
            key={index} 
            className={`stage-dot ${index < currentStage ? 'completed' : ''} ${index === currentStage ? 'active' : ''}`}
            title={t.title}
          ></div>
        ))}
      </div>

      <div className="code-task">
        <div className="task-header">
          <h3>{task.title}</h3>
          <span className="difficulty-badge" data-difficulty={task.difficulty}>
            Difficulty: {'★'.repeat(task.difficulty)}{'☆'.repeat(3 - task.difficulty)}
          </span>
        </div>
        <p className="task-description">{task.description}</p>
        <div className="task-meta">
          <span>Language: {profile?.primaryLanguage || 'Python'}</span>
          <span>Stage {currentStage + 1} of {CODING_TASKS.length}</span>
        </div>
      </div>

      <textarea
        className="typing-area code-area"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={`// Write your ${profile?.primaryLanguage || 'Python'} code here...`}
        rows={10}
        style={{ fontFamily: "'Consolas', 'Monaco', 'Fira Code', monospace" }}
      />

      <div className="stage-stats">
        <div className="stage-stat">
          <span className="stat-icon">⏱️</span>
          <span>{keystrokes.length} keystrokes</span>
        </div>
        <div className="stage-stat">
          <span className="stat-icon">⌫</span>
          <span>{backspaceCount} corrections</span>
        </div>
        <div className="stage-stat">
          <span className="stat-icon">⏸️</span>
          <span>{pauseCount} pauses</span>
        </div>
      </div>

      <div className="btn-container">
        <button className="btn" onClick={handleStageComplete}>
          {currentStage < CODING_TASKS.length - 1 ? 'Next Stage' : 'Complete Assessment'}
        </button>
      </div>
    </div>
  )
}

// ================== COGNITIVE TASK SCREEN ==================
function CognitiveTaskScreen({ onNext, setCogBaseline }) {
  const [userInput, setUserInput] = useState('')
  const [started, setStarted] = useState(false)
  const [keystrokes, setKeystrokes] = useState([])
  const [startTime, setStartTime] = useState(null)

  const handleKeyDown = (e) => {
    if (!started) {
      setStarted(true)
      setStartTime(Date.now())
    }

    const keystroke = {
      timestamp: Date.now() - startTime,
      key: e.key,
      is_backspace: e.key === 'Backspace' || e.key === 'Delete',
      is_enter: e.key === 'Enter',
      is_tab: e.key === 'Tab',
      is_space: e.key === ' ',
      is_punctuation: false
    }
    setKeystrokes(prev => [...prev, keystroke])
  }

  const handleSubmit = async () => {
    try {
      const response = await fetch(`${API_BASE}/coding-metrics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          stages: [{
            stage: 1,
            keystrokes: keystrokes,
            time_to_first_keystroke: keystrokes[0]?.timestamp || 0,
            total_time: Date.now() - startTime,
            backspace_count: keystrokes.filter(k => k.is_backspace).length,
            pause_events: 0,
            long_pause_events: 0,
            rewrite_count: 0,
            code_lines: userInput.split('\n').length,
            syntax_errors: 0
          }],
          completed_stages: 1
        })
      })
      const data = await response.json()
      if (data.status === 'success') {
        setCogBaseline(data.cognitive_profile)
      }
    } catch (error) {
      console.error('Error saving cognitive metrics:', error)
    }
    onNext()
  }

  return (
    <div className="card">
      <h2>Cognitive Variation Task</h2>
      <p className="subtitle">Problem-solving pattern analysis</p>

      <div className="code-task">
        <div className="task-header">
          <h3>Find the Maximum Element</h3>
          <span className="difficulty-badge" data-difficulty={2}>
            Difficulty: ★★☆
          </span>
        </div>
        <p className="task-description">
          Given an array [4, 2, 7, 1], write code to find and return the maximum element.
        </p>
        <div className="task-hint">
          <strong>Hint:</strong> Consider edge cases and efficiency
        </div>
      </div>

      <textarea
        className="typing-area code-area"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="// Write your solution here..."
        rows={8}
        style={{ fontFamily: "'Consolas', 'Monaco', 'Fira Code', monospace" }}
      />

      <div className="btn-container">
        <button className="btn" onClick={handleSubmit}>
          Generate Baseline Report
        </button>
      </div>
    </div>
  )
}

// ================== SUMMARY SCREEN ==================
function SummaryScreen({ onRestart }) {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await fetch(`${API_BASE}/summary`)
        const data = await response.json()
        setSummary(data)
      } catch (error) {
        console.error('Error fetching summary:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchSummary()
  }, [])

  const formatJSON = (obj) => {
    if (!obj) return '{}'
    return JSON.stringify(obj, null, 2)
  }

  if (loading) {
    return (
      <div className="card">
        <div className="loading">
          <div className="spinner"></div>
          <p>Generating comprehensive baseline analysis...</p>
        </div>
      </div>
    )
  }

  const classifications = summary?.classifications || {}
  const baseline = summary?.baseline_vector || {}

  return (
    <div className="card summary-card">
      <h2>Calibration Complete</h2>
      <p className="subtitle">Your professional behavioral baseline has been generated</p>

      <div className="confidence-badge">
        <span className="confidence-label">Baseline Confidence</span>
        <span className="confidence-value">
          {((summary?.calibration_metadata?.baseline_confidence || 0) * 100).toFixed(0)}%
        </span>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'typing' ? 'active' : ''}`}
          onClick={() => setActiveTab('typing')}
        >
          Typing Analysis
        </button>
        <button 
          className={`tab ${activeTab === 'cognitive' ? 'active' : ''}`}
          onClick={() => setActiveTab('cognitive')}
        >
          Cognitive Profile
        </button>
        <button 
          className={`tab ${activeTab === 'vector' ? 'active' : ''}`}
          onClick={() => setActiveTab('vector')}
        >
          Baseline Vector
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="tab-content">
          <div className="classifications-grid">
            <div className="classification-card">
              <div className="classification-header">
                <span className="classification-icon">⌨️</span>
                <h4>Typing Stability</h4>
              </div>
              <div className={`classification-value ${(classifications.typing_stability?.classification || '').toLowerCase().replace(' ', '-')}`}>
                {classifications.typing_stability?.classification || 'N/A'}
              </div>
              <div className="classification-confidence">
                Confidence: {((classifications.typing_stability?.confidence || 0) * 100).toFixed(0)}%
              </div>
              <div className="classification-details">
                <span>CV: {classifications.typing_stability?.cv_score?.toFixed(3) || 'N/A'}</span>
                <span>Rhythm: {classifications.typing_stability?.rhythm_score?.toFixed(1) || 'N/A'}</span>
              </div>
            </div>

            <div className="classification-card">
              <div className="classification-header">
                <span className="classification-icon">✏️</span>
                <h4>Correction Intensity</h4>
              </div>
              <div className={`classification-value ${(classifications.correction_intensity?.classification || '').toLowerCase().replace(' ', '-')}`}>
                {classifications.correction_intensity?.classification || 'N/A'}
              </div>
              <div className="classification-confidence">
                Confidence: {((classifications.correction_intensity?.confidence || 0) * 100).toFixed(0)}%
              </div>
              <div className="classification-details">
                <span>Rate: {((classifications.correction_intensity?.correction_rate || 0) * 100).toFixed(1)}%</span>
              </div>
            </div>

            <div className="classification-card">
              <div className="classification-header">
                <span className="classification-icon">🧠</span>
                <h4>Load Sensitivity</h4>
              </div>
              <div className={`classification-value ${(classifications.load_sensitivity?.classification || '').toLowerCase().replace(' ', '-')}`}>
                {classifications.load_sensitivity?.classification || 'N/A'}
              </div>
              <div className="classification-confidence">
                Confidence: {((classifications.load_sensitivity?.confidence || 0) * 100).toFixed(0)}%
              </div>
              <div className="classification-details">
                <span>Sensitivity: {classifications.load_sensitivity?.sensitivity_score?.toFixed(3) || 'N/A'}</span>
                <span>Adaptive: {classifications.load_sensitivity?.adaptive_capacity?.toFixed(1) || 'N/A'}</span>
              </div>
            </div>

            <div className="classification-card">
              <div className="classification-header">
                <span className="classification-icon">😤</span>
                <h4>Frustration Index</h4>
              </div>
              <div className={`classification-value ${(classifications.frustration_index?.classification || '').toLowerCase().replace(' ', '-')}`}>
                {classifications.frustration_index?.classification || 'N/A'}
              </div>
              <div className="classification-confidence">
                Confidence: {((classifications.frustration_index?.confidence || 0) * 100).toFixed(0)}%
              </div>
              <div className="classification-details">
                <span>Score: {classifications.frustration_index?.frustration_score?.toFixed(3) || 'N/A'}</span>
                <span>Overload: {((classifications.frustration_index?.overload_probability || 0) * 100).toFixed(0)}%</span>
              </div>
            </div>
          </div>

          <div className="cognitive-state-card">
            <h4>Current Cognitive State Assessment</h4>
            <div className={`state-badge state-${classifications.cognitive_state?.classification?.toLowerCase() || 'normal'}`}>
              {classifications.cognitive_state?.classification || 'Normal'}
            </div>
            <div className="state-metrics">
              <div className="state-metric">
                <span className="metric-label">Flow Probability</span>
                <span className="metric-value">{((classifications.cognitive_state?.flow_probability || 0) * 100).toFixed(0)}%</span>
              </div>
              <div className="state-metric">
                <span className="metric-label">Endurance Score</span>
                <span className="metric-value">{classifications.cognitive_state?.endurance_score?.toFixed(1) || 'N/A'}</span>
              </div>
            </div>
          </div>

          <div className="expertise-display">
            <h4>Expertise Level</h4>
            <div className="expertise-badge">
              {baseline.expertise_level || 'Intermediate'}
            </div>
            <div className="expertise-factors">
              <span>Experience Factor: {baseline.experience_factor?.toFixed(3) || 'N/A'}</span>
              <span>Stability Modifier: {baseline.stability_modifier?.toFixed(3) || 'N/A'}</span>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'typing' && baseline.keyboard && (
        <div className="tab-content">
          <div className="metrics-section">
            <h4>Speed Metrics</h4>
            <div className="metrics-grid">
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.typing_speed_wpm}</span>
                <span className="metric-label">WPM</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.typing_speed_cpm}</span>
                <span className="metric-label">CPM</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.burst_speed_cpm}</span>
                <span className="metric-label">Burst Speed</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.sustainable_speed_cpm}</span>
                <span className="metric-label">Sustainable</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Timing Statistics</h4>
            <div className="metrics-grid">
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.mean_ikt_ms}ms</span>
                <span className="metric-label">Mean IKT</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.std_ikt_ms}ms</span>
                <span className="metric-label">Std Dev</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.median_ikt_ms}ms</span>
                <span className="metric-label">Median</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.interquartile_range_ms}ms</span>
                <span className="metric-label">IQR</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Distribution Analysis</h4>
            <div className="metrics-grid">
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.coefficient_of_variation?.toFixed(4)}</span>
                <span className="metric-label">CV</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.skewness?.toFixed(4)}</span>
                <span className="metric-label">Skewness</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.kurtosis?.toFixed(4)}</span>
                <span className="metric-label">Kurtosis</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.percentile_95_ms}ms</span>
                <span className="metric-label">95th %ile</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Rhythm & Flow</h4>
            <div className="metrics-grid">
              <div className="metric-item highlight">
                <span className="metric-value">{baseline.keyboard.rhythm_consistency_score}</span>
                <span className="metric-label">Rhythm Score</span>
              </div>
              <div className="metric-item highlight">
                <span className="metric-value">{(baseline.keyboard.flow_state_probability * 100).toFixed(0)}%</span>
                <span className="metric-label">Flow Probability</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.micro_pause_frequency}</span>
                <span className="metric-label">Micro Pauses/100c</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.burst_count}</span>
                <span className="metric-label">Burst Count</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Error Analysis</h4>
            <div className="metrics-grid">
              <div className="metric-item">
                <span className="metric-value">{(baseline.keyboard.correction_rate * 100).toFixed(2)}%</span>
                <span className="metric-label">Correction Rate</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{(baseline.keyboard.immediate_correction_rate * 100).toFixed(2)}%</span>
                <span className="metric-label">Immediate</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.error_burst_count}</span>
                <span className="metric-label">Error Bursts</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.total_backspaces}</span>
                <span className="metric-label">Total Backspaces</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Cognitive Indicators</h4>
            <div className="metrics-grid">
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.cognitive_load_index}</span>
                <span className="metric-label">Cognitive Load</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.fatigue_indicator}</span>
                <span className="metric-label">Fatigue</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.attention_stability}</span>
                <span className="metric-label">Attention</span>
              </div>
              <div className="metric-item highlight">
                <span className="metric-value">{baseline.keyboard.typing_proficiency_score}</span>
                <span className="metric-label">Proficiency</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Pause Analysis</h4>
            <div className="metrics-grid">
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.total_pauses}</span>
                <span className="metric-label">Total Pauses</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.long_pauses}</span>
                <span className="metric-label">Long Pauses</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.very_long_pauses}</span>
                <span className="metric-label">Very Long</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.keyboard.pause_pattern_regularity?.toFixed(3)}</span>
                <span className="metric-label">Regularity</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'cognitive' && baseline.cognitive_profile && (
        <div className="tab-content">
          <div className="metrics-section">
            <h4>Stage Progression</h4>
            <div className="metrics-grid">
              <div className="metric-item">
                <span className="metric-value">{baseline.cognitive_profile.std_shift_between_stages}</span>
                <span className="metric-label">Std Shift</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{(baseline.cognitive_profile.correction_shift * 100).toFixed(2)}%</span>
                <span className="metric-label">Correction Shift</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.cognitive_profile.latency_shift_ms}ms</span>
                <span className="metric-label">Latency Shift</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.cognitive_profile.speed_shift_cpm}</span>
                <span className="metric-label">Speed Shift</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Stress & Frustration</h4>
            <div className="metrics-grid">
              <div className="metric-item highlight">
                <span className="metric-value">{baseline.cognitive_profile.frustration_index?.toFixed(4)}</span>
                <span className="metric-label">Frustration Index</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{(baseline.cognitive_profile.stress_accumulation_rate * 100).toFixed(1)}%</span>
                <span className="metric-label">Stress Rate</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{(baseline.cognitive_profile.cognitive_overload_probability * 100).toFixed(0)}%</span>
                <span className="metric-label">Overload Prob</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Adaptive Capacity</h4>
            <div className="metrics-grid">
              <div className="metric-item highlight">
                <span className="metric-value">{baseline.cognitive_profile.adaptive_capacity}</span>
                <span className="metric-label">Adaptive Capacity</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.cognitive_profile.load_sensitivity?.toFixed(4)}</span>
                <span className="metric-label">Load Sensitivity</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{(baseline.cognitive_profile.recovery_rate * 100).toFixed(0)}%</span>
                <span className="metric-label">Recovery Rate</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Flow State Analysis</h4>
            <div className="metrics-grid">
              <div className="metric-item highlight">
                <span className="metric-value">{(baseline.cognitive_profile.flow_state_duration_ratio * 100).toFixed(0)}%</span>
                <span className="metric-label">Flow Duration</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.cognitive_profile.flow_entry_count}</span>
                <span className="metric-label">Flow Entries</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.cognitive_profile.flow_exit_count}</span>
                <span className="metric-label">Flow Exits</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.cognitive_profile.average_flow_duration_stages}</span>
                <span className="metric-label">Avg Duration</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Problem Solving</h4>
            <div className="metrics-grid">
              <div className="metric-item">
                <span className="metric-value">{baseline.cognitive_profile.problem_solving_efficiency?.toFixed(4)}</span>
                <span className="metric-label">Efficiency</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{baseline.cognitive_profile.iteration_tendency?.toFixed(4)}</span>
                <span className="metric-label">Iteration</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{(baseline.cognitive_profile.exploration_vs_exploitation_ratio * 100).toFixed(0)}%</span>
                <span className="metric-label">Explore Ratio</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Endurance & Session</h4>
            <div className="metrics-grid">
              <div className="metric-item highlight">
                <span className="metric-value">{baseline.cognitive_profile.endurance_score}</span>
                <span className="metric-label">Endurance</span>
              </div>
              <div className="metric-item">
                <span className="metric-value">{(baseline.cognitive_profile.degradation_rate * 100).toFixed(1)}%</span>
                <span className="metric-label">Degradation</span>
              </div>
              <div className="metric-item highlight">
                <span className="metric-value">{baseline.cognitive_profile.optimal_session_length_minutes}min</span>
                <span className="metric-label">Optimal Session</span>
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h4>Overall Scores</h4>
            <div className="metrics-grid">
              <div className="metric-item highlight">
                <span className="metric-value">{baseline.cognitive_profile.cognitive_flexibility_score}</span>
                <span className="metric-label">Flexibility</span>
              </div>
              <div className="metric-item highlight">
                <span className="metric-value">{baseline.cognitive_profile.focus_endurance_score}</span>
                <span className="metric-label">Focus</span>
              </div>
              <div className="metric-item highlight">
                <span className="metric-value">{baseline.cognitive_profile.problem_solving_score}</span>
                <span className="metric-label">Problem Solving</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'vector' && (
        <div className="tab-content">
          <h4>Generated Baseline Vector</h4>
          <p className="vector-description">
            This vector represents your behavioral baseline and can be used for future comparisons.
          </p>
          <div className="json-display">
            <pre>{formatJSON(baseline)}</pre>
          </div>
        </div>
      )}

      <div className="btn-container">
        <button className="btn btn-secondary" onClick={onRestart}>
          Start New Calibration
        </button>
      </div>
    </div>
  )
}

// ================== MAIN APP ==================
function App() {
  const [screen, setScreen] = useState(0)
  const [profile, setProfile] = useState({})
  const [typingBaseline, setTypingBaseline] = useState(null)
  const [codingBaseline, setCodingBaseline] = useState(null)
  const [cogBaseline, setCogBaseline] = useState(null)

  const handleRestart = async () => {
    try {
      await fetch(`${API_BASE}/reset`, { method: 'POST' })
    } catch (error) {
      console.error('Error resetting session:', error)
    }
    setScreen(0)
    setProfile({})
    setTypingBaseline(null)
    setCodingBaseline(null)
    setCogBaseline(null)
  }

  const screens = [
    <WelcomeScreen key="welcome" onNext={() => setScreen(1)} />,
    <PrivacyScreen key="privacy" onNext={() => setScreen(2)} />,
    <ProfileScreen 
      key="profile" 
      onNext={() => setScreen(3)} 
      profile={profile} 
      setProfile={setProfile} 
    />,
    <TypingTestScreen 
      key="typing" 
      onNext={() => setScreen(4)} 
      setTypingBaseline={setTypingBaseline}
    />,
    <CodingTestScreen 
      key="coding" 
      onNext={() => setScreen(5)} 
      profile={profile}
      setCodingBaseline={setCodingBaseline}
    />,
    <CognitiveTaskScreen 
      key="cognitive" 
      onNext={() => setScreen(6)}
      setCogBaseline={setCogBaseline}
    />,
    <SummaryScreen key="summary" onRestart={handleRestart} />
  ]

  return (
    <div className="app">
      {screens[screen]}
    </div>
  )
}

export default App
