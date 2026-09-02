const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, downloadMediaMessage } = require('@whiskeysockets/baileys');
const QRCode = require('qrcode');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');
const url = require('url');
const https = require('https');

const PORT = 3000;
const PROJECT_REPORTS_DIR = 'C:\\Users\\denni\\Downloads\\Compressed\\n8n-skills-2.21.0\\n8n-reports';
const AUTHORIZED_NUMBERS = [
    '254718369274', // Maggy Njoki
    '254722586543', // Mr. Gichuhi
    '254727295273', // Edwin
    '254796340713', // Ken
    '254798381229', // Willy
    '254115763781', // Kinoti
];
const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

// ⚠️ IMPORTANT: After importing the workflow into n8n Cloud, replace this URL
// with your actual webhook URL from the Webhook Trigger node.
// Format: http://localhost:5678/webhook/whatsapp-report
const N8N_WEBHOOK_URL = 'http://localhost:5678/webhook/whatsapp-report';

let currentQrDataUrl = null;
let isConnected = false;
let waSock = null;

if (!fs.existsSync(PROJECT_REPORTS_DIR)) {
    fs.mkdirSync(PROJECT_REPORTS_DIR, { recursive: true });
}

function resolveTargetFolder(text = "") {
    const match = text.match(/(\d{1,2})(?:st|nd|rd|th)?\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)/i);
    if (match) {
        const day = parseInt(match[1], 10);
        const monthRaw = match[2].toLowerCase();
        const monthNames = { jan: 'Jan', feb: 'Feb', mar: 'Mar', apr: 'Apr', may: 'May', jun: 'Jun', jul: 'Jul', aug: 'Aug', sep: 'Sep', oct: 'Oct', nov: 'Nov', dec: 'Dec' };
        const month = monthNames[monthRaw] || 'Aug';
        const suffix = (day === 1 || day === 21 || day === 31) ? 'st' :
                       (day === 2 || day === 22) ? 'nd' :
                       (day === 3 || day === 23) ? 'rd' : 'th';
        const targetPath = path.join(PROJECT_REPORTS_DIR, `Report ${day}${suffix} ${month}`);
        if (!fs.existsSync(targetPath)) fs.mkdirSync(targetPath, { recursive: true });
        return { folder: targetPath, dateStr: `${day}${suffix} ${month}` };
    }

    const now = new Date();
    const day = now.getDate();
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const month = monthNames[now.getMonth()];
    const suffix = (day === 1 || day === 21 || day === 31) ? 'st' :
                   (day === 2 || day === 22) ? 'nd' :
                   (day === 3 || day === 23) ? 'rd' : 'th';
    const targetPath = path.join(PROJECT_REPORTS_DIR, `Report ${day}${suffix} ${month}`);
    if (!fs.existsSync(targetPath)) fs.mkdirSync(targetPath, { recursive: true });
    return { folder: targetPath, dateStr: `${day}${suffix} ${month}` };
}

