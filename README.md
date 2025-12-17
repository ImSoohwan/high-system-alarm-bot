📄 한국어 문서는 README_KR.md를 참고하세요.

# Extracurricular Program Notification Bot

A Python-based notification system that monitors a university extracurricular program website and sends real-time alerts to Discord when matching announcements are posted.  
The system is designed to run continuously on a Raspberry Pi with minimal resource usage.

---

## Motivation

Extracurricular programs at my university are filled on a first-come, first-served basis, often without a clearly announced opening time.  
To avoid missing opportunities due to delayed manual checks, this project aims to automatically detect new announcements and notify users immediately.

---

## Core Features

- Automated monitoring of a login-required, dynamically rendered website  
- Real-time Discord notifications  
- Keyword-based filtering of announcements  
- Runtime configuration via Discord bot commands  
- Lightweight and stable 24/7 operation on Raspberry Pi  

---

## Tech Stack

- Python  
- requests  
- aiohttp  
- BeautifulSoup  
- Discord Bot API  
- Raspberry Pi (Linux)

---

## System Architecture

1. Periodically request the extracurricular program list  
2. Parse program titles and metadata  
3. Compare results against registered keywords  
4. Send notifications to Discord when matches are found  
5. Allow runtime control through Discord bot commands  

---

## Implementation Journey & Key Decisions

### 1. Static Web Scraping (Initial Attempt)

The first approach used `requests` and `BeautifulSoup` to scrape HTML content directly.  
This failed because the website rendered program data dynamically using JavaScript, resulting in empty responses.

**Lesson learned:**  
Static scraping is insufficient for JavaScript-driven websites.

---

### 2. Selenium-Based Scraping

Selenium was introduced to control a real browser session, allowing dynamic content to load correctly.  
Login automation and data extraction were successful, and Discord Webhook notifications were implemented.

**Problem:**  
Selenium was too resource-intensive for Raspberry Pi, making it unsuitable for long-term 24/7 operation.

**Lesson learned:**  
A solution that works functionally may still fail operationally.

---

### 3. API-Based Scraping (Final Solution)

By analyzing browser network traffic using developer tools, an internal AJAX endpoint used by the website was discovered.  
The project was redesigned to replicate this API request directly using proper headers and payloads.

**Results:**  
- Selenium completely removed  
- Significant performance improvement  
- Stable execution on Raspberry Pi  

**Key insight:**  
Many dynamic websites rely on undocumented internal APIs that can be accessed directly.

---

## Discord Bot Integration

To eliminate hardcoded configuration values and improve usability, the system was rebuilt as a Discord bot.

### Supported Commands

- `!키워드 추가 <keyword>` / `!키워드 삭제 <keyword>`  
- `!쿨타임설정 <seconds>`  
- `!시작`, `!중지`, `!status`  

---

## Asynchronous Scraping

Discord bots operate asynchronously, and blocking HTTP requests would freeze the bot.  
To prevent this, `aiohttp` was used to perform non-blocking API requests.

```python
async with aiohttp.ClientSession() as session:
    async with session.post(api_url, headers=headers, data=payload) as res:
        text = await res.text()
This allows scraping tasks to run concurrently without interrupting bot responsiveness.

---

## Deployment

- Deployed on Raspberry Pi for continuous 24/7 operation  
- Optimized for low CPU and memory usage  
- Platform-specific issues (Windows → Linux) were resolved during deployment  

---

## Limitations

- Relies on undocumented internal APIs that may change  
- Tightly coupled to the university website structure  
- Requires valid user credentials  

---

## Outcome

- Real-time notifications delivered immediately after announcements are posted  
- Enabled multiple users to register simultaneously without missing deadlines  
- Achieved stable long-term operation with minimal system resources  

---

## Author

ImSoohwan
