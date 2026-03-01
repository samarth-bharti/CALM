import { useState, useEffect, useRef } from 'react'

// API base URL
const API_BASE = 'http://localhost:8000'

// ================== ANTI-CHEAT UTILITIES ==================
const useAntiCheat = (sessionId, enabled = true) => {
  const [antiCheatEvents, setAntiCheatEvents] = useState([])

  const logEvent = async (eventType, details = {}) => {
    const event = {
      session_id: sessionId,
      event_type: eventType,
      timestamp: Date.now(),
      details: JSON.stringify(details)
    }
    
    setAntiCheatEvents(prev => [...prev, event])
    
    if (sessionId) {
      try {
        await fetch(`${API_BASE}/anti-cheat-event`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(event)
        })
      } catch (error) {
        console.error('Error logging anti-cheat event:', error)
      }
    }
  }

  useEffect(() => {
    if (!enabled) return

    // Copy-paste blocking
    const handleCopy = (e) => {
      e.preventDefault()
      logEvent('copy_attempt', { message: 'User attempted to copy' })
    }

    const handlePaste = (e) => {
      e.preventDefault()
      logEvent('paste_attempt', { message: 'User attempted to paste' })
    }

    const handleCut = (e) => {
      e.preventDefault()
      logEvent('cut_attempt', { message: 'User attempted to cut' })
    }

    // Tab switch detection
    const handleVisibilityChange = () => {
      if (document.hidden) {
        logEvent('tab_switch', { message: 'User switched away from tab' })
      }
    }

    // Window blur detection
    const handleBlur = () => {
      logEvent('window_blur', { message: 'Window lost focus' })
    }

    // Context menu blocking
    const handleContextMenu = (e) => {
      e.preventDefault()
      logEvent('context_menu_attempt', { message: 'User attempted right-click' })
    }

    // Keyboard shortcut blocking
    const handleKeyDown = (e) => {
      // Block Ctrl+C, Ctrl+V, Ctrl+X, F12, Ctrl+Shift+I
      if (
        (e.ctrlKey && ['c', 'v', 'x'].includes(e.key.toLowerCase())) ||
        e.key === 'F12' ||
        (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'i')
      ) {
        e.preventDefault()
        logEvent('blocked_shortcut', { key: e.key, ctrl: e.ctrlKey, shift: e.shiftKey })
      }
    }

    // Attach listeners
    document.addEventListener('copy', handleCopy)
    document.addEventListener('paste', handlePaste)
    document.addEventListener('cut', handleCut)
    document.addEventListener('visibilitychange', handleVisibilityChange)
    window.addEventListener('blur', handleBlur)
    document.addEventListener('contextmenu', handleContextMenu)
    document.addEventListener('keydown', handleKeyDown)

    return () => {
      document.removeEventListener('copy', handleCopy)
      document.removeEventListener('paste', handlePaste)
      document.removeEventListener('cut', handleCut)
      document.removeEventListener('visibilitychange', handleVisibilityChange)
      window.removeEventListener('blur', handleBlur)
      document.removeEventListener('contextmenu', handleContextMenu)
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [enabled, sessionId])

  return { antiCheatEvents, logEvent }
}

// ================== HARDWARE DETECTION UTILITIES ==================
const detectHardware = () => {
  const ua = navigator.userAgent
  let browserName = 'Unknown'
  let browserVersion = 'Unknown'
  let osName = 'Unknown'

  // Detect browser
  if (ua.indexOf('Firefox') > -1) {
    browserName = 'Firefox'
    browserVersion = ua.match(/Firefox\/(\d+\.\d+)/)?.[1] || 'Unknown'
  } else if (ua.indexOf('Chrome') > -1 && ua.indexOf('Edg') === -1) {
    browserName = 'Chrome'
    browserVersion = ua.match(/Chrome\/(\d+\.\d+)/)?.[1] || 'Unknown'
  } else if (ua.indexOf('Edg') > -1) {
    browserName = 'Edge'
    browserVersion = ua.match(/Edg\/(\d+\.\d+)/)?.[1] || 'Unknown'
  } else if (ua.indexOf('Safari') > -1) {
    browserName = 'Safari'
    browserVersion = ua.match(/Version\/(\d+\.\d+)/)?.[1] || 'Unknown'
  }

  // Detect OS
  if (ua.indexOf('Win') > -1) osName = 'Windows'
  else if (ua.indexOf('Mac') > -1) osName = 'macOS'
  else if (ua.indexOf('Linux') > -1) osName = 'Linux'
  else if (ua.indexOf('Android') > -1) osName = 'Android'
  else if (ua.indexOf('iOS') > -1) osName = 'iOS'

  return {
    screen_width: window.screen.width,
    screen_height: window.screen.height,
    screen_resolution: `${window.screen.width}x${window.screen.height}`,
    pixel_ratio: window.devicePixelRatio || 1,
    color_depth: window.screen.colorDepth,
    user_agent: ua,
    browser_name: browserName,
    browser_version: browserVersion,
    os_name: osName,
    os_version: osName,
    platform: navigator.platform,
    has_touch: 'ontouchstart' in window,
    has_mouse: matchMedia('(pointer:fine)').matches,
    has_keyboard: true,
    pointer_type: matchMedia('(pointer:fine)').matches ? (matchMedia('(pointer:coarse)').matches ? 'touch' : 'mouse') : 'touch',
    connection_type: navigator.connection?.effectiveType || 'unknown',
    device_memory_gb: navigator.deviceMemory || null,
    cpu_cores: navigator.hardwareConcurrency || null,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    language: navigator.language
  }
}

// ================== WELCOME SCREEN ==================
function WelcomeScreen({ onNext }) {
  return (
    <div className="card">
      <div className="logo-container">
        <div className="logo-pulse"></div>
        <div className="logo-ring"></div>
      </div>
      <h1>Employee Assessment System</h1>
      <p className="subtitle">
        Comprehensive professional behavioral analytics to understand your work patterns,
        skills, and cognitive responses.
      </p>
      <div className="features-grid">
        <div className="feature-item">
          <span className="feature-icon">👤</span>
          <span>Profile Assessment</span>
        </div>
        <div className="feature-item">
          <span className="feature-icon">⌨️</span>
          <span>Typing Analysis</span>
        </div>
        <div className="feature-item">
          <span className="feature-icon">🖱️</span>
          <span>Mouse Behavior</span>
        </div>
        <div className="feature-item">
          <span className="feature-icon">🎯</span>
          <span>Role-Specific Tests</span>
        </div>
      </div>
      <div className="btn-container">
        <button className="btn btn-primary" onClick={onNext}>
          Start Assessment
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
          <h4>Secure Data</h4>
          <p>All data is encrypted and stored securely</p>
        </div>
        <div className="privacy-card">
          <div className="privacy-icon">⏱️</div>
          <h4>Behavioral Patterns</h4>
          <p>We measure timing and behavior patterns</p>
        </div>
        <div className="privacy-card">
          <div className="privacy-icon">💻</div>
          <h4>Professional Use</h4>
          <p>Data used for assessment purposes only</p>
        </div>
        <div className="privacy-card">
          <div className="privacy-icon">🎯</div>
          <h4>One Attempt</h4>
          <p>Each employee can take the test once</p>
        </div>
      </div>

      <label className="checkbox-container">
        <input 
          type="checkbox" 
          checked={agreed} 
          onChange={(e) => setAgreed(e.target.checked)}
        />
        <span>I understand and agree to proceed with the assessment</span>
      </label>
      <div className="btn-container">
        <button className="btn" disabled={!agreed} onClick={onNext}>
          Continue to Employee Information
        </button>
      </div>
    </div>
  )
}

// ================== EMPLOYEE INFO SCREEN ==================
function EmployeeInfoScreen({ onNext, setSessionId, setEmployeeData }) {
  const [formData, setFormData] = useState({
    employee_id: '',
    full_name: '',
    email: '',
    age: '',
    gender: '',
    department: '',
    job_role: '',
    years_experience: '',
    employment_type: '',
    work_mode: ''
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const validate = () => {
    const newErrors = {}
    
    if (!formData.employee_id || formData.employee_id.length < 3) {
      newErrors.employee_id = 'Employee ID must be at least 3 characters'
    }
    if (!formData.full_name || formData.full_name.length < 2) {
      newErrors.full_name = 'Full name is required'
    }
    if (!formData.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Valid email is required'
    }
    if (!formData.age || formData.age < 18 || formData.age > 70) {
      newErrors.age = 'Age must be between 18 and 70'
    }
    if (!formData.gender) newErrors.gender = 'Gender is required'
    if (!formData.department) newErrors.department = 'Department is required'
    if (!formData.job_role) newErrors.job_role = 'Job role is required'
    if (!formData.years_experience || formData.years_experience < 0 || formData.years_experience > 50) {
      newErrors.years_experience = 'Years of experience must be between 0 and 50'
    }
    if (!formData.employment_type) newErrors.employment_type = 'Employment type is required'
    if (!formData.work_mode) newErrors.work_mode = 'Work mode is required'

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async () => {
    if (!validate()) return

    setLoading(true)
    setError('')

    try {
      // First, check if employee already has a session
      const checkResponse = await fetch(`${API_BASE}/start-session`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ employee_id: formData.employee_id })
      })
      const checkData = await checkResponse.json()

      if (checkData.status === 'error' && checkData.message.includes('already')) {
        setError('You have already completed an assessment. Each employee can only take the test once.')
        setLoading(false)
        return
      }

      // Save employee info
      const response = await fetch(`${API_BASE}/employee-info`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          age: parseInt(formData.age),
          years_experience: parseInt(formData.years_experience),
          session_id: checkData.session_id,
          timestamp: Date.now(),
          consent_given: true
        })
      })
      const data = await response.json()

      if (data.status === 'success') {
        setSessionId(data.session_id)
        setEmployeeData(formData)
        onNext()
      } else {
        setError(data.message || 'Failed to save employee information')
      }
    } catch (error) {
      console.error('Error saving employee info:', error)
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Employee Information</h2>
      <p className="subtitle">Please provide your details to begin the assessment</p>

      {error && <div className="error-message">{error}</div>}

      <div className="form-section">
        <div className="form-group">
          <label>Employee ID *</label>
          <input
            type="text"
            value={formData.employee_id}
            onChange={(e) => setFormData({...formData, employee_id: e.target.value})}
            placeholder="e.g., EMP001"
          />
          {errors.employee_id && <span className="error-text">{errors.employee_id}</span>}
        </div>

        <div className="form-group">
          <label>Full Name *</label>
          <input
            type="text"
            value={formData.full_name}
            onChange={(e) => setFormData({...formData, full_name: e.target.value})}
            placeholder="John Doe"
          />
          {errors.full_name && <span className="error-text">{errors.full_name}</span>}
        </div>

        <div className="form-group">
          <label>Email *</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            placeholder="john.doe@company.com"
          />
          {errors.email && <span className="error-text">{errors.email}</span>}
        </div>

        <div className="form-group">
          <label>Age *</label>
          <input
            type="number"
            value={formData.age}
            onChange={(e) => setFormData({...formData, age: e.target.value})}
            placeholder="25"
            min="18"
            max="70"
          />
          {errors.age && <span className="error-text">{errors.age}</span>}
        </div>

        <div className="form-group">
          <label>Gender *</label>
          <select
            value={formData.gender}
            onChange={(e) => setFormData({...formData, gender: e.target.value})}
          >
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
            <option value="Prefer not to say">Prefer not to say</option>
          </select>
          {errors.gender && <span className="error-text">{errors.gender}</span>}
        </div>

        <div className="form-group">
          <label>Department *</label>
          <select
            value={formData.department}
            onChange={(e) => setFormData({...formData, department: e.target.value})}
          >
            <option value="">Select Department</option>
            <option value="Engineering">Engineering</option>
            <option value="Product">Product</option>
            <option value="Design">Design</option>
            <option value="Data">Data</option>
            <option value="QA">QA</option>
            <option value="DevOps">DevOps</option>
            <option value="Other">Other</option>
          </select>
          {errors.department && <span className="error-text">{errors.department}</span>}
        </div>

        <div className="form-group">
          <label>Job Role/Position *</label>
          <input
            type="text"
            value={formData.job_role}
            onChange={(e) => setFormData({...formData, job_role: e.target.value})}
            placeholder="e.g., Senior Software Engineer"
          />
          {errors.job_role && <span className="error-text">{errors.job_role}</span>}
        </div>

        <div className="form-group">
          <label>Years of Experience *</label>
          <input
            type="number"
            value={formData.years_experience}
            onChange={(e) => setFormData({...formData, years_experience: e.target.value})}
            placeholder="5"
            min="0"
            max="50"
          />
          {errors.years_experience && <span className="error-text">{errors.years_experience}</span>}
        </div>

        <div className="form-group">
          <label>Employment Type *</label>
          <select
            value={formData.employment_type}
            onChange={(e) => setFormData({...formData, employment_type: e.target.value})}
          >
            <option value="">Select Type</option>
            <option value="Full-time">Full-time</option>
            <option value="Part-time">Part-time</option>
            <option value="Contract">Contract</option>
            <option value="Intern">Intern</option>
          </select>
          {errors.employment_type && <span className="error-text">{errors.employment_type}</span>}
        </div>

        <div className="form-group">
          <label>Work Mode *</label>
          <select
            value={formData.work_mode}
            onChange={(e) => setFormData({...formData, work_mode: e.target.value})}
          >
            <option value="">Select Mode</option>
            <option value="Remote">Remote</option>
            <option value="Hybrid">Hybrid</option>
            <option value="Office">Office</option>
          </select>
          {errors.work_mode && <span className="error-text">{errors.work_mode}</span>}
        </div>
      </div>

      <div className="btn-container">
        <button className="btn" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Saving...' : 'Continue to Classification'}
        </button>
      </div>
    </div>
  )
}

