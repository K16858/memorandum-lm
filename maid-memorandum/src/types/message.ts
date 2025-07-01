export interface Message {
    id: number,
    content: string,
    sender: 'user' | 'assistant' | 'system'
}
