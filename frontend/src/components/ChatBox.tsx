"use client";
import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Box, Button, TextField, Typography, Paper } from "@mui/material";

const generateSessionId = () =>
    typeof crypto !== "undefined" && crypto.randomUUID
        ? crypto.randomUUID()
        : Math.random().toString(36).substring(2) + Date.now().toString(36);

interface Message {
    source: "user" | "bot";
    text: string;
}

export default function ChatBox() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [sessionId] = useState<string>(generateSessionId);
    const scrollRef = useRef<HTMLDivElement>(null);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const newMessage: Message = { source: "user", text: input };
        setMessages((prev) => [...prev, newMessage]);

        try {
            const res = await axios.post("http://localhost:8000/v1/conversations", {
                session_id: sessionId,
                user_id: "demo_user",
                payload: { content: input },
                context: {},
            });

            const botMessage: Message = {
                source: "bot",
                text: res.data.messages?.[0]?.text ?? "No response",
            };
            setMessages((prev) => [...prev, botMessage]);
        } catch (err) {
            console.error(err);
            setMessages((prev) => [
                ...prev,
                { source: "bot", text: "Error connecting to AI." },
            ]);
        }
        setInput("");
    };

    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    return (
        <Paper elevation={3} sx={{ p: 2, maxWidth: 600, mx: "auto", mt: 4 }}>
            <Box sx={{ height: 400, overflowY: "auto", mb: 2 }}>
                {messages.map((m, idx) => (
                <Box
                    key={idx}
                    sx={{
                    display: "flex",
                    justifyContent: m.source === "user" ? "flex-end" : "flex-start",
                    mb: 1,
                    }}
                >
                    <Box
                    sx={{
                        bgcolor: m.source === "user" ? "primary.main" : "grey.300",
                        color: m.source === "user" ? "white" : "black",
                        p: 1,
                        borderRadius: 1,
                        maxWidth: "80%",
                    }}
                    >
                        <Typography variant="body1">{m.text}</Typography>
                    </Box>
                </Box>
                ))}
                <div ref={scrollRef}></div>
            </Box>
            <Box sx={{ display: "flex" }}>
                <TextField
                    fullWidth
                    variant="outlined"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                    placeholder="Type your message..."
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={sendMessage}
                    sx={{ ml: 1 }}
                >
                    Send
                </Button>
            </Box>
        </Paper>
    );
}
