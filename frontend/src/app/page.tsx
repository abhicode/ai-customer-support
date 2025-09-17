"use client";

import { Container, Typography } from "@mui/material";
import ChatBox from "@/components/ChatBox";

export default function Home() {
    return (
        <Container>
            <Typography variant="h4" align="center" sx={{ mt: 4 }}>
                AI Customer Support
            </Typography>
            <ChatBox />
        </Container>
    );
}