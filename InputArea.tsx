import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles } from 'lucide-react';
import { cn } from '../lib/utils';

interface InputAreaProps {
    onSend: (message: string) => void;
    disabled?: boolean;
}

export const InputArea: React.FC<InputAreaProps> = ({ onSend, disabled }) => {
    const [input, setInput] = useState('');
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSubmit = (e?: React.FormEvent) => {
        e?.preventDefault();
        if (input.trim() && !disabled) {
            onSend(input.trim());
            setInput('');
            if (textareaRef.current) {
                textareaRef.current.style.height = 'auto';
            }
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInput(e.target.value);
        // Auto-resize
        e.target.style.height = 'auto';
        e.target.style.height = `${e.target.scrollHeight}px`;
    };

    return (
        <div className="relative w-full max-w-4xl mx-auto p-4 bg-white/80 backdrop-blur-md border border-secondary-200 rounded-3xl shadow-lg mt-4">
            <form onSubmit={handleSubmit} className="flex items-end gap-2">
                <textarea
                    ref={textareaRef}
                    value={input}
                    onChange={handleInput}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask me anything..."
                    rows={1}
                    disabled={disabled}
                    className="flex-1 max-h-32 bg-transparent border-0 focus:ring-0 resize-none p-3 text-secondary-800 placeholder:text-secondary-400 focus:outline-none"
                    style={{ minHeight: '44px' }}
                />
                <button
                    type="submit"
                    disabled={!input.trim() || disabled}
                    className={cn(
                        "p-3 rounded-xl transition-all duration-200 flex-shrink-0",
                        input.trim() && !disabled
                            ? "bg-primary-600 text-white hover:bg-primary-700 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
                            : "bg-secondary-100 text-secondary-400 cursor-not-allowed"
                    )}
                >
                    {disabled ? <Sparkles className="animate-spin" size={20} /> : <Send size={20} />}
                </button>
            </form>
        </div>
    );
};