// ================== CLASSIFICATION SCREEN ==================
const CLASSIFICATION_QUESTIONS = [
  {
    id: 'q1',
    text: 'What is your primary work focus?',
    options: ['Building new features', 'Fixing bugs', 'Research & analysis', 'Customer support']
  },
  {
    id: 'q2',
    text: 'How often do you work under tight deadlines?',
    options: ['Constantly', 'Frequently', 'Occasionally', 'Rarely']
  },
  {
    id: 'q3',
    text: 'What type of work do you primarily do?',
    options: ['Customer-facing', 'Internal tools', 'Research projects', 'Maintenance & support']
  },
  {
    id: 'q4',
    text: 'What kind of code changes do you make most often?',
    options: ['New features', 'Bug fixes', 'Performance optimization', 'Code refactoring']
  },
  {
    id: 'q5',
    text: 'How much collaboration is involved in your work?',
    options: ['High (daily meetings)', 'Medium (weekly sync)', 'Low (mostly independent)', 'Minimal (solo work)']
  },
  {
    id: 'q6',
    text: 'Which tools do you use most frequently?',
    options: ['Frontend frameworks (React/Vue/Angular)', 'Backend frameworks (Node/Django/Flask)', 'Data tools (Jupyter/R/MATLAB)', 'DevOps tools (Git/Jenkins/Docker)']
  },
  {
    id: 'q7',
    text: 'How would you describe your problem-solving approach?',
    options: ['Creative & innovative', 'Analytical & systematic', 'Methodical & thorough', 'Reactive & adaptive']
  },
  {
    id: 'q8',
    text: 'What best describes your typical work pace?',
    options: ['Fast-paced & dynamic', 'Steady & consistent', 'Flexible & variable', 'Slow & deliberate']
  }
]

