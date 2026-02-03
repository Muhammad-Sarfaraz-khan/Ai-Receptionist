import React, { useState, useEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';
import { InputArea } from './InputArea';
import { chatApi } from '../api/chat';
import { ChatMessage, ChatResponse } from '../types';
import { Sparkles, Trash2 } from 'lucide-react';

interface Message {
    id: string;
    text: string;
    isAi: boolean;
    timestamp: Date;
}

export const ChatContainer: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: 'welcome',
            text: "Hello! I'm your AI Receptionist. How can I assist you today?",
            isAi: true,
            timestamp: new Date()
        }
    ]);
    const [loading, setLoading] = useState(false);
    const [conversationId, setConversationId] = useState<string>('');
    const [suggestedActions, setSuggestedActions] = useState<string[]>([]);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    const handleSendMessage = async (text: string) => {
        // Add user message
        const userMsg: Message = {
            id: Date.now().toString(),
            text,
            isAi: false,
            timestamp: new Date()
        };
        setMessages(prev => [...prev, userMsg]);
        setLoading(true);
        setSuggestedActions([]);

        try {
            // Prepare API payload
            const payload: ChatMessage = {
                message: text,
                conversation_id: conversationId || null
            };

            const response: ChatResponse = await chatApi.sendMessage(payload);

            // Update conversation ID if new
            if (response.conversation_id) {
                setConversationId(response.conversation_id);
            }

            // Add AI response
            const aiMsg: Message = {
                id: (Date.now() + 1).toString(),
                text: response.response,
                isAi: true,
                timestamp: new Date()
            };
            setMessages(prev => [...prev, aiMsg]);

            if (response.suggested_actions) {
                setSuggestedActions(response.suggested_actions);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMsg: Message = {
                id: (Date.now() + 1).toString(),
                text: "I'm sorry, I encountered an error connecting to the server. Please try again later.",
                isAi: true,
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setLoading(false);
        }
    };

    const handleClearChat = async () => {
        if (conversationId) {
            try {
                await chatApi.clearConversation(conversationId);
            } catch (e) {
                console.error('Failed to clear conversation on server', e);
            }
        }
        setConversationId('');
        setMessages([
            {
                id: 'welcome-new',
                text: "Conversation cleared. How can I help you now?",
                isAi: true,
                timestamp: new Date()
            }
        ]);
        setSuggestedActions([]);
    };

    return (
        <div className="flex flex-col h-full w-full max-w-4xl mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-secondary-200 bg-white/50 backdrop-blur-sm sticky top-0 z-10">
                <div className="flex items-center gap-2">
                    <div className="bg-primary-100 p-2 rounded-lg">
                        <Sparkles className="text-primary-600" size={20} />
                    </div>
                    <div>
                        <h2 className="font-semibold text-secondary-800">AI Receptionist</h2>
                        <p className="text-xs text-secondary-500">Always here to help</p>
                    </div>
                </div>
                {messages.length > 1 && (
                    <button
                        onClick={handleClearChat}
                        className="text-secondary-400 hover:text-red-500 transition-colors p-2 hover:bg-red-50 rounded-lg"
                        title="Clear conversation"
                    >
                        <Trash2 size={18} />
                    </button>
                )}
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.map((msg) => (
                    <MessageBubble
                        key={msg.id}
                        message={msg.text}
                        isAi={msg.isAi}
                    />
                ))}

                {loading && (
                    <div className="flex justify-start w-full mb-4">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center">
                                <Sparkles size={18} />
                            </div>
                            <div className="bg-white border border-secondary-100 p-4 rounded-2xl rounded-tl-none flex gap-1 items-center h-[54px]">
                                <div className="w-2 h-2 bg-secondary-400 rounded-full typing-dot"></div>
                                <div className="w-2 h-2 bg-secondary-400 rounded-full typing-dot"></div>
                                <div className="w-2 h-2 bg-secondary-400 rounded-full typing-dot"></div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Suggested Actions */}
                {!loading && suggestedActions.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-2 ml-11">
                        {suggestedActions.map((action, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleSendMessage(action)}
                                className="text-sm bg-white border border-primary-200 text-primary-700 px-3 py-1.5 rounded-full hover:bg-primary-50 hover:border-primary-300 transition-colors shadow-sm"
                            >
                                {action}
                            </button>
                        ))}
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 bg-gradient-to-t from-secondary-50 to-transparent">
                <InputArea onSend={handleSendMessage} disabled={loading} />
                <p className="text-center text-xs text-secondary-400 mt-2">
                    AI can make mistakes. Please verify important information.
                </p>
            </div>
        </div>
    );
};
