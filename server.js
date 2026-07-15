import http from 'http';

const PORT = process.env.PORT || 3000;
const PLATFORM_NAME = process.env.PLATFORM_NAME || 'FOOL Platform';
const PHASE = process.env.PHASE || 'Phase 1';

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(`
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head><meta charset="UTF-8"><title>${PLATFORM_NAME}</title>
    <style>body{font-family:sans-serif;background:#0d1117;color:#c9d1d9;text-align:center;padding:50px}h1{color:#58a6ff}</style>
    </head>
    <body>
      <h1>${PLATFORM_NAME}</h1>
      <p>${PHASE}</p>
      <p>✅ العقود | ✅ النماذج | ✅ المعايير | ✅ السجل | ✅ سير العمل</p>
      <p style="color:#3fb950">🟢 الخادم يعمل على المنفذ ${PORT}</p>
    </body>
    </html>
  `);
});

server.listen(PORT, () => {
  console.log(`${PLATFORM_NAME} running on port ${PORT}`);
});