function ClassificationScreen({ onNext, sessionId, setClassifiedRole }) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState({})
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleAnswer = (answer) => {
    setAnswers({...answers, [CLASSIFICATION_QUESTIONS[currentQuestion].id]: answer})
    
    if (currentQuestion < CLASSIFICATION_QUESTIONS.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      submitClassification({...answers, [CLASSIFICATION_QUESTIONS[currentQuestion].id]: answer})
    }
  }

  const submitClassification = async (allAnswers) => {
    setLoading(true)
    try {
      // Transform answers object to array of ClassificationQuestion objects
      const answersArray = CLASSIFICATION_QUESTIONS.map((q, index) => {
        const answerText = allAnswers[q.id] || ''
        const answerIndex = q.options.indexOf(answerText)
        return {
          question_id: q.id,
          question_text: q.text,
          answer: answerText,
          answer_index: answerIndex >= 0 ? answerIndex : 0
        }
      })

      const response = await fetch(`${API_BASE}/classification`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          answers: answersArray
        })
      })
      const data = await response.json()
      
      if (data.status === 'success') {
        setResult(data.classification)
        setClassifiedRole(data.classification.primary_role)
      }
    } catch (error) {
      console.error('Error submitting classification:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <div className="loading">
          <div className="spinner"></div>
          <p>Analyzing your responses...</p>
        </div>
      </div>
    )
  }

  if (result) {
    return (
      <div className="card">
        <h2>Classification Complete</h2>
        <p className="subtitle">Based on your responses, we've identified your professional role</p>
        
        <div className="classification-result">
          <div className="role-badge">{result.primary_role}</div>
          <div className="confidence-display">
            Confidence: {(result.confidence_score * 100).toFixed(0)}%
          </div>
        </div>

        <div className="role-scores">
          <div className="score-item">
            <span>Production Developer</span>
            <div className="score-bar">
              <div className="score-fill" style={{width: `${result.production_score * 100}%`}}></div>
            </div>
            <span>{(result.production_score * 100).toFixed(0)}%</span>
          </div>
          <div className="score-item">
            <span>Deadline-Driven</span>
            <div className="score-bar">
              <div className="score-fill" style={{width: `${result.deadline_score * 100}%`}}></div>
            </div>
            <span>{(result.deadline_score * 100).toFixed(0)}%</span>
          </div>
          <div className="score-item">
            <span>Research-Oriented</span>
            <div className="score-bar">
              <div className="score-fill" style={{width: `${result.research_score * 100}%`}}></div>
            </div>
            <span>{(result.research_score * 100).toFixed(0)}%</span>
          </div>
          <div className="score-item">
            <span>Maintenance-Focused</span>
            <div className="score-bar">
              <div className="score-fill" style={{width: `${result.maintenance_score * 100}%`}}></div>
            </div>
            <span>{(result.maintenance_score * 100).toFixed(0)}%</span>
          </div>
        </div>

        <div className="btn-container">
          <button className="btn" onClick={onNext}>
            Continue to Hardware Check
          </button>
        </div>
      </div>
    )
  }

  const question = CLASSIFICATION_QUESTIONS[currentQuestion]
  const progress = ((currentQuestion + 1) / CLASSIFICATION_QUESTIONS.length) * 100

  return (
    <div className="card">
      <h2>Professional Classification</h2>
      <p className="subtitle">Answer these questions to help us understand your role</p>

      <div className="progress-container">
        <div className="progress-bar">
          <div className="progress-fill" style={{width: `${progress}%`}}></div>
        </div>
        <span className="progress-text">Question {currentQuestion + 1} of {CLASSIFICATION_QUESTIONS.length}</span>
      </div>

      <div className="question-card">
        <h3>{question.text}</h3>
        <div className="options-grid">
          {question.options.map((option, index) => (
            <button
              key={index}
              className="option-button"
              onClick={() => handleAnswer(option)}
            >
              {option}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

// ================== HARDWARE INFO SCREEN ==================
function HardwareInfoScreen({ onNext, sessionId }) {
  const [hardwareData, setHardwareData] = useState(detectHardware())
  const [manualData, setManualData] = useState({
    laptop_model: '',
    ram: '',
    cpu_type: ''
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/hardware-info`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          ...hardwareData,
          ...manualData,
          timestamp: Date.now()
        })
      })
      const data = await response.json()
      
      if (data.status === 'success') {
        onNext()
      }
    } catch (error) {
      console.error('Error saving hardware info:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Hardware & System Information</h2>
      <p className="subtitle">We've auto-detected your system details. Please verify and complete.</p>

      <div className="form-section">
        <h3 className="form-section-title">Auto-Detected Information</h3>
        
        <div className="info-grid">
          <div className="info-item">
            <span className="info-label">Operating System:</span>
            <span className="info-value">{hardwareData.os_name}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Browser:</span>
            <span className="info-value">{hardwareData.browser_name} {hardwareData.browser_version}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Screen Resolution:</span>
            <span className="info-value">{hardwareData.screen_resolution}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Connection Type:</span>
            <span className="info-value">{hardwareData.connection_type}</span>
          </div>
          {hardwareData.cpu_cores && (
            <div className="info-item">
              <span className="info-label">CPU Cores:</span>
              <span className="info-value">{hardwareData.cpu_cores}</span>
            </div>
          )}
          {hardwareData.device_memory_gb && (
            <div className="info-item">
              <span className="info-label">Device Memory:</span>
              <span className="info-value">{hardwareData.device_memory_gb} GB</span>
            </div>
          )}
        </div>
      </div>

      <div className="form-section">
        <h3 className="form-section-title">Manual Input Required</h3>
        
        <div className="form-group">
          <label>Laptop/Desktop Model</label>
          <input
            type="text"
            value={manualData.laptop_model}
            onChange={(e) => setManualData({...manualData, laptop_model: e.target.value})}
            placeholder="e.g., Dell XPS 15, MacBook Pro M2"
          />
        </div>

        <div className="form-group">
          <label>RAM</label>
          <select
            value={manualData.ram}
            onChange={(e) => setManualData({...manualData, ram: e.target.value})}
          >
            <option value="">Select RAM</option>
            <option value="4GB">4GB</option>
            <option value="8GB">8GB</option>
            <option value="16GB">16GB</option>
            <option value="32GB">32GB</option>
            <option value="64GB+">64GB+</option>
          </select>
        </div>

        <div className="form-group">
          <label>CPU Type</label>
          <select
            value={manualData.cpu_type}
            onChange={(e) => setManualData({...manualData, cpu_type: e.target.value})}
          >
            <option value="">Select CPU</option>
            <option value="Intel i3">Intel i3</option>
            <option value="Intel i5">Intel i5</option>
            <option value="Intel i7">Intel i7</option>
            <option value="Intel i9">Intel i9</option>
            <option value="AMD Ryzen 3">AMD Ryzen 3</option>
            <option value="AMD Ryzen 5">AMD Ryzen 5</option>
            <option value="AMD Ryzen 7">AMD Ryzen 7</option>
            <option value="AMD Ryzen 9">AMD Ryzen 9</option>
            <option value="Apple M1">Apple M1</option>
            <option value="Apple M2">Apple M2</option>
            <option value="Apple M3">Apple M3</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </div>

      <div className="btn-container">
        <button className="btn" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Saving...' : 'Continue to Typing Test'}
        </button>
      </div>
    </div>
  )
}

// ================== TYPING TEST SCREEN (ENHANCED) ==================
const TYPING_TEXT = `The quick brown fox jumps over the lazy dog. Programming is both an art and a science, requiring creativity and logical thinking. Every developer has a unique coding style that reflects their thought process. By understanding your natural rhythm, you can optimize your workflow and improve productivity. This assessment measures your typing patterns, including speed, consistency, and correction behavior.`

function TypingTestScreen({ onNext, sessionId }) {
  const [userInput, setUserInput] = useState('')
  const [started, setStarted] = useState(false)
  const [completed, setCompleted] = useState(false)
  const [keystrokes, setKeystrokes] = useState([])
  const [startTime, setStartTime] = useState(null)
  const [metrics, setMetrics] = useState(null)
  const textareaRef = useRef(null)
  const { logEvent } = useAntiCheat(sessionId, started && !completed)

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
    // Capture keystrokes at submission time to avoid race conditions
    const currentKeystrokes = [...keystrokes]
    
    // Ensure we have enough keystroke data
    if (currentKeystrokes.length < 2) {
      console.warn('Insufficient keystroke data for submission')
    }
    
    try {
      const response = await fetch(`${API_BASE}/typing-metrics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          keystrokes: currentKeystrokes,
          total_chars: finalInput.length,
          expected_text: TYPING_TEXT,
          actual_text: finalInput,
          test_duration_ms: currentKeystrokes.length > 0 
            ? currentKeystrokes[currentKeystrokes.length - 1]?.timestamp || 0 
            : 0
        })
      })
      const data = await response.json()
      if (data.status === 'success') {
        setMetrics(data.metrics)
        // Navigate to next screen after successful submission
        if (onNext) {
          onNext()
        }
      }
    } catch (error) {
      console.error('Error saving typing metrics:', error)
    }
  }

  const progress = (userInput.length / TYPING_TEXT.length) * 100

  return (
    <div className="card">
      <h2>Typing Assessment</h2>
      <p className="subtitle">Type the text below naturally. Copy-paste is disabled.</p>
      
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
          </div>
          <div className="btn-container">
            <button className="btn" onClick={onNext}>
              Continue to Mouse Tests
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

// ================== MOUSE ACCURACY SCREEN ==================
function MouseAccuracyScreen({ onNext, sessionId }) {
  const [targets, setTargets] = useState([])
  const [currentTarget, setCurrentTarget] = useState(0)
  const [clicks, setClicks] = useState([])
  const [started, setStarted] = useState(false)
  const [completed, setCompleted] = useState(false)
  const containerRef = useRef(null)

  useEffect(() => {
    if (started && targets.length === 0) {
      generateTargets()
    }
  }, [started])

  const generateTargets = () => {
    const newTargets = []
    for (let i = 0; i < 20; i++) {
      newTargets.push({
        x: Math.random() * 600 + 50,
        y: Math.random() * 400 + 50,
        timestamp: Date.now()
      })
    }
    setTargets(newTargets)
  }

  const handleClick = (e) => {
    if (!started || completed) return

    const rect = containerRef.current.getBoundingClientRect()
    const clickX = e.clientX - rect.left
    const clickY = e.clientY - rect.top
    const target = targets[currentTarget]

    const distance = Math.sqrt(
      Math.pow(clickX - target.x, 2) + Math.pow(clickY - target.y, 2)
    )

    const click = {
      timestamp: Date.now(),
      x: clickX,
      y: clickY,
      target_x: target.x,
      target_y: target.y,
      distance_from_target: distance,
      reaction_time_ms: Date.now() - target.timestamp
    }

    setClicks(prev => [...prev, click])

    if (currentTarget < targets.length - 1) {
      setCurrentTarget(currentTarget + 1)
      setTargets(prev => {
        const updated = [...prev]
        updated[currentTarget + 1].timestamp = Date.now()
        return updated
      })
    } else {
      setCompleted(true)
      submitResults([...clicks, click])
    }
  }

  const submitResults = async (allClicks) => {
    try {
      const response = await fetch(`${API_BASE}/mouse-metrics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          test_type: 'click_accuracy',
          clicks: allClicks,
          timestamp: Date.now()
        })
      })
      await response.json()
    } catch (error) {
      console.error('Error saving mouse metrics:', error)
    }
  }

  if (!started) {
    return (
      <div className="card">
        <h2>Mouse Accuracy Test</h2>
        <p className="subtitle">Click on 20 targets as accurately as possible</p>
        <div className="test-instructions">
          <p>• Click the center of each target</p>
          <p>• Be as accurate as you can</p>
          <p>• Speed matters, but accuracy is more important</p>
        </div>
        <div className="btn-container">
          <button className="btn" onClick={() => setStarted(true)}>
            Start Test
          </button>
        </div>
      </div>
    )
  }

  if (completed) {
    const avgDistance = clicks.reduce((sum, c) => sum + c.distance_from_target, 0) / clicks.length
    const avgReaction = clicks.reduce((sum, c) => sum + c.reaction_time_ms, 0) / clicks.length

    return (
      <div className="card">
        <h2>Test Complete!</h2>
        <div className="quick-stats">
          <div className="quick-stat">
            <span className="stat-value">{avgDistance.toFixed(1)}px</span>
            <span className="stat-label">Avg Distance</span>
          </div>
          <div className="quick-stat">
            <span className="stat-value">{avgReaction.toFixed(0)}ms</span>
            <span className="stat-label">Avg Reaction</span>
          </div>
        </div>
        <div className="btn-container">
          <button className="btn" onClick={onNext}>
            Continue to Reaction Test
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <h2>Mouse Accuracy Test</h2>
      <p className="subtitle">Target {currentTarget + 1} of {targets.length}</p>
      
      <div 
        ref={containerRef}
        className="mouse-test-area"
        onClick={handleClick}
      >
        {targets[currentTarget] && (
          <div 
            className="target-circle"
            style={{
              left: `${targets[currentTarget].x}px`,
              top: `${targets[currentTarget].y}px`
            }}
          >
            <div className="target-center"></div>
          </div>
        )}
      </div>
    </div>
  )
}

// ================== MOUSE REACTION SCREEN ==================
function MouseReactionScreen({ onNext, sessionId }) {
  const [state, setState] = useState('ready') // ready, waiting, active, complete
  const [reactions, setReactions] = useState([])
  const [targetAppearTime, setTargetAppearTime] = useState(null)
  const [currentTrial, setCurrentTrial] = useState(0)
  const totalTrials = 10

  const startTrial = () => {
    setState('waiting')
    const delay = Math.random() * 2000 + 1000 // 1-3 seconds
    setTimeout(() => {
      setState('active')
      setTargetAppearTime(Date.now())
    }, delay)
  }

  const handleClick = () => {
    if (state === 'active') {
      const reactionTime = Date.now() - targetAppearTime
      const newReactions = [...reactions, reactionTime]
      setReactions(newReactions)

      if (currentTrial < totalTrials - 1) {
        setCurrentTrial(currentTrial + 1)
        setState('ready')
        setTimeout(() => startTrial(), 500)
      } else {
        setState('complete')
        submitResults(newReactions)
      }
    } else if (state === 'waiting') {
      // Clicked too early
      setState('ready')
      alert('Too early! Wait for the green circle.')
    }
  }

  const submitResults = async (allReactions) => {
    try {
      const response = await fetch(`${API_BASE}/mouse-metrics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          test_type: 'reaction_time',
          reactions: allReactions,
          timestamp: Date.now()
        })
      })
      await response.json()
    } catch (error) {
      console.error('Error saving reaction metrics:', error)
    }
  }

  if (state === 'ready' && currentTrial === 0) {
    return (
      <div className="card">
        <h2>Reaction Time Test</h2>
        <p className="subtitle">Click as fast as possible when you see the green circle</p>
        <div className="test-instructions">
          <p>• Wait for the green circle to appear</p>
          <p>• Click it as quickly as you can</p>
          <p>• Complete 10 trials</p>
        </div>
        <div className="btn-container">
          <button className="btn" onClick={startTrial}>
            Start Test
          </button>
        </div>
      </div>
    )
  }

  if (state === 'complete') {
    const avgReaction = reactions.reduce((sum, r) => sum + r, 0) / reactions.length
    const fastest = Math.min(...reactions)

    return (
      <div className="card">
        <h2>Test Complete!</h2>
        <div className="quick-stats">
          <div className="quick-stat">
            <span className="stat-value">{avgReaction.toFixed(0)}ms</span>
            <span className="stat-label">Average</span>
          </div>
          <div className="quick-stat">
            <span className="stat-value">{fastest}ms</span>
            <span className="stat-label">Fastest</span>
          </div>
        </div>
        <div className="btn-container">
          <button className="btn" onClick={onNext}>
            Continue to Drag-Drop Test
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <h2>Reaction Time Test</h2>
      <p className="subtitle">Trial {currentTrial + 1} of {totalTrials}</p>
      
      <div className="reaction-test-area" onClick={handleClick}>
        {state === 'waiting' && (
          <div className="reaction-message">Wait...</div>
        )}
        {state === 'active' && (
          <div className="reaction-target">
            CLICK NOW!
          </div>
        )}
        {state === 'ready' && currentTrial > 0 && (
          <div className="reaction-message">Get ready...</div>
        )}
      </div>
    </div>
  )
}

