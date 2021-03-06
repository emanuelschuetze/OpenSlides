import { ChatMessage } from 'app/shared/models/core/chat-message';
import { BaseViewModel } from 'app/site/base/base-view-model';

export class ViewChatMessage extends BaseViewModel {
    public static COLLECTIONSTRING = ChatMessage.COLLECTIONSTRING;

    private _chatMessage: ChatMessage;

    /**
     * This is set by the repository
     */
    public getVerboseName;

    public get chatmessage(): ChatMessage {
        return this._chatMessage;
    }

    public get id(): number {
        return this.chatmessage.id;
    }

    public get message(): string {
        return this.chatmessage.message;
    }

    public constructor(message?: ChatMessage) {
        super(ChatMessage.COLLECTIONSTRING);
        this._chatMessage = message;
    }

    public getTitle = () => {
        return 'Chatmessage';
    };

    public getModel(): ChatMessage {
        return this.chatmessage;
    }

    public updateDependencies(message: BaseViewModel): void {}
}
