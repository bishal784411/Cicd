# DevOps Monitoring Dashboard - Solution & Fix Agent

A comprehensive DevOps monitoring dashboard for automated solution detection and fix deployment. Built with React and FastAPI, this system provides real-time monitoring, AI-powered error analysis, and automated remediation capabilities.

## 🚀 Features

### Monitoring & Detection
- **Real-time System Health**: Live monitoring of system resources and application health
- **Multi-type Error Detection**: HTML, CSS, JavaScript, Security, Performance, and Configuration issues
- **AI-Powered Analysis**: Intelligent error analysis with actionable insights
- **Severity Classification**: Critical, High, Medium, and Low priority issue categorization

### Automation & Remediation  
- **Auto-Fix Capabilities**: One-click automated fixes for common issues
- **Fix Tracking**: Complete audit trail of applied fixes and their outcomes
- **System Metrics**: CPU, Memory, Disk usage, and Network latency monitoring
- **Agent Status**: Real-time monitoring of the solution agent status

### DevOps Dashboard
- **Enterprise UI**: Professional monitoring interface designed for DevOps teams
- **Real-time Updates**: 3-second polling for immediate issue detection
- **Connection Monitoring**: Visual connection status with automatic reconnection
- **Resource Prioritization**: Critical issues displayed first with clear visual hierarchy

## 🏗️ Architecture

### Frontend (React + TypeScript)
- Modern React with TypeScript and Tailwind CSS
- Real-time polling with connection status monitoring
- Expandable file cards with detailed error analysis
- System health overview with resource usage metrics
- Auto-fix trigger capabilities with status tracking

### Backend (FastAPI)
- RESTful API with comprehensive monitoring endpoints
- CORS enabled for seamless frontend integration
- Fix request handling and job tracking
- System metrics collection and reporting
- Health check endpoints with detailed status

## 📋 Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create your `error_log.json` file (or use the sample):
```bash
cp sample_error_log.json error_log.json
```

4. Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The dashboard will be available at `http://localhost:5173`

## 🔌 API Endpoints

### `GET /monitor/errors`
Returns comprehensive monitoring data including system health, file status, and metrics:
```json
{
  "last_updated": "2024-01-15T14:30:00.000Z",
  "total_files": 6,
  "files_with_errors": 4,
  "critical_issues": 2,
  "system_health": "degraded",
  "agent_status": "active",
  "files": [...],
  "metrics": {
    "cpu_usage": 45,
    "memory_usage": 67,
    "disk_usage": 23,
    "network_latency": 12,
    "active_monitors": 15,
    "fixes_applied_today": 8
  }
}
```

### `POST /monitor/fix`
Triggers automated fix for specific errors:
```json
{
  "file": "src/components/UserAuth.tsx",
  "error_index": 0
}
```

### `GET /monitor/metrics`
Returns real-time system metrics.

### `GET /health`
Enhanced health check with system status and monitoring overview.

## 📊 Error Log Format

The system expects `error_log.json` with enhanced DevOps monitoring format:
```json
{
  "last_updated": "2024-01-15T14:30:00.000Z",
  "errors": [
    {
      "timestamp": "2024-01-15T14:25:00.000Z",
      "file": "src/components/UserAuth.tsx",
      "error_type": "SECURITY",
      "line_number": 45,
      "message": "Potential XSS vulnerability: User input not properly sanitized",
      "ai_analysis": "Detailed AI analysis of the security issue...",
      "severity": "critical",
      "fix_suggestion": "Use React's built-in XSS protection...",
      "auto_fixable": true,
      "fix_applied": false
    }
  ]
}
```

## 🔧 Integration with MonitorAgent

To integrate with your existing Python MonitorAgent:

1. **Error Logging**: Ensure your MonitorAgent writes to `error_log.json` in the expected format
2. **Fix Integration**: Implement fix handlers that respond to POST requests to `/monitor/fix`
3. **Metrics Collection**: Add system metrics collection to your monitoring pipeline
4. **Status Reporting**: Update agent status based on monitoring activity

## 🎨 Customization

- **Polling Interval**: Modify `pollInterval` in `useMonitoring` hook (default: 3 seconds)
- **API Base URL**: Update `API_BASE_URL` in `src/hooks/useMonitoring.ts`
- **Error Log Path**: Change `ERROR_LOG_PATH` in `backend/main.py`
- **System Metrics**: Customize metrics collection in `generate_mock_system_metrics()`
- **UI Theme**: Adjust Tailwind CSS classes for custom branding

## 🚀 Production Deployment

1. Build the React frontend:
```bash
npm run build
```

2. Configure FastAPI for production with proper ASGI server
3. Set up reverse proxy (nginx) for static file serving
4. Configure SSL certificates and security headers
5. Set up monitoring and logging for the monitoring system itself

## 🛠️ Technologies Used

- **Frontend**: React 18, TypeScript, Tailwind CSS, Lucide React
- **Backend**: FastAPI, Python 3.8+, Pydantic, Uvicorn
- **Build Tools**: Vite, ESLint, PostCSS
- **Styling**: Tailwind CSS with custom DevOps theme
- **Icons**: Lucide React for consistent iconography

## 🔒 Security Considerations

- CORS properly configured for production domains
- Input validation on all API endpoints
- Error message sanitization to prevent information leakage
- Rate limiting recommended for production deployment
- SSL/TLS encryption for all communications

## 📈 Monitoring Features

- **System Health**: Overall system status with color-coded indicators
- **Resource Usage**: Real-time CPU, Memory, Disk, and Network monitoring
- **Error Trends**: Historical error tracking and pattern recognition
- **Fix Success Rate**: Tracking of automated fix success and failure rates
- **Uptime Monitoring**: Per-file uptime percentage tracking
- **Alert Thresholds**: Configurable thresholds for critical system metrics

This dashboard provides enterprise-grade monitoring capabilities specifically designed for DevOps teams managing complex application environments with automated remediation requirements.