// ================== MOUSE DRAG-DROP SCREEN ==================
function MouseDragDropScreen({ onNext, sessionId }) {
  const [items] = useState(['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'])
  const [completed, setCompleted] = useState([])
  const [dragData, setDragData] = useState([])
  const [currentDrag, setCurrentDrag] = useState(null)
  const [dragPath, setDragPath] = useState([])

  const handleDragStart = (e, item) => {
    setCurrentDrag(item)
    setDragPath([{ x: e.clientX, y: e.clientY, timestamp: Date.now() }])
  }

  const handleDrag = (e) => {
    if (currentDrag && e.clientX !== 0 && e.clientY !== 0) {
      setDragPath(prev => [...prev, { x: e.clientX, y: e.clientY, timestamp: Date.now() }])
    }
  }

  const handleDrop = (e, zone) => {
    e.preventDefault()
    if (currentDrag) {
      const newCompleted = [...completed, currentDrag]
      setCompleted(newCompleted)
      
      const drag = {
        item: currentDrag,
        zone: zone,
        path: dragPath,
        duration: Date.now() - dragPath[0].timestamp
      }
      const newDragData = [...dragData, drag]
      setDragData(newDragData)

      if (newCompleted.length === items.length) {
        submitResults(newDragData)
      }

      setCurrentDrag(null)
      setDragPath([])
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const submitResults = async (allDragData) => {
    try {
      const response = await fetch(`${API_BASE}/mouse-metrics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          test_type: 'drag_drop',
          drags: allDragData,
          timestamp: Date.now()
        })
      })
      await response.json()
    } catch (error) {
      console.error('Error saving drag-drop metrics:', error)
    }
  }

  if (completed.length === items.length) {
    return (
      <div className="card">
        <h2>Test Complete!</h2>
        <p className="subtitle">All items successfully dragged</p>
        <div className="btn-container">
          <button className="btn" onClick={onNext}>
            Continue to Role-Specific Tests
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <h2>Drag & Drop Test</h2>
      <p className="subtitle">Drag all items to the drop zone</p>
      
      <div className="drag-drop-container">
        <div className="draggable-items">
          {items.filter(item => !completed.includes(item)).map((item, index) => (
            <div
              key={index}
              className="draggable-item"
              draggable
              onDragStart={(e) => handleDragStart(e, item)}
              onDrag={handleDrag}
            >
              {item}
            </div>
          ))}
        </div>

        <div 
          className="drop-zone"
          onDrop={(e) => handleDrop(e, 'target')}
          onDragOver={handleDragOver}
        >
          <p>Drop items here</p>
          <p className="drop-count">{completed.length} / {items.length}</p>
        </div>
      </div>
    </div>
  )
}

// ================== ROLE-SPECIFIC TESTS SCREEN ==================
function RoleSpecificTestsScreen({ onNext, sessionId, classifiedRole }) {
  const [currentTest, setCurrentTest] = useState(0)
  const [testContent, setTestContent] = useState(null)
  const [userInput, setUserInput] = useState('')
  const [started, setStarted] = useState(false)
  const [keystrokes, setKeystrokes] = useState([])
  const [startTime, setStartTime] = useState(null)
  const [loading, setLoading] = useState(true)
  const { logEvent } = useAntiCheat(sessionId, started)
  const totalTests = 6

  useEffect(() => {
    fetchTestContent()
  }, [currentTest])

  const fetchTestContent = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/test-content/${classifiedRole}?test_number=${currentTest}`)
      const data = await response.json()
      
      // Handle both array response and single test response
      if (data.tests && Array.isArray(data.tests)) {
        // Backend returns array, get specific test by index
        const test = data.tests[currentTest % data.tests.length]
        setTestContent({
          id: test.test_id,
          name: test.test_name,
          prompt: test.prompt,
          code_snippet: test.initial_code || test.expected_code || ''
        })
      } else if (data.test) {
        // Backend returns single test object
        setTestContent(data.test)
      } else {
        console.error('Invalid test content response:', data)
      }
      setLoading(false)
    } catch (error) {
      console.error('Error fetching test content:', error)
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (!started) {
      setStarted(true)
      setStartTime(Date.now())
    }

    const keystroke = {
      timestamp: Date.now() - (startTime || Date.now()),
      key: e.key,
      is_backspace: e.key === 'Backspace' || e.key === 'Delete'
    }
    setKeystrokes(prev => [...prev, keystroke])
  }

  const handleSubmit = async () => {
    try {
      const response = await fetch(`${API_BASE}/role-specific-test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          test_id: testContent.id,
          test_category: classifiedRole,
          test_name: testContent.name,
          user_input: userInput,
          keystrokes: keystrokes,
          start_time: startTime,
          end_time: Date.now(),
          duration_ms: Date.now() - startTime
        })
      })
      await response.json()

      if (currentTest < totalTests - 1) {
        setCurrentTest(currentTest + 1)
        setUserInput('')
        setStarted(false)
        setKeystrokes([])
        setStartTime(null)
      } else {
        onNext()
      }
    } catch (error) {
      console.error('Error submitting test:', error)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading test...</p>
        </div>
      </div>
    )
  }

  const progress = ((currentTest + 1) / totalTests) * 100

  return (
    <div className="card">
      <h2>Role-Specific Tests: {classifiedRole}</h2>
      <p className="subtitle">Test {currentTest + 1} of {totalTests}</p>

      <div className="progress-container">
        <div className="progress-bar">
          <div className="progress-fill" style={{width: `${progress}%`}}></div>
        </div>
        <span className="progress-text">{Math.round(progress)}% Complete</span>
      </div>

      {testContent && (
        <div className="test-content">
          <h3>{testContent.name}</h3>
          <p className="test-description">{testContent.prompt}</p>
          
          {testContent.code_snippet && (
            <div className="code-snippet">
              <pre>{testContent.code_snippet}</pre>
            </div>
          )}

          <textarea
            className="typing-area code-area"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Write your solution here..."
            rows={10}
          />

          <div className="btn-container">
            <button className="btn" onClick={handleSubmit} disabled={!userInput.trim()}>
              {currentTest < totalTests - 1 ? 'Next Test' : 'Complete Tests'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

// ================== THANK YOU SCREEN ==================
function ThankYouScreen({ sessionId }) {
  return (
    <div className="card">
      <div className="logo-container">
        <div className="logo-pulse"></div>
        <div className="logo-ring"></div>
      </div>
      <h1>Thank You!</h1>
      <p className="subtitle">
        Your assessment has been completed successfully.
      </p>
      <div className="thank-you-content">
        <p>✓ All responses have been recorded</p>
        <p>✓ Your data has been securely saved</p>
        <p>✓ Session ID: {sessionId}</p>
      </div>
      <div className="thank-you-message">
        <p>
          Your assessment results will be reviewed by the appropriate team.
          You may now close this window.
        </p>
      </div>
    </div>
  )
}

// ================== MAIN APP ==================
function App() {
  const [screen, setScreen] = useState(0)
  const [sessionId, setSessionId] = useState(null)
  const [employeeData, setEmployeeData] = useState(null)
  const [classifiedRole, setClassifiedRole] = useState(null)

  const screens = [
    <WelcomeScreen key="welcome" onNext={() => setScreen(1)} />,
    <PrivacyScreen key="privacy" onNext={() => setScreen(2)} />,
    <EmployeeInfoScreen 
      key="employee-info" 
      onNext={() => setScreen(3)}
      setSessionId={setSessionId}
      setEmployeeData={setEmployeeData}
    />,
    <ClassificationScreen 
      key="classification" 
      onNext={() => setScreen(4)}
      sessionId={sessionId}
      setClassifiedRole={setClassifiedRole}
    />,
    <HardwareInfoScreen 
      key="hardware" 
      onNext={() => setScreen(5)}
      sessionId={sessionId}
    />,
    <TypingTestScreen 
      key="typing" 
      onNext={() => setScreen(6)}
      sessionId={sessionId}
    />,
    <MouseAccuracyScreen 
      key="mouse-accuracy" 
      onNext={() => setScreen(7)}
      sessionId={sessionId}
    />,
    <MouseReactionScreen 
      key="mouse-reaction" 
      onNext={() => setScreen(8)}
      sessionId={sessionId}
    />,
    <MouseDragDropScreen 
      key="mouse-drag" 
      onNext={() => setScreen(9)}
      sessionId={sessionId}
    />,
    <RoleSpecificTestsScreen 
      key="role-tests" 
      onNext={() => setScreen(10)}
      sessionId={sessionId}
      classifiedRole={classifiedRole}
    />,
    <ThankYouScreen 
      key="thank-you"
      sessionId={sessionId}
    />
  ]

  return (
    <div className="app">
      <div className="progress-indicator">
        <div className="progress-dots">
          {screens.map((_, index) => (
            <div 
              key={index}
              className={`progress-dot ${index === screen ? 'active' : ''} ${index < screen ? 'completed' : ''}`}
            />
          ))}
        </div>
      </div>
      {screens[screen]}
    </div>
  )
}

export default App
