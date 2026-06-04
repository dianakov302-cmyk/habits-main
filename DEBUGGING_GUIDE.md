# 🔧 AUTO-LOGIN DEBUGGING GUIDE

**Date:** June 4, 2026  
**Status:** Enhanced with console logging for troubleshooting

---

## What We Just Added

I've added **comprehensive console logging** to help you see exactly what's happening when you register:

### Console Messages to Look For

When you complete registration, you should see in the browser console (F12):

```
✓ App: Initializing registration page
API Request: POST http://localhost:8080/users/register
API Response: 200 from http://localhost:8080/users/register
✓ Registration successful!
✓ Token stored: eyJhbGciOiJIUzI1NiI...
✓ Email stored: yourname@example.com
→ Redirecting to test.html...

[page navigates to test.html]

✓ App: Initializing test page
✓ Quiz: Initializing...
✓ Quiz: Fully initialized. Rendering first question...
Quiz: Rendering question 1/5
```

---

## How to Test Now

### Step 1: Clear Browser Cache

This is important! The browser may be caching the old JavaScript.

**Chrome/Firefox/Edge:**
- Press: **Ctrl+Shift+Delete** (Windows) or **Cmd+Shift+Delete** (macOS)
- Select "All time" or "Everything"
- Check "Cookies and other site data" and "Cached images and files"
- Click "Delete data"

**Safari:**
- Menu → Preferences → Privacy
- Click "Manage Website Data"
- Select all → Remove

### Step 2: Open DevTools Console

- Press: **F12** (or right-click → Inspect)
- Go to **Console** tab
- You'll see logs from the JavaScript

### Step 3: Register

1. Go to: `http://localhost:3000/registration.html` or `http://127.0.0.1:3000/registration.html`
2. Fill in:
   - **Name:** Your name (e.g., "Alice Smith")
   - **Email:** A unique email (e.g., "alice123@example.com")
   - **Password:** At least 6 characters
   - **Confirm:** Same password
3. Click **"Create Account"**

### Step 4: Watch the Console

As you click "Create Account", watch the Console and you should see:

```
✓ App: Initializing registration page
API Request: POST http://localhost:8080/users/register
API Response: 200 from http://localhost:8080/users/register
✓ Registration successful!
✓ Token stored: eyJhbGciOiJIUzI1NiI...
✓ Email stored: yourname@example.com
→ Redirecting to test.html...
```

Then the page should redirect automatically to test.html and you should see:

```
✓ App: Initializing test page
✓ Quiz: Initializing...
✓ Quiz: Fully initialized. Rendering first question...
Quiz: Rendering question 1/5
```

---

## Troubleshooting By Error

### ❌ Error: "API Request: POST ... API Response: 400 or 500"

**What it means:** The backend received the request but rejected it.

**Solutions:**
1. Check the response error: Look in Console → Network tab → find the /users/register request → look at the Response
2. Common errors:
   - Email already registered → Use a different, unique email
   - Password too short → Use at least 6 characters
   - Invalid email format → Make sure email appears valid

### ❌ Error: "✗ Quiz: #quizContent element not found!"

**What it means:** The test.html page doesn't have the quiz container.

**Solution:** The test.html file might be corrupted or missing. Let's fix it:

```bash
curl -s http://127.0.0.1:3000/test.html | grep "quizContent"
# Should return: <div id="quizContent"></div>
```

If not found, the file needs to be restored.

### ❌ Error: Console shows nothing, no logs at all

**What it means:** The JavaScript isn't loading.

**Solutions:**
1. Try a **hard refresh**: Ctrl+Shift+R (Windows) or Cmd+Shift+R (macOS)
2. Clear browser cache (see Step 1 above)
3. Check if JavaScript errors are blocking the page: Look for ANY red errors in Console
4. Load the registration.html page directly and check the Network tab:
   - Does app.js load? (look for 200 status)
   - Does registration.js load? (look for 200 status)

### ❌ Registration succeeds but NO redirect to test.html

**What it means:** Page is staying on registration.html after clicking submit.

**Debugging:**
1. Check console for errors (red text)
2. Check if token is stored:
   - Open Console → Type: `localStorage.getItem('anaida_token')`
   - Should return a long JWT string, not null
