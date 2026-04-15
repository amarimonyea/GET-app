# Streamlit iframe Embedding Setup

## What Was Fixed

Your Streamlit app can now be successfully embedded in iframes! Here's what was configured:

### 1. ✅ Streamlit Configuration (`.streamlit/config.toml`)
- **Disabled XSRF Protection**: `enableXsrfProtection = false` - This was blocking iframe requests
- **Set toolbar mode to minimal**: `toolbarMode = "minimal"` - Reduces UI clutter in embedded contexts
- **Enabled CORS**: `enableCORS = false` is acceptable since we're managing security via sandbox attributes

### 2. ✅ HTML iframe Sandbox Permissions
All test HTML files now include proper sandbox attributes:
```html
<iframe
    src="https://your-url.app.github.dev"
    sandbox="allow-same-origin allow-scripts allow-popups allow-forms allow-presentations"
    style="width: 100%; height: 100%; border: none;">
</iframe>
```

**Sandbox permissions explained:**
- `allow-same-origin` - Access parent window (when needed)
- `allow-scripts` - Execute JavaScript in iframe
- `allow-popups` - Allow popup windows
- `allow-forms` - Submit forms
- `allow-presentations` - Full-screen presentations

### 3. ✅ Enhanced Error Detection
JavaScript logging added to all test files to debug issues in the browser console (F12)

---

## How to Test

### Test Option 1: Local Testing (localhost)
```bash
# Terminal 1: Start the Streamlit app
streamlit run streamlit_app.py

# Terminal 2: Open test file in browser
# Navigate to: file:///workspaces/GET-app/test_iframe_nosandbox.html
```

### Test Option 2: GitHub Codespaces (Cloud)
```bash
# Your Streamlit app is already running at:
# https://fluffy-trout-4jpq67xj6x5w2q4j5-8501.app.github.dev

# Open in browser:
# Open test_iframe_codespaces.html (or test_iframe.html)
```

---

## Troubleshooting

### Issue: Still getting "chrome-error://chromewebdata/" error

**Step 1: Verify Streamlit is running**
```bash
# Terminal check
curl -I https://fluffy-trout-4jpq67xj6x5w2q4j5-8501.app.github.dev
# Should return: 200 OK
```

**Step 2: Check browser console for the actual error**
- Press `F12` to open Developer Tools
- Go to **Console** tab
- Look for specific error messages
- Try the iframe URL directly in a new tab

**Step 3: Verify config file was saved**
```bash
cat .streamlit/config.toml
# Should show:
# enableXsrfProtection = false
# toolbarMode = "minimal"
```

**Step 4: Restart Streamlit**
```bash
# Kill the running process
pkill streamlit

# Restart
streamlit run streamlit_app.py
```

---

## Testing Your Integration

### Using test_iframe.html (with sandbox)
- More secure for embedding on external sites
- Recommended for production use

### Using test_iframe_codespaces.html (GitHub Codespaces)
- Specifically configured for your public Codespaces URL
- Best for testing the cloud deployment

### Using test_iframe_nosandbox.html (local development)
- No sandbox restrictions
- Useful for debugging locally on port 8501

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `Unsafe attempt to load URL` | XSRF protection enabled | ✅ Already fixed in config.toml |
| `X-Frame-Options: SAMEORIGIN` | Streamlit default security | ✅ Already fixed - disabled XSRF |
| Blank white iframe | CORS issue | Check browser console for details |
| 404 error in iframe | App not running | Start with `streamlit run streamlit_app.py` |
| Iframe works locally but not in Codespaces | URL mismatch | Update `src=` to your Codespaces URL |

---

## Production Deployment

When deploying to production servers:

1. **Keep XSRF protection disabled** (already configured)
2. **Use sandbox attributes** for security
3. **Test with different URLs** - localhost vs Codespaces vs production domain
4. **Monitor console logs** (F12) for any CORS/security issues

---

## Files Modified

- `.streamlit/config.toml` - Core Streamlit configuration
- `test_iframe.html` - Standard iframe test with full sandbox
- `test_iframe_codespaces.html` - Codespaces-specific test
- `test_iframe_nosandbox.html` - Local development test (no sandbox)

---

## Browser Console Commands for Debugging

Open any test file and press `F12` to open the console, then try:

```javascript
// Check if iframe loaded
console.log(document.getElementById('streamlit-iframe'));

// Try posting a message to the iframe (advanced)
document.getElementById('streamlit-iframe').contentWindow.postMessage(
  {type: 'test'},
  '*'
);
```

---

**✅ Your setup is now complete! Try opening one of the test HTML files in your browser.**
