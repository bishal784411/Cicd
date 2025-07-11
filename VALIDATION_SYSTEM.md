# Comprehensive Validation System

This repository includes a comprehensive validation system that checks for:

## 🔍 What Gets Checked

### Network & Infrastructure
- ✅ Internet connectivity
- ✅ GitHub API accessibility
- ✅ Docker Hub connectivity
- ✅ NPM registry access (if using Node.js)

### GitHub & Git
- ✅ GitHub credentials validation
- ✅ Repository access permissions
- ✅ Git configuration
- ✅ Uncommitted changes detection

### Docker Environment
- ✅ Docker CLI availability
- ✅ Docker daemon status
- ✅ Container functionality test
- ✅ Docker Compose availability

### Code Quality
- ✅ HTML validation (structure, missing attributes)
- ✅ CSS validation (syntax, missing semicolons)
- ✅ JavaScript validation (syntax, console.log detection)
- ✅ AI-powered error analysis (if configured)

### Security
- ✅ Hardcoded secrets detection
- ✅ Unsafe JavaScript patterns
- ✅ Sensitive file detection

## 🚀 How to Use

### Local Development
```bash
# Run the enhanced monitor
python enhanced_monitor.py

# Run without git checks
python enhanced_monitor.py --no-git
```

### Pre-commit Hooks
The system automatically runs validation before each commit. If errors are found, the commit is blocked.

### GitHub Actions
Every push and pull request triggers comprehensive validation in the cloud.

## ⚙️ Configuration

### Environment Variables (.env)
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key
GITHUB_TOKEN=your_github_token_here
```

### GitHub Secrets
Add these secrets to your repository settings:
- `GEMINI_API_KEY`: For AI-powered error analysis
- `GEMINI_URL`: Gemini API endpoint

## 📁 Files Created

- `.github/workflows/pre-push-validation.yml`: GitHub Actions workflow
- `.git/hooks/pre-commit`: Local pre-commit hook
- `enhanced_monitor.py`: Enhanced monitoring script
- `.env.example`: Environment variables template
- `VALIDATION_SYSTEM.md`: This documentation

## 🔧 Customization

You can customize the validation rules by editing:
- `enhanced_monitor.py`: For local monitoring
- `.github/workflows/pre-push-validation.yml`: For GitHub Actions
- `.git/hooks/pre-commit`: For pre-commit hooks

## 🚨 Error Handling

When errors are detected:
1. **Local**: Errors are logged to `error_log.json`
2. **Pre-commit**: Commit is blocked until errors are fixed
3. **GitHub Actions**: Build fails and notifications are sent

## 🎯 Best Practices

1. **Fix errors immediately** when detected
2. **Review AI suggestions** for complex issues
3. **Keep environment variables secure**
4. **Test changes locally** before pushing
5. **Monitor validation reports** regularly

## 📞 Support

If you encounter issues:
1. Check the error logs
2. Verify environment variables
3. Test network connectivity
4. Review GitHub permissions
