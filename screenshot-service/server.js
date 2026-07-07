const express = require('express');
const puppeteer = require('puppeteer');
const app = express();

app.get('/health', (req, res) => {
  res.send('OK');
});

app.get('/screenshot', async (req, res) => {
  let url = req.query.url;
  if (!url) return res.status(400).send('Missing URL');

  // Prepend protocol if missing
  if (!/^https?:\/\//i.test(url)) {
    url = 'https://' + url;
  }

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    // Set viewport and goto with timeout
    await page.goto(url, { 
      waitUntil: 'networkidle2', 
      timeout: 30000 
    });
    
    const screenshot = await page.screenshot({
      fullPage: true, // Capture the entire scrollable page
      type: 'png'
    });
    
    res.set('Content-Type', 'image/png');
    res.send(screenshot);
    
  } catch (error) {
    console.error(`Error taking screenshot for ${url}:`, error.message);
    res.status(500).send('Error taking screenshot: ' + error.message);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Screenshot service running on port ${PORT}`));
