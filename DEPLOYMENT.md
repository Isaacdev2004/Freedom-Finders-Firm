# Deployment Guide

## Render Deployment

### Issue: lxml Compilation Error

If you encounter lxml compilation errors on Render, use one of these solutions:

### Solution 1: Use Alternative Requirements (Recommended)

Replace `requirements.txt` with `requirements_alternative.txt`:

```bash
# In Render dashboard, change build command to:
pip install -r requirements_alternative.txt
```

### Solution 2: Update requirements.txt

The current `requirements.txt` has been updated with:
- `lxml==4.9.1` (more stable version)
- `runtime.txt` specifies Python 3.11.7

### Solution 3: Manual Render Configuration

1. **Environment Variables**:
   ```
   PYTHON_VERSION=3.11.7
   ZAPIER_WEBHOOK_URL=https://webhook.site/your-unique-url
   ```

2. **Build Command**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Command**:
   ```bash
   gunicorn main:app
   ```

### Solution 4: Use render.yaml

The `render.yaml` file is configured for automatic deployment:

```yaml
services:
  - type: web
    name: google-business-scraper
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.7
      - key: ZAPIER_WEBHOOK_URL
        value: https://webhook.site/your-unique-url
        sync: false
```

## Alternative Deployment: Replit

1. **Create new Repl**
2. **Upload all files**
3. **Set environment variables**:
   - `ZAPIER_WEBHOOK_URL`
4. **Run**: `python main.py`

## Testing Deployment

After deployment, test with:

```bash
curl -X POST https://your-app-name.onrender.com/extract \
  -H "Content-Type: application/json" \
  -d '{"business_name": "Blue Bottle Coffee San Francisco"}'
```

## Troubleshooting

### If lxml still fails:
1. Use `requirements_alternative.txt`
2. The scraper already uses `html.parser` instead of `lxml`
3. All functionality will work without lxml

### If build fails:
1. Check Python version compatibility
2. Ensure all dependencies are in requirements.txt
3. Try the alternative requirements file

## Environment Variables

Set these in your deployment platform:

- `ZAPIER_WEBHOOK_URL`: Your Zapier webhook URL
- `PYTHON_VERSION`: 3.11.7 (for Render)

## Health Check

After deployment, visit:
- `https://your-app-name.onrender.com/health`
- Should return: `{"status": "healthy", "service": "Google Business Scraper", "version": "1.0.0"}` 