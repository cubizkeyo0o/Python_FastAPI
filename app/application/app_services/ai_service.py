import json
from uuid import UUID
from typing import List, Dict, Any, Optional
from fastapi import Depends, Request

from app.infrastructure.ai_clients.gemini_client import GeminiAIClient
from app.infrastructure.ai_clients.openai_client import OpenAIClient
from app.infrastructure.cache.redis_client import RedisClient
from app.application.app_services.message_service import MessageService
from app.application.dtos.message import *
from app.utils.enums.key_cache import *
from app.utils.enums.system_role import *

class AIService:
    _gemini_client: GeminiAIClient
    _openai_client: OpenAIClient
    message_sercie: MessageService
    cache_client: RedisClient
    max_messages: 10

    def __init__(self,
                 gemini_client: GeminiAIClient = Depends(GeminiAIClient),
                 openai_client: OpenAIClient = Depends(OpenAIClient),
                 message_service: MessageService = Depends(MessageService),
                 cache_client: RedisClient = Depends(RedisClient)):
        self._gemini_client = gemini_client
        self._openai_client = openai_client
        self.message_sercie = message_service
        self.cache_client = cache_client

    async def prompt_gemini(self, request: Request, session_id: UUID, content: str):
        # 1 user has many role, but i just get fix first role
        roles = getattr(request.state, "roles", [])
        role = roles[0]

        # add messsage of user into database and cachedb
        user_msg_data = MessageCreate(session_id=session_id, role=role, content=content)
        user_msg_created = await self.message_sercie.create_message(user_msg_data)
        content_new = await self.add_message_to_session(**user_msg_created)

        # send new contenxt to ai client
        response = self._gemini_client.generate_text(content_new)
        assistant_msg = response.close()

        assistant_msg_data = MessageCreate(session_id=session_id, role=SystemRole.ASSISTANT, content=assistant_msg)
        assistant_msg_created = await self.message_sercie.create_message(assistant_msg_data)
        await self.add_message_to_session(session_id=session_id, role=SystemRole.ASSISTANT, message=assistant_msg_created)

    def _make_key(self, session_id: str) -> str:
        return f"session:{session_id}"

    async def get_session_cache(self, session_id: str):
        data = await self.cache_client.client.hgetall(self._make_key(session_id))
        if not data:
            return None
        return {
            KeyCache.SUMMARY_CONTEXT: data.get("summary_context", ""),
            KeyCache.RECENT_MESSAGES: json.loads(data.get("recent_messages", "[]"))
        }

    async def set_session_cache(self, session_id: str, summary: str, messages: List[Dict[str, str]]):
        await self.cache_client.client.hset(
            self._make_key(session_id),
            mapping={
                "summary_context": summary,
                "recent_messages": json.dumps(messages[-self.max_messages:])
            }
        )

    async def add_message_to_session(self, session_id: str, role: str, message: str):
        # get all messages 
        message_cache = await self.get_session_cache(session_id) or {
            "summary_context": "",
            "recent_messages": []
        }

        messages = message_cache["recent_messages"]
        messages.append({"role": role, "message": message})

        messages = messages[-self.max_messages:]

        await self.cache_client.client.hset(
            self._make_key(session_id),
            mapping={
                KeyCache.SUMMARY_CONTEXT: message_cache["summary_context"],
                KeyCache.RECENT_MESSAGES: json.dumps(messages)
            }
        )
        
        return {
            KeyCache.SUMMARY_CONTEXT: message_cache["summary_context"],
            KeyCache.RECENT_MESSAGES: messages
        }

    async def get_recent_messages(self, session_id: str):
        cache = await self.get_session_cache(session_id)
        return cache["recent_messages"] if cache else []

    async def get_summary_context(self, session_id: str) -> str:
        cache = await self.get_session_cache(session_id)
        return cache["summary_context"] if cache else ""

    async def update_summary_context(self, session_id: str, new_summary: str):
        await self.cache_client.client.hset(
            self._make_key(session_id),
            key=KeyCache.SUMMARY_CONTEXT,
            value=new_summary
        )

    