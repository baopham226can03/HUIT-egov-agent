const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const axios = require("axios");
const cors = require("cors");

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: { origin: "*" },
});

require('dotenv').config();

app.use(express.static("public"));
app.use(cors());

const queue = []; // Hàng đợi lưu câu hỏi
const activeClients = {}; // Lưu danh sách client trong group

io.on("connection", (socket) => {
    console.log("User connected:", socket.id);

    // Khi user join vào group chat
    socket.on("joinGroup", (groupId) => {
        socket.join(socket.id);
        activeClients[socket.id] = socket.id;
        console.log(`User ${socket.id} joined group ${groupId}`);
    });

    // Khi user gửi câu hỏi
    socket.on("sendQuestion", async ({ groupId, question }) => {
        // console.log(`Nhóm ${groupId} nhận câu hỏi: ${question}`);
        // callStreamingAPI(groupId, question);
        queue.push({ clientId: socket.id, groupId:socket.id, question });
    });

    socket.on("disconnect", () => {
        delete activeClients[socket.id];
        console.log("User disconnected:", socket.id);

        // Xóa tất cả câu hỏi của client đã disconnect khỏi hàng đợi
        const newQueue = queue.filter((item) => item.clientId !== socket.id);
        queue.length = 0; // Xóa hết phần tử cũ
        queue.push(...newQueue); // Gán lại hàng đợi mới

        console.log("Updated queue after disconnect:", queue);
    });
});

var apiIsRunning = false;

// Gọi API và gửi từng phần response về đúng group
async function callStreamingAPI(groupId, question) {
    try {
        apiIsRunning = true;
        const response = await axios({
            method: "POST", // Hoặc "POST" nếu API yêu cầu
            url: process.env.AGENT_SERVICE_URL,
            data: { question }, // Gửi câu hỏi theo query string (nếu API hỗ trợ)
            responseType: "stream",
        });


        response.data.on("data", (chunk) => {
            const text = chunk.toString(); // Xử lý chuỗi tránh khoảng trắng dư thừa
            console.log(text);
            if (text) {
                io.to(groupId).emit("response", { text });
            }
        });

        response.data.on("end", () => {
            io.to(groupId).emit("response", { text:"", isEnd:true });
            response.data.removeAllListeners(); // Giải phóng bộ nhớ tránh memory leak
            apiIsRunning = false;
        });

        response.data.on("error", (err) => {
            console.error("Lỗi khi nhận dữ liệu từ API:", err);
            io.to(groupId).emit("response", { text: "Lỗi từ API", isEnd:true });
            apiIsRunning = false;
        });
    } catch (error) {
        console.error("Lỗi khi gọi API:", error.message);
        io.to(groupId).emit("response", { text: "Lỗi kết nối API", isEnd:true });
        apiIsRunning = false;
    }
}

async function processQueue() {
    while (true) {
        if (queue.length > 0 && !apiIsRunning) {
            console.log("queue", queue);
            const { clientId, question } = queue.shift(); // Lấy request đầu tiên
            console.log("process", clientId, question);
            await callStreamingAPI(clientId, question); // Gọi API và gửi về client từng từ
            await new Promise((resolve) => setTimeout(resolve, 1500));
        } else {
            await new Promise((resolve) => setTimeout(resolve, 500));
        }
    }
}

server.listen(process.env.MESSAGE_QUEUE_SERVICE_PORT,"0.0.0.0", () =>
    console.log("Server listening on port ", server.address().address + ":" + process.env.MESSAGE_QUEUE_SERVICE_PORT));
processQueue(); // Chạy process hàng đợi