// ============================================================
// 🚀 TRIGGER n8n CLOUD WORKFLOW
// Flow: Bridge POSTs logs → n8n runs Gemini AI Vision → n8n returns HTML
//       → Bridge saves index.html → Bridge compiles PDF → Bridge sends to WhatsApp
// ============================================================
function triggerN8nWorkflow(targetFolder, dateStr, userCommand = null) {
    const logPath = path.join(targetFolder, 'daily_supervisor_logs.json');
    let logs = [];
    if (fs.existsSync(logPath)) {
        try { logs = JSON.parse(fs.readFileSync(logPath, 'utf-8')); } catch(e) {}
    }

    const payload = JSON.stringify({
        targetFolder,
        reportDate: dateStr,
        logs,
        userCommand
    });

    const parsedUrl = new URL(N8N_WEBHOOK_URL);
    const options = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
        path: parsedUrl.pathname,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(payload)
        }
    };

    console.log(`\n🌐 [n8n Trigger] Sending data to n8n Cloud workflow...`);
    console.log(`   📡 Webhook: ${N8N_WEBHOOK_URL}`);
    console.log(`   📁 Target Folder: ${targetFolder}`);
    console.log(`   📅 Report Date: ${dateStr}`);
    console.log(`   📝 Log entries: ${logs.length}`);

    const client = parsedUrl.protocol === 'https:' ? https : http;
    const req = client.request(options, (res) => {
        let body = '';
        res.on('data', chunk => { body += chunk; });
        res.on('end', async () => {
            if (res.statusCode >= 200 && res.statusCode < 300) {
                console.log(`✅ [n8n Response] Workflow completed! Status: ${res.statusCode}`);
                try {
                    const responseData = JSON.parse(body);

                    // n8n returns { status, reportDate, targetFolder, htmlReport, kpis }
                    if (responseData.htmlReport) {
                        // Save the AI-generated HTML report
                        const htmlPath = path.join(targetFolder, 'index.html');
                        fs.writeFileSync(htmlPath, responseData.htmlReport, 'utf-8');
                        console.log(`📝 [n8n → Bridge] Saved AI-generated index.html to ${targetFolder}`);

                        // Compile PDF with Edge and deliver to WhatsApp
                        compileAndSendPdf(targetFolder, waSock?.user?.id, dateStr);
                    } else {
                        console.log(`⚠️  [n8n Response] No htmlReport in response. Response keys: ${Object.keys(responseData).join(', ')}`);
                    }
                } catch(e) {
                    console.error(`❌ [n8n Response] Failed to parse response: ${e.message}`);
                    console.error(`   Raw response: ${body.slice(0, 500)}`);
                }
            } else {
                console.error(`❌ [n8n Trigger] Failed! Status: ${res.statusCode}`);
                console.error(`   Response: ${body.slice(0, 300)}`);
            }
        });
    });

    req.on('error', (err) => {
        console.error(`❌ [n8n Trigger] Connection error: ${err.message}`);
        console.error(`   Make sure your n8n Cloud workflow is active and the webhook URL is correct.`);
    });

    req.write(payload);
    req.end();
}

// ============================================================
// PDF Compiler & WhatsApp Deliverer
// ============================================================
function compileAndSendPdf(targetFolder, recipientJid, dateStr, callback) {
    const htmlFile = path.join(targetFolder, 'index.html');
    const pdfFile = path.join(targetFolder, `Daily_Operations_Report_${dateStr.replace(/[^a-zA-Z0-9]/g, '_')}.pdf`);

    if (fs.existsSync(htmlFile)) {
        const cmd = `"${EDGE_PATH}" --headless --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf="${pdfFile}" "${htmlFile}"`;
        console.log(`📄 [PDF Compiler] Compiling HTML → PDF...`);
        exec(cmd, async (err) => {
            if (err) console.error("Edge PDF compile error:", err);
            else console.log(`📄 [PDF Compiled] ${pdfFile}`);
            
            await deliverToWhatsApp(pdfFile, recipientJid, dateStr);
            if (callback) callback();
        });
    } else {
        console.error(`❌ [PDF Compiler] No index.html found in ${targetFolder}`);
        if (callback) callback();
    }
}

async function deliverToWhatsApp(pdfPath, recipientJid, dateStr) {
    if (!waSock || !isConnected || !fs.existsSync(pdfPath)) return;
    try {
        // Strip the device ID (e.g. :23) from the JID to ensure it goes to the primary phone
        let targetJid = recipientJid || waSock?.user?.id || '';
        targetJid = targetJid.replace(/:\d+/, '');

        // If it's a LID, force it to the main WhatsApp number
        if (targetJid.endsWith('@lid') && waSock?.user?.id) {
            targetJid = waSock.user.id.replace(/:\d+/, '');
        }
            
        console.log(`📤 Sending PDF to Dennis on WhatsApp (${targetJid})...`);
        const pdfBuffer = fs.readFileSync(pdfPath);
        
        await waSock.sendMessage(targetJid, {
            document: pdfBuffer,
            mimetype: 'application/pdf',
            fileName: path.basename(pdfPath),
            caption: `📄 *Daily Operations Progress Report — ${dateStr}*\n👤 *Compiled by Dennis*\n✅ *Generated by n8n Gemini AI Vision Pipeline!*`
        });
        console.log(`\n🚀 [Delivered to WhatsApp] PDF Report shared directly into Dennis's WhatsApp chat!`);
    } catch (e) {
        console.error("Error delivering PDF to WhatsApp:", e.message);
    }
}