3. If token is stored, the redirect code might have an error
4. Solutions:
   - Try clicking "Create Account" again
   - Do a hard refresh and try again
   - Check for JavaScript errors in the Console

### ❌ Page redirects to test.html but NO QUIZ appears

**What it means:** test.html loads but the quiz doesn't render.

**Debugging:**
1. Does console show: "✓ Quiz: Initializing..."?
   - If YES → Check if it shows "✓ Quiz: Fully initialized..."
   - If it stops, check for errors above it
2. Is the #quizContent div visible?
   - Right-click on page → Inspect → Search for "quizContent"
3. Check the Network tab:
   - Is test.js loading? (look for status 200)
   - Look for any RED errors (404, 500, etc.)

### ❌ Error: "API Response: 401 from http://localhost:8080/users/..."

**What it means:** Token is invalid or missing.

**Solution:** Token might have expired or not gotten stored. Try registering again with a fresh email.

---

## Network Tab Debugging

If console logs aren't clear, use the **Network tab**:

1. Press **F12**
2. Go to **Network** tab
3. Register
4. Look for these requests in order:
   - ✅ `app.js?v=4` — 200 OK
   - ✅ `registration.js` — 200 OK
   - ✅ `api.js` — 200 OK
   - ✅ `POST /users/register` — 200 OK
   - ✅ `test.html` — 200 OK
   - ✅ `test.js` — 200 OK
   - ✅ `style.css` — 200 OK

Any **RED** requests or non-200 status codes are problems.

---

## localStorage Check

The auto-login works if these are set:

**In Console, type:**

```javascript
console.log('Token:', localStorage.getItem('anaida_token'));
console.log('Email:', localStorage.getItem('anaida_user_email'));
```

**Expected output:**
```
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Email: yourname@example.com
```

If both are set, authentication should work!

---

## Test Token Validity

**In Console, type:**

```javascript
fetch('/users/me', {
  headers: { 'Authorization': 'Bearer ' + localStorage.getItem('anaida_token') }
}).then(r => r.json()).then(d => console.log(d))
```

**Expected output:**
```
{ email: "yourname@example.com", authenticated: true }
```

---

## If STILL Not Working

1. **Hard refresh browser:**
   - Windows: Ctrl+Shift+R
   - Mac: Cmd+Shift+R

2. **Clear all browser cache:**
   - See "Step 1" above

3. **Check backend is running:**
   - Open terminal
   - Run: `curl http://localhost:8080/health`
   - Should return: `{"status":"ok","database":"connected"}`
   - If error, restart servers: `bash run.sh`

4. **Check frontend is running:**
   - Run: `curl http://localhost:3000/registration.html | head -10`
   - Should return HTML starting with `<!DOCTYPE html>`

5. **Open browser DevTools and screenshot the Console**
   - Look for any RED errors
   - You may need to share this with support

---

## File Locations (If You Need to Manually Check)

```
frontend/site/
├── registration.html      ← Registration page
├── test.html              ← Test/quiz page
└── js/modules/
    ├── app.js             ← Main initializer (HAS LOGGING)
    ├── registration.js    ← Auto-login logic (HAS LOGGING)
    ├── api.js             ← API client (HAS LOGGING)
    └── test.js            ← Quiz logic (HAS LOGGING)
```

All files with logging enabled starting today!

---

## Quick Checklist

- [ ] Closed and reopened browser after restart?
- [ ] Cleared browser cache?
- [ ] Did hard refresh (Ctrl+Shift+R)?
- [ ] Checked Console for errors (F12)?
- [ ] Unique email each test (no duplicates)?
- [ ] Password at least 6 characters?
- [ ] Backend running (curl health check)?
- [ ] Frontend running (can access registration.html)?
- [ ] Checked localStorage has token set?

---

## Success Indicators

You'll know it's working when you see:

✅ Page redirects automatically after "Create Account"  
✅ test.html loads with quiz title and questions  
✅ No errors in Console (F12)  
✅ Console shows "✓ Quiz: Fully initialized"  
✅ localStorage has token and email set  
✅ Can click answers and see quiz progress  

---

**Any issues? Check the Console first — the logging will tell us exactly where the problem is!** 🔍

