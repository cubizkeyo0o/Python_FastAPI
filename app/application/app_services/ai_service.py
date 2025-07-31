import json
from uuid import UUID
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.infrastructure.ai_clients.gemini_client import GeminiAIClient
from app.infrastructure.ai_clients.openai_client import OpenAIClient
from app.infrastructure.cache.redis_client import RedisClient
from app.infrastructure.database.database_session import get_db_session
from app.application.app_services.message_service import MessageService
from app.application.app_services.session_service import SessionService
from app.application.dtos.message import *
from app.utils.enums.key_cache import *
from app.utils.enums.system_role import *
from app.utils.exceptions.common_exceptions import EntityNotFoundException

class AIService:
    _db: AsyncSession
    _gemini_client: GeminiAIClient
    _openai_client: OpenAIClient
    message_servie: MessageService
    session_service: SessionService
    cache_client: RedisClient
    max_messages: int

    def __init__(self,
                 db: AsyncSession = Depends(get_db_session),
                 gemini_client: GeminiAIClient = Depends(GeminiAIClient),
                 openai_client: OpenAIClient = Depends(OpenAIClient),
                 message_service: MessageService = Depends(MessageService),
                 session_service: SessionService = Depends(SessionService),
                 cache_client: RedisClient = Depends(RedisClient)):
        self._db = db
        self._gemini_client = gemini_client
        self._openai_client = openai_client
        self.message_servie = message_service
        self.session_service = session_service
        self.cache_client = cache_client
        self.max_messages = 10

    async def prompt_gemini(self, role: str, session_id: UUID, content: str):
        # add messsage of user into database and cachedb
        user_msg_data = MessageCreate(session_id=session_id, role=role, content=content)
        user_msg_created = await self.message_servie.create_message(user_msg_data)
        content_new = self.add_message_to_session(**user_msg_created.model_dump())

        response_ai = ""
        response_stream_ai = self._gemini_client.generate_text(content_new)
        # send new contenxt to ai client
        for chunk in response_stream_ai:
            if chunk.text:
                response_ai += " " + chunk.text
            yield chunk.text or ""

        assistant_msg_data = MessageCreate(session_id=session_id, role=SystemRole.MODEL, content=response_ai)
        assistant_msg_created = await self.message_servie.create_message(assistant_msg_data)
        self.add_message_to_session(**assistant_msg_created.model_dump())

        # commit all message into database
        await self._db.commit()

    def _make_key(self, session_id: str) -> str:
        return f"session:{session_id}"

    def get_session_cache(self, session_id: str):
        data = self.cache_client.client.hgetall(self._make_key(session_id))
        if not data:
            return None
        return {
            KeyCache.SUMMARY_CONTEXT: data.get("summary_context", ""),
            KeyCache.RECENT_MESSAGES: json.loads(data.get("recent_messages", "[]"))
        }

    def set_session_cache(self, session_id: str, summary: str, messages: List[Dict[str, str]]):
        self.cache_client.client.hset(
            self._make_key(session_id),
            mapping={
                "summary_context": summary,
                "recent_messages": json.dumps(messages[-self.max_messages:])
            }
        )

    def add_message_to_session(self, session_id: str, role: str, content: str):
        # get all messages 
        message_cache = self.get_session_cache(session_id) or {
            "summary_context": "",
            "recent_messages": []
        }

        messages = message_cache["recent_messages"]

        # format content request send to gemini api
        messages.append({"role": role.lower(), "parts": [{"text": content}]})

        messages = messages[-self.max_messages:]

        self.cache_client.client.hset(
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

    def get_recent_messages(self, session_id: str):
        cache = self.get_session_cache(session_id)
        return cache["recent_messages"] if cache else []

    def get_summary_context(self, session_id: str) -> str:
        cache = self.get_session_cache(session_id)
        return cache["summary_context"] if cache else ""

    def update_summary_context(self, session_id: str, new_summary: str):
        self.cache_client.client.hset(
            self._make_key(session_id),
            key=KeyCache.SUMMARY_CONTEXT,
            value=new_summary
        )

    