// ============================================================
// HTTP Server — also accepts manual /api/deliver-report for direct use
// ============================================================
const server = http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);

    // Manual endpoint: POST /api/deliver-report
    // Accepts { targetFolder, reportDate, htmlReport? }
    // If htmlReport is provided, saves it as index.html first
    if (parsedUrl.pathname === '/api/deliver-report' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString('utf-8'); });
        req.on('end', async () => {
            try {
                const data = JSON.parse(body || '{}');
                const targetFolder = data.targetFolder || path.join(PROJECT_REPORTS_DIR, 'Report 26th Aug');
                const dateStr = data.reportDate || "26th August 2026";

                // If HTML report was included, save it
                if (data.htmlReport) {
                    const htmlPath = path.join(targetFolder, 'index.html');
                    fs.writeFileSync(htmlPath, data.htmlReport, 'utf-8');
                    console.log(`📝 [API] Saved HTML report to ${targetFolder}`);
                }

                compileAndSendPdf(targetFolder, waSock?.user?.id, dateStr, () => {
                    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
                    res.end(JSON.stringify({ status: "SUCCESS", message: "Report compiled and sent to WhatsApp!" }));
                });
            } catch (err) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: "ERROR", error: err.message }));
            }
        });
        return;
    }

    // Manual trigger: POST /api/trigger-n8n
    // Accepts { targetFolder?, reportDate? } — triggers the n8n workflow
    if (parsedUrl.pathname === '/api/trigger-n8n' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString('utf-8'); });
        req.on('end', () => {
            try {
                const data = JSON.parse(body || '{}');
                const { folder, dateStr } = resolveTargetFolder(data.reportDate || '');
                const targetFolder = data.targetFolder || folder;
                triggerN8nWorkflow(targetFolder, data.reportDate || dateStr);
                res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
                res.end(JSON.stringify({ status: "TRIGGERED", message: `n8n workflow triggered for ${dateStr}` }));
            } catch (err) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: "ERROR", error: err.message }));
            }
        });
        return;
    }

    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    if (isConnected) {
        res.end(`<!DOCTYPE html><html><body style="font-family:system-ui;background:#0f172a;color:white;display:flex;align-items:center;justify-content:center;height:100vh;"><div style="background:#1e293b;padding:40px;border-radius:20px;text-align:center;max-width:500px;"><h1 style="color:#4ade80;">✅ WhatsApp Bridge Active</h1><p style="margin-top:10px;">n8n Cloud → Gemini AI Vision → PDF → WhatsApp</p><p style="margin-top:16px;color:#94a3b8;font-size:0.85rem;word-break:break-all;">Webhook: ${N8N_WEBHOOK_URL}</p></div></body></html>`);
        return;
    }
    res.end(`<!DOCTYPE html><html><body style="font-family:system-ui;background:#0f172a;color:white;display:flex;align-items:center;justify-content:center;height:100vh;"><div style="background:#1e293b;padding:36px;border-radius:20px;text-align:center;"><div style="background:white;padding:20px;border-radius:16px;display:inline-block;">${currentQrDataUrl ? `<img src="${currentQrDataUrl}" style="width:280px;height:280px;">` : `<p style="color:#333;">Generating QR...</p>`}</div></div></body></html>`);
});

server.listen(PORT, () => {
    console.log(`\n🌐 WhatsApp Bridge active on port ${PORT}`);
});

