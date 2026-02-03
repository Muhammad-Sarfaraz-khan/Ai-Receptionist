import React from 'react';
import { cn } from '../lib/utils';
import { Bot, User } from 'lucide-react';
import { motion } from 'framer-motion';

interface MessageBubbleProps {
    message: string;
    isAi: boolean;
    timestamp?: string;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isAi, timestamp }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={cn(
                "flex w-full mb-4",
                isAi ? "justify-start" : "justify-end"
            )}
        >
            <div className={cn(
                "flex max-w-[80%] md:max-w-[70%] gap-3",
                isAi ? "flex-row" : "flex-row-reverse"
            )}>
                <div className={cn(
                    "w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0",
                    isAi ? "bg-primary-100 text-primary-600" : "bg-secondary-200 text-secondary-600"
                )}>
                    {isAi ? <Bot size={18} /> : <User size={18} />}
                </div>

                <div className={cn(
                    "p-4 rounded-2xl shadow-sm text-sm md:text-base whitespace-pre-wrap",
                    isAi
                        ? "bg-white text-secondary-800 rounded-tl-none border border-secondary-100"
                        : "bg-primary-600 text-white rounded-tr-none"
                )}>
                    {message}
                </div>
            </div>
        </motion.div>
    );
};
