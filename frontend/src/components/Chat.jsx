import React, {
    useRef,
    useState,
} from "react";

import {
    sendChatMessage,
} from "../services/api";


function formatResponse(data) {

    if (!data) {
        return "The AI returned an empty response.";
    }

    if (typeof data === "string") {
        return data;
    }

    if (data.response) {

        if (
            typeof data.response ===
            "string"
        ) {
            return data.response;
        }

        return JSON.stringify(
            data.response,
            null,
            2
        );
    }

    if (data.answer) {
        return typeof data.answer ===
            "string"
            ? data.answer
            : JSON.stringify(
                  data.answer,
                  null,
                  2
              );
    }

    if (data.message) {
        return typeof data.message ===
            "string"
            ? data.message
            : JSON.stringify(
                  data.message,
                  null,
                  2
              );
    }

    return JSON.stringify(
        data,
        null,
        2
    );
}


export default function Chat({
    onResponse,
    fileId,
}) {

    const [messages, setMessages] =
        useState([]);

    const [input, setInput] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    const messagesRef =
        useRef(null);


    const sendMessage = async () => {

        const query =
            input.trim();

        if (
            !query ||
            loading
        ) {
            return;
        }

        setMessages(
            previous => [
                ...previous,

                {
                    role: "user",
                    content: query,
                },
            ]
        );

        setInput("");
        setLoading(true);

        try {

            const data =
                await sendChatMessage(
                    query,
                    fileId
                );

            console.log(
                "Chat response:",
                data
            );

            const responseText =
                formatResponse(data);

            setMessages(
                previous => [
                    ...previous,

                    {
                        role:
                            "assistant",

                        content:
                            responseText,

                        artifact:
                            data.artifact ||
                            null,
                    },
                ]
            );

            if (onResponse) {
                onResponse(data);
            }

        } catch (error) {

            console.error(
                "Chat error:",
                error
            );

            setMessages(
                previous => [
                    ...previous,

                    {
                        role:
                            "assistant",

                        content:
                            `⚠️ ${error.message}`,

                        error: true,
                    },
                ]
            );

        } finally {

            setLoading(false);

            setTimeout(() => {

                if (
                    messagesRef.current
                ) {

                    messagesRef.current
                        .scrollTop =
                        messagesRef.current
                            .scrollHeight;
                }

            }, 50);
        }
    };


    const handleKeyDown =
        (event) => {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendMessage();
            }
        };


    return (
        <section className="chat-card">

            <div className="chat-header">

                <h2>
                    AI Assistant
                </h2>

                <p>
                    Ask questions about your
                    documents or request
                    document/PPT generation.
                </p>

            </div>


            <div
                className="chat-messages"
                ref={messagesRef}
            >

                {messages.length === 0 && (
                    <div className="empty-chat">

                        <div>
                            🤖
                        </div>

                        <p>
                            Ask something about
                            your uploaded document.
                        </p>

                        <small>
                            Example: "Create an
                            8-slide PPT from
                            my resume."
                        </small>

                    </div>
                )}


                {messages.map(
                    (message, index) => (

                        <div
                            key={index}
                            className={
                                `message ${
                                    message.role ===
                                    "user"
                                        ? "user-message"
                                        : "assistant-message"
                                }`
                            }
                        >

                            <div
                                className={
                                    message.error
                                        ? "message-bubble error-message"
                                        : "message-bubble"
                                }
                            >
                                {message.content}
                            </div>

                        </div>
                    )
                )}


                {loading && (
                    <div className="message assistant-message">

                        <div className="message-bubble">

                            <span>
                                🤖 AI is working...
                            </span>

                        </div>

                    </div>
                )}

            </div>


            <div className="chat-input-area">

                <textarea
                    value={input}
                    onChange={(event) =>
                        setInput(
                            event.target.value
                        )
                    }
                    onKeyDown={
                        handleKeyDown
                    }
                    placeholder={
                        "Ask the AI something..."
                    }
                    rows={2}
                    disabled={loading}
                />

                <button
                    onClick={
                        sendMessage
                    }
                    disabled={
                        loading ||
                        !input.trim()
                    }
                >
                    {loading
                        ? "..."
                        : "Send"}
                </button>

            </div>

        </section>
    );
}