async function startWhatsAppBridge() {
    const authPath = path.join(__dirname, 'auth_info_baileys');
    const { state, saveCreds } = await useMultiFileAuthState(authPath);

    waSock = makeWASocket({ auth: state, printQRInTerminal: false });
    waSock.ev.on('creds.update', saveCreds);

    waSock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;
        if (qr) currentQrDataUrl = await QRCode.toDataURL(qr, { width: 320, margin: 2 });
        if (connection === 'close') {
            isConnected = false;
            const shouldReconnect = (lastDisconnect?.error)?.output?.statusCode !== DisconnectReason.loggedOut;
            if (shouldReconnect) startWhatsAppBridge();
        } else if (connection === 'open') {
            isConnected = true;
            console.log('\n=============================================');
            console.log('✅ WHATSAPP CONNECTED & READY');
            console.log('👤 Self-Chat (@lid / Dennoh) FULLY SUPPORTED');
            console.log(`📁 Project Reports: ${PROJECT_REPORTS_DIR}`);
            console.log(`🌐 n8n Webhook: ${N8N_WEBHOOK_URL}`);
            console.log('=============================================\n');
        }
    });

    waSock.ev.on('messages.upsert', async (m) => {
        const msg = m.messages[0];
        if (!msg || !msg.message) return;

        const senderJid = msg.key.remoteJid || "";

        if (
            senderJid.endsWith('@newsletter') || 
            senderJid.endsWith('@broadcast') || 
            senderJid === 'status@broadcast' ||
            senderJid.startsWith('120363') ||
            msg.message.documentMessage // Prevent infinite loop when sending PDFs
        ) return;

        const sender = senderJid.split('@')[0];
        const pushName = msg.pushName || "Supervisor";
        const isFromDennis = msg.key.fromMe || senderJid.endsWith('@lid') || (waSock?.user?.id && senderJid.includes(waSock.user.id.split(':')[0]));

        const isAuthorized = isFromDennis || AUTHORIZED_NUMBERS.includes(sender);
        if (!isAuthorized) {
            console.log(`\n🚫 [Unauthorized] Ignoring message from ${pushName} (${senderJid})`);
            return;
        }

        let text = msg.message.conversation || 
                   msg.message.extendedTextMessage?.text || 
                   msg.message.imageMessage?.caption || 
                   msg.message.videoMessage?.caption || "";

        const isSelfChat = senderJid.endsWith('@lid') || (waSock?.user?.id && senderJid.includes(waSock.user.id.split(':')[0]));
        if (msg.key.fromMe && !isSelfChat && !text.includes('!report')) {
            console.log(`\n🚫 [Ignored] Outgoing message to supervisor`);
            return;
        }

        const contextInfo = msg.message.extendedTextMessage?.contextInfo || 
                            msg.message.imageMessage?.contextInfo || 
                            msg.message.videoMessage?.contextInfo;
                            
        let quotedDateStr = null;
        if (contextInfo && contextInfo.quotedMessage && contextInfo.quotedMessage.documentMessage) {
            const fileName = contextInfo.quotedMessage.documentMessage.fileName || "";
            const match = fileName.match(/Daily_Operations_Report_(.+)\.pdf/);
            if (match) {
                quotedDateStr = match[1].replace(/_/g, ' '); 
                console.log(`📎 [Reply Detected] Message is a reply to report from: ${quotedDateStr}`);
            }
        }

        const hasImage = Boolean(msg.message.imageMessage);
        const hasVideo = Boolean(msg.message.videoMessage);

        console.log(`\n📥 [Incoming WhatsApp Message] from ${pushName} (${senderJid}): "${text || (hasImage ? 'Photo attached' : '')}"`);

        const { folder: targetFolder, dateStr } = resolveTargetFolder(quotedDateStr || text);

        let userCommand = null;
        if (text && text.includes('!report')) {
            const parts = text.split(/:\s*/);
            if (parts.length > 1) {
                userCommand = parts.slice(1).join(': ');
            }
        }

        let savedFilePath = null;
        if (hasImage || hasVideo) {
            try {
                const buffer = await downloadMediaMessage(msg, 'buffer', {});
                const ext = hasImage ? 'jpeg' : 'mp4';
                const cleanDesc = text ? text.replace(/[^a-zA-Z0-9]/g, '_').slice(0, 30) : 'WhatsApp_Update';
                const filename = `${cleanDesc}_${Date.now()}.${ext}`;
                savedFilePath = path.join(targetFolder, filename);
                fs.writeFileSync(savedFilePath, buffer);
                console.log(`📸 [Media Downloaded] Saved as: ${filename}`);
            } catch (err) {
                console.error('Error downloading media:', err.message);
            }
        }

        // Log message to daily logs
        const logPath = path.join(targetFolder, 'daily_supervisor_logs.json');
        let logs = [];
        if (fs.existsSync(logPath)) {
            try { logs = JSON.parse(fs.readFileSync(logPath, 'utf-8')); } catch(e) {}
        }
        logs.push({
            timestamp: new Date().toISOString(),
            sender,
            senderJid,
            pushName,
            isFromDennis,
            text,
            hasMedia: Boolean(savedFilePath),
            savedFilePath
        });
        fs.writeFileSync(logPath, JSON.stringify(logs, null, 2));

        console.log(`✅ [Logged into Report ${dateStr}] ${pushName}: ${text || '(media only)'}`);

        // 🚀 TRIGGER n8n CLOUD WORKFLOW (Gemini AI → HTML → PDF → WhatsApp)
        if (isFromDennis || text.includes('!report')) {
            console.log(`⚡ Triggering n8n Cloud AI Vision workflow...`);
            triggerN8nWorkflow(targetFolder, dateStr, userCommand);
        }
    });
}

startWhatsAppBridge();
